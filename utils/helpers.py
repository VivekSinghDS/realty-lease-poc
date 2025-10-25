import ast
import asyncio
import os 
import json
from typing import Any, Dict, List
import json 
import pickle 
from typing import Dict, Any, List
from adapters.database._local import _Local
from adapters.database.base import Database
from adapters.llms._groq import _Groq
from adapters.llms._openai import _OpenAI
from adapters.llms._perplexity import _Perplexity
from adapters.llms.base import LargeLanguageModel
from dotenv import load_dotenv

from utils.constants import ANALYSIS_CONFIG, AnalysisType
from utils.parsers.pdf import PDFChunker
from utils.references import audit 

load_dotenv()
def get_llm_adapter() -> LargeLanguageModel:
    llm_details = json.loads(str(os.environ.get('LLM')))
    if llm_details['provider'] == "openai":
        return _OpenAI()
    elif llm_details['provider'] == "groq":
        return _Groq()
    else:
        return _Perplexity()


llm_adapter = get_llm_adapter()
def build_chunk_data(chunks: List) -> str:
    """Convert chunks to formatted string data"""
    data = "Given below is the data of a Lease PDF\n"
    for i, chunk in enumerate(chunks):
        data += f"""
        
            Details about Page number {i}
            "chunk_id": {chunk.chunk_id},
            "page_number": {chunk.page_number},
            "text": {chunk.original_page_text},
            "previous_overlap": {chunk.previous_overlap},
            "next_overlap": {chunk.next_overlap},
            "overlap_info": {chunk.overlap_info}
        
        """
    return data

def parse_llm_response(content: str) -> Dict[str, Any]:
    """Parse LLM response with fallback handling"""
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        try:
            return ast.literal_eval(content)
        except (ValueError, SyntaxError):
            return {"content": content}

def get_db_adapter() -> Database:
    provider_config: dict = json.loads(str(os.environ.get('DATABASE')))
    if provider_config['provider'] == "local":
        return _Local()
    return _Local()

async def load_or_process_pdf(filename: str, file_content: bytes) -> List:
    """Load cached PDF chunks or process new PDF"""
    cache_path = f'./cached_pdfs/{filename}.pkl'
    
    if os.path.exists(cache_path):
        print(f'Found cached PDF analysis for {filename}')
        with open(cache_path, 'rb') as f:
            return pickle.load(f)
    
    print(f'Processing new PDF: {filename}')
    chunker = PDFChunker(overlap_percentage=0.2)
    chunks = chunker.process_pdf(file_content, extract_tables=True)
    
    # Cache the chunks
    os.makedirs('./cached_pdfs', exist_ok=True)
    with open(cache_path, 'wb') as f:
        pickle.dump(chunks, f)
    
    return chunks        

async def perform_standard_analysis(
    analysis_type: AnalysisType,
    chunks: List
) -> Dict[str, Any]:
    """Perform standard analysis (info, space, charge-schedules, misc, executive-summary)"""
    config = ANALYSIS_CONFIG[analysis_type]
    data = build_chunk_data(chunks)
    
    documents = content_from_doc(config["doc_indices"])
    field_definitions = documents[0]
    system_template = documents[1]
    
    system_prompt = system_template.format(
        reference=field_definitions,
        JSON_STRUCTURE=json.dumps(config["structure"])
    )
    
    payload = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": data}
    ]
    
    response = llm_adapter.get_non_streaming_response(payload)
    return parse_llm_response(response.choices[0].message.content)

async def perform_audit_analysis(chunks: List) -> Dict[str, Any]:
    """Perform audit analysis"""
    data = build_chunk_data(chunks)
    
    payload = [
        {
            "role": "system",
            "content": audit.system + " Output format is as follows " + json.dumps(audit.output_schema)
        },
        {
            "role": "user",
            "content": data + """Critically analyze the provided Lease Agreement by comparing clauses and identifying all terms that are ambiguous, 
                rely on subjective future agreement, contain internal conflicts, or represent significant, unquantified financial/operational 
                risks for the Tenant. Every identified point must be supported by direct citations.
                Finally make sure to provide all the Tabled and bulleted risk register with verbatim citations for every point."""
        }
    ]
    
    response = llm_adapter.get_non_streaming_response(payload)
    return parse_llm_response(response.choices[0].message.content)


