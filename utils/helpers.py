import ast
import asyncio
import os 
import json
from typing import Any, Dict, List
import json 
import pickle 
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