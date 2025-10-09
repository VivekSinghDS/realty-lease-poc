import os 
import json
from pathlib import Path
from typing import Any
import fitz  # PyMuPDF
import base64
import json 
from fastapi import UploadFile
import requests
from adapters.llms._groq import _Groq
import json 
import requests 
from adapters.llms._openai import _OpenAI
from adapters.llms._perplexity import _Perplexity
from adapters.llms.base import LargeLanguageModel

def get_llm_adapter() -> LargeLanguageModel:
    llm_details = json.loads(str(os.environ.get('LLM')))
    if llm_details['provider'] == "openai":
        return _OpenAI()
    elif llm_details['provider'] == "groq":
        return _Groq()
    else:
        return _Perplexity()
    
    
def save_response_to_file(response_data: str, filename: str):
    try:
        # Remove file extension from filename to use as directory name
        base_filename = Path(filename).stem
        
        # Create directory path
        directory_path = Path(f"./results/{base_filename}")
        directory_path.mkdir(parents=True, exist_ok=True)
        
        # Parse the response as JSON (assuming it's JSON format)
        try:
            response_json = json.loads(response_data)
        except json.JSONDecodeError:
            # If it's not valid JSON, wrap it in a JSON structure
            response_json = {"response": response_data}
        
        # Save to result.json
        result_file_path = directory_path / "result.json"
        with open(result_file_path, 'w', encoding='utf-8') as file:
            json.dump(response_json, file, indent=2, ensure_ascii=False)
            
        print(f"Successfully saved response to {result_file_path}")
        
    except Exception as e:
        print(f"Error saving response to file: {str(e)}")
        
def update_result_json(resultant_json: dict, llm_iterative_response_json: str | dict) -> dict:
    """
    Iteratively updates the resultant_json with new data from LLM response.
    
    Args:
        resultant_json: The current state of the lease JSON (can be empty dict initially)
        llm_iterative_response_json: The LLM response, either as a JSON string or dict
        
    Returns:
        Updated resultant_json with merged data
    """
    try:
        # Parse LLM response if it's a string
        if isinstance(llm_iterative_response_json, str):
            try:
                new_data = json.loads(llm_iterative_response_json)
            except json.JSONDecodeError:
                # Try to extract JSON from the response if it contains other text
                first_open = llm_iterative_response_json.find('{')
                last_close = llm_iterative_response_json.rfind('}')
                if first_open != -1 and last_close != -1 and first_open < last_close:
                    json_substring = llm_iterative_response_json[first_open:last_close + 1]
                    new_data = json.loads(json_substring)
                else:
                    print(f"Warning: Could not parse LLM response as JSON: {llm_iterative_response_json[:100]}")
                    return resultant_json
        else:
            new_data = llm_iterative_response_json
            
        # If resultant_json is empty, initialize with the structure
        if not resultant_json:
            # Load the template structure
            template_path = os.path.join(os.path.dirname(__file__), 'references', 'lease_structure_template.json')
            if os.path.exists(template_path):
                with open(template_path, 'r') as f:
                    resultant_json = json.load(f)
            else:
                # Fallback to empty dict if template doesn't exist
                resultant_json = {}
        
        # Deep merge the new data into resultant_json
        resultant_json = _deep_merge(resultant_json, new_data)
        
        return resultant_json
        
    except Exception as e:
        print(f"Error updating result JSON: {str(e)}")
        return resultant_json


def _deep_merge(base: dict, update: dict) -> dict:
    """
    Recursively merges update dict into base dict.
    
    For dictionaries: merge recursively
    For lists: append unique items (based on content similarity)
    For primitives: update with new value if it's not empty/default
    
    Args:
        base: The base dictionary to merge into
        update: The dictionary with new values to merge
        
    Returns:
        Merged dictionary
    """
    for key, value in update.items():
        if key not in base:
            # Key doesn't exist in base, add it
            base[key] = value
        elif isinstance(value, dict) and isinstance(base[key], dict):
            # Both are dicts, merge recursively
            base[key] = _deep_merge(base[key], value)
        elif isinstance(value, list) and isinstance(base[key], list):
            # Both are lists, append new unique items
            for item in value:
                # Check if item already exists (to avoid duplicates)
                if not _item_exists_in_list(base[key], item):
                    base[key].append(item)
        else:
            # For primitive values, update only if new value is meaningful
            if value and value != "string" and value != "":
                base[key] = value
    
    return base


def _item_exists_in_list(lst: list, item: Any) -> bool:
    """
    Check if an item already exists in a list.
    Handles both primitive types and dict/list comparisons.
    
    Args:
        lst: The list to check
        item: The item to look for
        
    Returns:
        True if item exists in list, False otherwise
    """
    if not lst:
        return False
        
    # For dictionaries, check if a similar dict exists based on key fields
    if isinstance(item, dict):
        for existing_item in lst:
            if isinstance(existing_item, dict):
                # Check similarity based on key fields or citation
                if _dicts_are_similar(existing_item, item):
                    return True
    else:
        # For primitives, simple membership check
        return item in lst
    
    return False


def _dicts_are_similar(dict1: dict, dict2: dict, threshold: float = 0.7) -> bool:
    """
    Check if two dictionaries are similar enough to be considered duplicates.
    Compares based on common fields like citation, description, etc.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        threshold: Similarity threshold (0.0 to 1.0)
        
    Returns:
        True if dictionaries are similar, False otherwise
    """
    # Priority fields to check for similarity
    priority_fields = ['citation', 'description', 'clause_name', 'value']
    
    matches = 0
    total_checks = 0
    
    for field in priority_fields:
        if field in dict1 and field in dict2:
            total_checks += 1
            if dict1[field] == dict2[field]:
                matches += 1
    
    # If no priority fields found, check all common keys
    if total_checks == 0:
        common_keys = set(dict1.keys()) & set(dict2.keys())
        if not common_keys:
            return False
        total_checks = len(common_keys)
        for key in common_keys:
            if dict1[key] == dict2[key]:
                matches += 1
    
    # Calculate similarity ratio
    similarity = matches / total_checks if total_checks > 0 else 0
    return similarity >= threshold

def content_from_doc(info_list):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    SERVICE_ACCOUNT_FILE = './attempt_3.json'
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

    credentials = service_account.Credentials.from_service_account_file(
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