async def run_single_analysis(
    analysis_type: AnalysisType,
    chunks: List
) -> Dict[str, Any]:
    """Run a single analysis based on type"""
    if analysis_type == AnalysisType.AUDIT:
        return await perform_audit_analysis(chunks)
    else:
        return await perform_standard_analysis(analysis_type, chunks)

async def run_all_analyses(chunks: List) -> Dict[str, Any]:
    """Run all analyses in parallel and merge results"""
    tasks = {
        analysis_type.value: run_single_analysis(analysis_type, chunks)
        for analysis_type in AnalysisType
        if analysis_type != AnalysisType.ALL
    }
    
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    
    # Flatten results by merging all dictionaries at root level
    combined_results = {}
    for key, result in zip(tasks.keys(), results):
        if isinstance(result, Exception):
            combined_results[f"{key}_error"] = str(result)
        else:
            # Merge the result dictionary into combined_results
            if isinstance(result, dict):
                combined_results.update(result)
            else:
                combined_results[key] = result
    
    return combined_results


def content_from_doc(info_list):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    # SERVICE_ACCOUNT_FILE = './attempt_4.json'
    SERVICE_ACCOUNT_FILE = json.loads(os.getenv("google_creds"))
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

    # credentials = service_account.Credentials.from_service_account_file(
    #     SERVICE_ACCOUNT_FILE, scopes=SCOPES
    # )
    credentials = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build('docs', 'v1', credentials=credentials)
    DOCUMENT_ID = '17yWZSPn_wB09cb2Ln55tnF2zBn8VJBaQSCLajGi0Gqs'

    # Request document with tabs content included
    doc = service.documents().get(
        documentId=DOCUMENT_ID,
        includeTabsContent=True
    ).execute()

    content = []

    for i, tab in enumerate(doc['tabs']):
        if i not in info_list:
            continue
        tab_properties = tab.get('tabProperties', {})
        tab_title = tab_properties.get('title', 'Untitled Tab')
        tab_id = tab_properties.get('tabId', 'N/A')
        
        print(f"\n--- Tab: {tab_title} (ID: {tab_id}) ---")
        
        # Extract text from this tab
        if 'documentTab' in tab:
            text = ''
            body = tab['documentTab'].get('body', {})
            for c in body.get('content', []):
                if 'paragraph' in c:
                    for e in c['paragraph']['elements']:
                        if 'textRun' in e:
                            text += e['textRun']['content']
            
            content.append(text)
    return content



