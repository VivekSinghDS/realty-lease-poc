from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import pickle

# If modifying these scopes, delete the token.pickle file
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

class GoogleDocsManager:
    def __init__(self, credentials_file='credentials.json'):
        """Initialize the Google Docs API client"""
        self.credentials_file = credentials_file
        self.service = self._authenticate()
    
    def _authenticate(self):
        """Authenticate and return the Google Docs service"""
        creds = None
        
        # Token.pickle stores the user's access and refresh tokens
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=8080)
            
            # Save credentials for next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        return build('docs', 'v1', credentials=creds)
    
    def get_document_content(self, document_id):
        """
        Fetch the latest content from a Google Doc
        
        Args:
            document_id: The ID of the Google Doc (from the URL)
        
        Returns:
            str: The text content of the document
        """
        try:
            document = self.service.documents().get(documentId=document_id).execute()
            
            # Extract text content
            content = self._extract_text(document.get('body').get('content'))
            
            return content
        
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None
    
    def _extract_text(self, elements):
        """Extract text from document structure"""
        text = ''
        
        for element in elements:
            if 'paragraph' in element:
                for text_run in element['paragraph']['elements']:
                    if 'textRun' in text_run:
                        text += text_run['textRun']['content']
            elif 'table' in element:
                # Handle tables if needed
                for row in element['table']['tableRows']:
                    for cell in row['tableCells']:
                        text += self._extract_text(cell['content'])
        
        return text
    
    def get_multiple_docs(self, document_ids):
        """
        Fetch content from multiple Google Docs
        
        Args:
            document_ids: List of document IDs
        
        Returns:
            dict: Dictionary with document IDs as keys and content as values
        """
        docs_content = {}
        
        for doc_id in document_ids:
            print(f"Fetching document: {doc_id}")
            content = self.get_document_content(doc_id)
            docs_content[doc_id] = content
        
        return docs_content


# Example usage
if __name__ == "__main__":
    # Initialize the manager
    manager = GoogleDocsManager('./creds.json')
    
    # Your 5 Google Doc IDs (get these from the document URLs)
    # URL format: https://docs.google.com/document/d/DOCUMENT_ID/edit
    doc_ids = [
        '17yWZSPn_wB09cb2Ln55tnF2zBn8VJBaQSCLajGi0Gqs',

    ]
    
    # Fetch all documents
    all_docs = dict(manager.get_multiple_docs(doc_ids))
    import json
    print(json.dumps(all_docs))
    # Store in 5 separate variables
    doc1_content = all_docs.get(doc_ids[0], '')
    doc2_content = all_docs.get(doc_ids[1], '')
    doc3_content = all_docs.get(doc_ids[2], '')
    doc4_content = all_docs.get(doc_ids[3], '')
    doc5_content = all_docs.get(doc_ids[4], '')
    
    
    # Print the content (for verification)
    print("\n=== Document 1 ===")
    print(doc1_content[:200] + "..." if len(doc1_content) > 200 else doc1_content)
    
    print("\n=== Document 2 ===")
    print(doc2_content[:200] + "..." if len(doc2_content) > 200 else doc2_content)
    
    print("\n=== Document 3 ===")
    print(doc3_content[:200] + "..." if len(doc3_content) > 200 else doc3_content)
    
    print("\n=== Document 4 ===")
    print(doc4_content[:200] + "..." if len(doc4_content) > 200 else doc4_content)
    
    print("\n=== Document 5 ===")
    print(doc5_content[:200] + "..." if len(doc5_content) > 200 else doc5_content)