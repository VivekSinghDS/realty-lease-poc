import os
from datetime import datetime
import json
from http import HTTPStatus
from fastapi import File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from utils.constants import AnalysisType
from utils.helpers import get_db_adapter, get_llm_adapter, load_or_process_pdf, run_all_analyses, run_single_analysis
from utils.references import amendments
from utils.schemas import CreateRequest


router = APIRouter()

database_adapter = get_db_adapter()
llm_adapter = get_llm_adapter()

@router.post("")
async def create_company(item: CreateRequest):
    return database_adapter.create({"name": item.name})

@router.get("")
async def get_company():
    companies_data: dict = database_adapter.get() or {}
    # Transform the response to match frontend expectations
    companies = []
    for i, company_name in enumerate(companies_data.get("companies", [])):
        companies.append({
            "id": i + 1,  # Generate sequential ID
            "uid": company_name,  # Use company name as UID
            "name": company_name
        })
    return {"companies": companies}

@router.get("/{company_uid}/documents")
async def get_single_company(company_uid: str):
    return database_adapter.get_single({"uid": company_uid})

@router.get("/{company_uid}/documents")
async def get_analysis(company_uid: str):
    return database_adapter.get_single({"uid": company_uid})

@router.post("/{company_uid}/documents/analyze")
async def get_document_analysis(
    company_uid: str,
    file: UploadFile = File(...),
    documentType: str = Form(...),
    analysisType: str = Form(AnalysisType.ALL.value)  # Default to ALL
):
    try:
        if not file:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}},
                status_code=HTTPStatus.BAD_REQUEST.value
            )
        
        # Validate analysis type
        try:
            requested_analysis = AnalysisType(analysisType.lower())
        except ValueError:
            return JSONResponse(
                content={"error": f"Invalid analysis type: {analysisType}. Valid types: {[e.value for e in AnalysisType]}"},
                status_code=HTTPStatus.BAD_REQUEST.value
            )
        
        # Load or process PDF
        file_content = await file.read()
        chunks = await load_or_process_pdf(file.filename or "", file_content)
        if documentType == "lease":
            # Perform requested analysis
            if requested_analysis == AnalysisType.ALL:
                results = await run_all_analyses(chunks)
            else:
                result = await run_single_analysis(requested_analysis, chunks)
                results = {requested_analysis.value: result}
            
            
            dir_path = f"./companies/{company_uid}/{documentType.lower()}"
            os.makedirs(dir_path, exist_ok=True)  # ✅ Create folder if missing
            
            output_path = os.path.join(dir_path, "output.json")
            with open(output_path, "w") as fp:
                json.dump(results, fp)
            
            
            document_metadata = {
                "id": file.filename,
                "uid": file.filename,
                "filename": file.filename,
                "type": documentType,
                "companyId": company_uid,
                "createdAt": datetime.now().isoformat(),
                "analysisData": results  # Store analysis in document
            }
            
            return {
                "document": document_metadata,
                "analysisData": results
            }
        else:
            print('bouncy boy')
            data = "Given below is the data of a Amendment file of a particular Lease\n"
            for i, chunk in enumerate(chunks):
                data += f"""\n\n
                
                    Details about Page number {str(i)}
                    "chunk_id": {chunk.chunk_id},
                    "page_number": {chunk.page_number},
                    "text": {chunk.original_page_text},
                    "previous_overlap": {chunk.previous_overlap},
                    "next_overlap": {chunk.next_overlap},
                    "overlap_info": {chunk.overlap_info}
                
                """
                
            with open(f'./companies/{company_uid}/lease/output.json', 'r') as f:
                lease_output = json.load(f)
            
            data += f"""
                \n\n
                Here is the Lease Abstraction uptil now : 
                
                {lease_output}
                
            """
            
            payload = [
                {
                    "role": "system", 
                    "content": amendments.system
                },
                {
                    "role": "user", 
                    "content": data
                }
            ]
            
            response = llm_adapter.get_non_streaming_response(payload)
            message_content = response.choices[0].message.content
            parsed = json.loads(message_content)
            with open(f'./companies/{company_uid}/amendments/{file.filename}.json', "w") as fp:
                json.dump(parsed, fp, indent=4)
            
            document_metadata = {
                "id": file.filename,
                "uid": file.filename,
                "filename": file.filename,
                "type": documentType,
                "companyId": company_uid,
                "createdAt": datetime.now().isoformat(),
                "analysisData": dict(json.loads(message_content))  # Store analysis in document
            }
            return {
                "document": document_metadata,
                "analysisData": dict(json.loads(message_content))
            }
    except Exception as e:
        print(f"Error in document analysis: {str(e)}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value
        )
@router.put("")
async def update_company():
    pass

@router.delete("")
async def delete_company():
    pass

