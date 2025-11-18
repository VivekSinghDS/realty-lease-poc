import os
from datetime import datetime
import json
import pickle
from http import HTTPStatus
from fastapi import File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from utils.constants import AnalysisType
from utils.helpers import content_from_doc, get_db_adapter, get_llm_adapter, load_or_process_pdf, run_all_analyses, run_single_analysis
from utils.parsers.pdf import PDFChunker
from utils.references import amendments, cam
from utils.schemas import CreateRequest


router = APIRouter()

database_adapter = get_db_adapter()
llm_adapter = get_llm_adapter()

@router.post("")
async def create_company(item: CreateRequest):
    return database_adapter.create({"name": item.name})

@router.delete("/{company_uid}")
async def delete_company(company_uid: str):
    return database_adapter.delete({"name": company_uid})

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

@router.post("/{company_uid}/documents/cam")
async def get_cam_rules(
    company_uid: str,
    assets: UploadFile = File(...),
    documentType: str = Form(...),
):
    
    try:
        print('inside here')
        if not assets:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}},
                status_code=HTTPStatus.BAD_REQUEST.value
            )
        
        if os.path.exists(f'./cached_pdfs/{assets.filename}.pkl'):
            print('Found the PDF analysis << --')
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'rb') as fp:
                chunks = pickle.load(fp)
        
        else:
            chunker = PDFChunker(overlap_percentage=0.2)
            # Process the PDF from bytes
            chunks = chunker.process_pdf(await assets.read(), extract_tables=True)
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'wb') as fp:
                pickle.dump(chunks, fp)
        
        documents = content_from_doc([6, 7])
        message_content = None  # Initialize to avoid NameError if chunks is empty
        previous_cam = None
        for i, chunk in enumerate(chunks):
            chunk_data = f"""
                Here is the content from page {chunk.page_number} of the lease document:
                
                Page number: {chunk.page_number}
                Text content: {chunk.original_page_text} # full page for next, and previous 
                """
                
            field_defintions: str= documents[0]
            system: str = documents[1]
            
                # if not os.path.exists('./cam_result'):
                #     os.makedirs('./cam_result', exist_ok=True)
                    
            system_prompt = system.format(CURRENT_PAGE_NUMBER = str(i + 1), PREVIOUS_PAGE_NUMBER = str(i), NEXT_PAGE_NUMBER = str(i + 2), NEXT_PAGE_CONTENT = None,
                                        PREVIOUS_PAGE_CONTENT = None if i == 0 else chunks[i - 1].original_page_text, CURRENT_PAGE_CONTENT = chunk.original_page_text, PREVIOUSLY_EXTRACTED_CAM_RULES = previous_cam)
        
            payload = [
                    {
                        "role": "system", "content": system_prompt + cam.JSON_PROD_INSTRUCTIONS
                    },
                    {
                        "role": "user", "content": chunk_data
                    }
                ]   
            response = llm_adapter.get_non_streaming_response(payload)
            message_content = response.choices[0].message.content
            try:
                # Assuming message_content is a JSON string
                import json
                # Use a non-conflicting variable name
                parsed_cam_data = json.loads(message_content) 
                print('parsing done')
                previous_cam = parsed_cam_data 


            except json.JSONDecodeError as json_err:
                print(f"Failed to parse JSON on page {i}: {json_err}")
                # Decide how to handle bad JSON from LLM (e.g., skip, use raw text)
                previous_cam = message_content # Fallback to raw text
            # os.makedirs('./cam_result', exist_ok=True)
                
            # with open(f'./cam_result/{str(i)}.txt', 'w') as fp:
            #     fp.write(str(message_content))

        if documentType == "lease":
            dir_path = f"./companies/{company_uid}/{documentType.lower()}"
            os.makedirs(dir_path, exist_ok=True)  # ✅ Create folder if missing
            
            output_path = os.path.join(dir_path, "output.json")
            
            # ✅ Step 1: Read existing JSON (if it exists)
            if os.path.exists(output_path):
                with open(output_path, "r") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {}  # fallback if file is empty or invalid JSON
            else:
                data = {}

            # ✅ Step 2: Add or update the "cam" key
            data["cam"] = previous_cam

            # ✅ Step 3: Save back to output.json
            with open(output_path, "w") as f:
                json.dump(data, f, indent=4)
        else:
            dir_path = f"./companies/{company_uid}/{documentType.lower()}"
            os.makedirs(dir_path, exist_ok=True)  # ✅ Create folder if missing
            
            output_path = os.path.join(dir_path, f"{assets.filename}.json")
            
            # ✅ Step 1: Read existing JSON (if it exists)
            if os.path.exists(output_path):
                with open(output_path, "r") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {}  # fallback if file is empty or invalid JSON
            else:
                data = {}

            # ✅ Step 2: Add or update the "cam" key
            data["cam"] = previous_cam

            # ✅ Step 3: Save back to output.json
            with open(output_path, "w") as f:
                json.dump(data, f, indent=4)
        
        return {
            "cam": previous_cam
        }
        
    except Exception as error:
        print(f"Error in CAM extraction: {str(error)}")
        import traceback
        traceback.print_exc()
        try:
            return JSONResponse(
                content={"error": str(error)},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value
            )
        except Exception as response_error:
            # If even the error response fails, log and re-raise
            print(f"Failed to create error response: {str(response_error)}")
            raise
        
@router.put("")
async def update_company():
    pass