def update_result_json(message_dict: Dict[str, Any], message_content: str) -> Dict[str, Any]:
    """
    Iteratively updates the result dictionary with new chunk data from LLM response.
    Handles appending to arrays and merging nested structures.
    
    Args:
        message_dict: The cumulative result dictionary
        message_content: The JSON string response from LLM for current chunk
        
    Returns:
        Updated message_dict with merged content
    """
    # Initialize empty structure if message_dict is empty
    if not message_dict:
        message_dict = {
            "newCamRules": [],
            "continuedRules": [],
            "crossPageContext": [],
            "flagsAndObservations": {
                "ambiguities": [],
                "conflicts": [],
                "missingProvisions": [],
                "tenantConcerns": [],
                "provisionsSpanningToNextPage": []
            },
            "cumulativeCamRulesSummary": {
                "totalRulesExtracted": 0,
                "rulesByCategory": {
                    "proportionateShare": 0,
                    "camExpenseCategories": 0,
                    "exclusions": 0,
                    "paymentTerms": 0,
                    "capsLimitations": 0,
                    "reconciliationProcedures": 0,
                    "baseYearProvisions": 0,
                    "grossUpProvisions": 0,
                    "administrativeFees": 0,
                    "auditRights": 0,
                    "noticeRequirements": 0,
                    "controllableVsNonControllable": 0,
                    "definitions": 0,
                    "calculationMethods": 0
                },
                "overallTenantRiskAssessment": "Low",
                "keyTenantProtections": [],
                "keyTenantExposures": []
            }
        }
    
    # Parse the new chunk data
    try:
        # Clean the message content (remove markdown code blocks if present)
        cleaned_content = message_content.strip()
        if cleaned_content.startswith("```json"):
            cleaned_content = cleaned_content[7:]
        if cleaned_content.startswith("```"):
            cleaned_content = cleaned_content[3:]
        if cleaned_content.endswith("```"):
            cleaned_content = cleaned_content[:-3]
        cleaned_content = cleaned_content.strip()
        
        new_data = json.loads(cleaned_content)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Problematic content: {message_content[:200]}...")
        raise ValueError(f"Invalid JSON response from LLM: {e}")
    
    # Merge newCamRules (append new rules)
    if "newCamRules" in new_data and new_data["newCamRules"]:
        message_dict["newCamRules"].extend(new_data["newCamRules"])
    
    # Merge continuedRules (append)
    if "continuedRules" in new_data and new_data["continuedRules"]:
        message_dict["continuedRules"].extend(new_data["continuedRules"])
    
    # Merge crossPageContext (append)
    if "crossPageContext" in new_data and new_data["crossPageContext"]:
        message_dict["crossPageContext"].extend(new_data["crossPageContext"])
    
    # Merge flagsAndObservations (append to each sub-array)
    if "flagsAndObservations" in new_data:
        flags = new_data["flagsAndObservations"]
        
        if "ambiguities" in flags and flags["ambiguities"]:
            message_dict["flagsAndObservations"]["ambiguities"].extend(flags["ambiguities"])
        
        if "conflicts" in flags and flags["conflicts"]:
            message_dict["flagsAndObservations"]["conflicts"].extend(flags["conflicts"])
        
        if "missingProvisions" in flags and flags["missingProvisions"]:
            message_dict["flagsAndObservations"]["missingProvisions"].extend(flags["missingProvisions"])
        
        if "tenantConcerns" in flags and flags["tenantConcerns"]:
            message_dict["flagsAndObservations"]["tenantConcerns"].extend(flags["tenantConcerns"])
        
        if "provisionsSpanningToNextPage" in flags and flags["provisionsSpanningToNextPage"]:
            # Replace rather than append for spanning provisions (only last chunk matters)
            message_dict["flagsAndObservations"]["provisionsSpanningToNextPage"] = flags["provisionsSpanningToNextPage"]
    
    # Merge cumulativeCamRulesSummary (update counts and merge arrays)
    if "cumulativeCamRulesSummary" in new_data:
        summary = new_data["cumulativeCamRulesSummary"]
        
        # Update total rules count
        if "totalRulesExtracted" in summary:
            message_dict["cumulativeCamRulesSummary"]["totalRulesExtracted"] = len(message_dict["newCamRules"])
        
        # Update category counts (accumulate)
        if "rulesByCategory" in summary:
            for category, count in summary["rulesByCategory"].items():
                if category in message_dict["cumulativeCamRulesSummary"]["rulesByCategory"]:
                    message_dict["cumulativeCamRulesSummary"]["rulesByCategory"][category] += count
        
        # Update risk assessment (take the highest severity)
        if "overallTenantRiskAssessment" in summary:
            current_risk = message_dict["cumulativeCamRulesSummary"]["overallTenantRiskAssessment"]
            new_risk = summary["overallTenantRiskAssessment"]
            risk_hierarchy = {"Low": 0, "Medium": 1, "High": 2, "Critical": 3}
            if risk_hierarchy.get(new_risk, 0) > risk_hierarchy.get(current_risk, 0):
                message_dict["cumulativeCamRulesSummary"]["overallTenantRiskAssessment"] = new_risk
        
        # Merge keyTenantProtections (avoid duplicates)
        if "keyTenantProtections" in summary and summary["keyTenantProtections"]:
            for protection in summary["keyTenantProtections"]:
                if protection not in message_dict["cumulativeCamRulesSummary"]["keyTenantProtections"]:
                    message_dict["cumulativeCamRulesSummary"]["keyTenantProtections"].append(protection)
        
        # Merge keyTenantExposures (avoid duplicates)
        if "keyTenantExposures" in summary and summary["keyTenantExposures"]:
            for exposure in summary["keyTenantExposures"]:
                if exposure not in message_dict["cumulativeCamRulesSummary"]["keyTenantExposures"]:
                    message_dict["cumulativeCamRulesSummary"]["keyTenantExposures"].append(exposure)
    
    return message_dict