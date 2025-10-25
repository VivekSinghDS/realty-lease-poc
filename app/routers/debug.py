import ast
import json 
import os 
from http import HTTPStatus
from fastapi import (
    APIRouter,
    File,
    UploadFile,
)
import pickle 
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from utils.logs import logger
from utils.helpers import content_from_doc, get_llm_adapter, update_result_json
from utils.parsers.pdf import PDFChunker
from utils.references import audit, cam, chargeSchedules, executive_summary, leaseInformation, misc, space, amendments
from utils.schemas import SaveZod
import time 
load_dotenv()
router = APIRouter()

llm_adapter = get_llm_adapter()

@router.post("/info")
async def get_lease_abstraction(
    assets: UploadFile | None = File(None)
):
        if not assets:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )
        
        if os.path.exists(f'./cached_pdfs/{assets.filename}.pkl'):
            print('Found the PDF analysis << --')
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'rb') as file:
                chunks = pickle.load(file)
        else:
            chunker = PDFChunker(overlap_percentage=0.2)
            # Process the PDF from bytes
            chunks = chunker.process_pdf(await assets.read(), extract_tables=True)
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'wb') as file:
                pickle.dump(chunks, file)
        
        # Convert chunks to JSON-serializable format
        data = "Given below is the data of a Lease PDF"
        for i, chunk in enumerate(chunks):
            data += f"""
            
                Details about Page number {str(i)}
                "chunk_id": {chunk.chunk_id},
                "page_number": {chunk.page_number},
                "text": {chunk.original_page_text},
                "previous_overlap": {chunk.previous_overlap},
                "next_overlap": {chunk.next_overlap},
                "overlap_info": {chunk.overlap_info}
            
            """
            
        documents = content_from_doc([0, 5])
        field_defintions: str= documents[0]
        system: str = documents[1]
        system_prompt = system.format(reference = field_defintions, JSON_STRUCTURE = json.dumps(leaseInformation.structure))
               
        payload = [
            {
                "role": "system", "content": system_prompt  # will be filled by Ashruth 
            },
            {
                "role": "user", "content": data
            }
        ]
        
        response = llm_adapter.get_non_streaming_response(payload)

        message_content = response.choices[0].message.content

        try:
            message_dict = json.loads(message_content)
        except json.JSONDecodeError:
            try:
                # Handle single-quoted Python-style dicts
                message_dict = ast.literal_eval(message_content)
            except (ValueError, SyntaxError):
                # Fallback — wrap raw content
                message_dict = {"content": message_content}

        return message_dict
    
@router.post("/space")
async def get_space(
    assets: UploadFile | None = File(None)
):
        if not assets:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )
        
        if os.path.exists(f'./cached_pdfs/{assets.filename}.pkl'):
            print('Found the PDF analysis << --')
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'rb') as file:
                chunks = pickle.load(file)
        else:
            chunker = PDFChunker(overlap_percentage=0.2)
            # Process the PDF from bytes
            chunks = chunker.process_pdf(await assets.read(), extract_tables=True)
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'wb') as file:
                pickle.dump(chunks, file)
        
        
        # Convert chunks to JSON-serializable format
        data = "Given below is the data of a Lease PDF\n"
        for i, chunk in enumerate(chunks):
            data += f"""
            
                Details about Page number {str(i)}
                "chunk_id": {chunk.chunk_id},
                "page_number": {chunk.page_number},
                "text": {chunk.original_page_text},
                "previous_overlap": {chunk.previous_overlap},
                "next_overlap": {chunk.next_overlap},
                "overlap_info": {chunk.overlap_info},
            
            """
            
        documents = content_from_doc([1, 5])
        field_defintions: str= documents[0]
        system: str = documents[1]
        system_prompt = system.format(reference = field_defintions, JSON_STRUCTURE = json.dumps(space.structure))
               
        payload = [
            {
                "role": "system", "content": system_prompt  # will be filled by Ashruth 
            },
            {
                "role": "user", "content": data
            }
        ]
        
        response = llm_adapter.get_non_streaming_response(payload)

        message_content = response.choices[0].message.content

        try:
            message_dict = json.loads(message_content)
        except json.JSONDecodeError:
            try:
                # Handle single-quoted Python-style dicts
                message_dict = ast.literal_eval(message_content)
            except (ValueError, SyntaxError):
                # Fallback — wrap raw content
                message_dict = {"content": message_content}

        return message_dict
    
@router.post("/charge-schedules")
async def get_sched(
    assets: UploadFile | None = File(None)
):
        if not assets:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )
        
        if os.path.exists(f'./cached_pdfs/{assets.filename}.pkl'):
            print('Found the PDF analysis << --')
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'rb') as file:
                chunks = pickle.load(file)
        else:
            chunker = PDFChunker(overlap_percentage=0.2)
            # Process the PDF from bytes
            chunks = chunker.process_pdf(await assets.read(), extract_tables=True)
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'wb') as file:
                pickle.dump(chunks, file)
        
        # Convert chunks to JSON-serializable format
        data = "Given below is the data of a Lease PDF"
        for i, chunk in enumerate(chunks):
            data += f"""
            
                Details about Page number {str(i)}
                "chunk_id": {chunk.chunk_id},
                "page_number": {chunk.page_number},
                "text": {chunk.original_page_text},
                "previous_overlap": {chunk.previous_overlap},
                "next_overlap": {chunk.next_overlap},
                "overlap_info": {chunk.overlap_info}
            
            """
            
        documents = content_from_doc([2, 5])
        field_defintions: str= documents[0]
        system: str = documents[1]
        system_prompt = system.format(reference = field_defintions, JSON_STRUCTURE = json.dumps(chargeSchedules.structure))
               
        payload = [
            {
                "role": "system", "content": system_prompt  # will be filled by Ashruth 
            },
            {
                "role": "user", "content": data
            }
        ]
        
        response = llm_adapter.get_non_streaming_response(payload)

        message_content = response.choices[0].message.content

        try:
            message_dict = json.loads(message_content)
        except json.JSONDecodeError:
            try:
                # Handle single-quoted Python-style dicts
                message_dict = ast.literal_eval(message_content)
            except (ValueError, SyntaxError):
                # Fallback — wrap raw content
                message_dict = {"content": message_content}

        return message_dict
    
@router.post("/misc")
async def get_misc(
    assets: UploadFile | None = File(None)
):
        if not assets:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )
        
        if os.path.exists(f'./cached_pdfs/{assets.filename}.pkl'):
            print('Found the PDF analysis << --')
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'rb') as file:
                chunks = pickle.load(file)
        else:
            chunker = PDFChunker(overlap_percentage=0.2)
            # Process the PDF from bytes
            chunks = chunker.process_pdf(await assets.read(), extract_tables=True)
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'wb') as file:
                pickle.dump(chunks, file)
        
        # Convert chunks to JSON-serializable format
        data = "Given below is the data of a Lease PDF"
        for i, chunk in enumerate(chunks):
            data += f"""
            
                Details about Page number {str(i)}
                "chunk_id": {chunk.chunk_id},
                "page_number": {chunk.page_number},
                "text": {chunk.original_page_text},
                "previous_overlap": {chunk.previous_overlap},
                "next_overlap": {chunk.next_overlap},
                "overlap_info": {chunk.overlap_info}
            
            """
            
        documents = content_from_doc([3, 5])
        field_defintions: str= documents[0]
        system: str = documents[1]
        system_prompt = system.format(reference = field_defintions, JSON_STRUCTURE = json.dumps(misc.structure))
               
        payload = [
            {
                "role": "system", "content": system_prompt  # will be filled by Ashruth 
            },
            {
                "role": "user", "content": data
            }
        ]
        
        response = llm_adapter.get_non_streaming_response(payload)

        message_content = response.choices[0].message.content

        try:
            message_dict = json.loads(message_content)
        except json.JSONDecodeError:
            try:
                # Handle single-quoted Python-style dicts
                message_dict = ast.literal_eval(message_content)
            except (ValueError, SyntaxError):
                # Fallback — wrap raw content
                message_dict = {"content": message_content}

        return message_dict

@router.post("/executive-summary")
async def get_exec_summary(
    assets: UploadFile | None = File(None)
):
        if not assets:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )
        
        if os.path.exists(f'./cached_pdfs/{assets.filename}.pkl'):
            print('Found the PDF analysis << --')
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'rb') as file:
                chunks = pickle.load(file)
        else:
            chunker = PDFChunker(overlap_percentage=0.2)
            # Process the PDF from bytes
            chunks = chunker.process_pdf(await assets.read(), extract_tables=True)
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'wb') as file:
                pickle.dump(chunks, file)
        
        # Convert chunks to JSON-serializable format
        data = "Given below is the data of a Lease PDF"
        for i, chunk in enumerate(chunks):
            data += f"""
            
                Details about Page number {str(i)}
                "chunk_id": {chunk.chunk_id},
                "page_number": {chunk.page_number},
                "text": {chunk.original_page_text},
                "previous_overlap": {chunk.previous_overlap},
                "next_overlap": {chunk.next_overlap},
                "overlap_info": {chunk.overlap_info}
            
            """
            
        documents = content_from_doc([4, 5])
        field_defintions: str= documents[0]
        system: str = documents[1]
        system_prompt = system.format(reference = field_defintions, JSON_STRUCTURE = json.dumps(executive_summary.structure))
               
        payload = [
            {
                "role": "system", "content": system_prompt  # will be filled by Ashruth 
            },
            {
                "role": "user", "content": data
            }
        ]
        
        response = llm_adapter.get_non_streaming_response(payload)

        message_content = response.choices[0].message.content

        try:
            message_dict = json.loads(message_content)
        except json.JSONDecodeError:
            try:
                # Handle single-quoted Python-style dicts
                message_dict = ast.literal_eval(message_content)
            except (ValueError, SyntaxError):
                # Fallback — wrap raw content
                message_dict = {"content": message_content}

        return message_dict
     
@router.post("/audit")
async def get_audit_details(
    assets: UploadFile | None = File(None)
):
        if not assets:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )
        
        if os.path.exists(f'./cached_pdfs/{assets.filename}.pkl'):
            print('Found the PDF analysis << --')
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'rb') as file:
                chunks = pickle.load(file)
        else:
            chunker = PDFChunker(overlap_percentage=0.2)
            # Process the PDF from bytes
            chunks = chunker.process_pdf(await assets.read(), extract_tables=True)
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'wb') as file:
                pickle.dump(chunks, file)
        
        # Convert chunks to JSON-serializable format
        data = "Given below is the data of a Lease PDF"
        for i, chunk in enumerate(chunks):
            data += f"""
            
                Details about Page number {str(i)}
                "chunk_id": {chunk.chunk_id},
                "page_number": {chunk.page_number},
                "text": {chunk.original_page_text},
                "previous_overlap": {chunk.previous_overlap},
                "next_overlap": {chunk.next_overlap},
                "overlap_info": {chunk.overlap_info}
            
            """
               
        payload = [
            {
                "role": "system", "content": audit.system + """ Output format is as follows """ + json.dumps(audit.output_schema) 
            },
            {
                "role": "user", "content": data + """Critically analyze the provided Lease Agreement by comparing clauses and identifying all terms that are ambiguous, 
                    rely on subjective future agreement, contain internal conflicts, or represent significant, unquantified financial/operational 
                    risks for the Tenant. Every identified point must be supported by direct citations.
                    Finally make sure to provide all the Tabled and bulleted risk register with verbatim citations for every point."""
            }
        ]
        
        response = llm_adapter.get_non_streaming_response(payload)

        message_content = response.choices[0].message.content

        try:
            message_dict = json.loads(message_content)
        except json.JSONDecodeError:
            try:
                # Handle single-quoted Python-style dicts
                message_dict = ast.literal_eval(message_content)
            except (ValueError, SyntaxError):
                # Fallback — wrap raw content
                message_dict = {"content": message_content}

        return message_dict
  
@router.post('/save')
async def save_lease(item: SaveZod):
    lease_abstract = item.lease_abstract 
    filename = item.filename
    lease_abstraction_json = json.dumps(lease_abstract)
    with open(f'./results/{filename}.json', 'w') as f:
        json.dump(lease_abstraction_json, f, indent=4) 

@router.post('/cam')
async def get_cam(
    assets: UploadFile 
):
    if not assets:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )
        
    if os.path.exists(f'./cached_pdfs/{assets.filename}.pkl'):
        print('Found the PDF analysis << --')
        with open(f'./cached_pdfs/{assets.filename}.pkl', 'rb') as file:
            chunks = pickle.load(file)
    else:
        chunker = PDFChunker(overlap_percentage=0.2)
        # Process the PDF from bytes
        chunks = chunker.process_pdf(await assets.read(), extract_tables=True)
        with open(f'./cached_pdfs/{assets.filename}.pkl', 'wb') as file:
            pickle.dump(chunks, file)
    
    # Convert chunks to JSON-serializable format
    data = "Given below is the data of a Lease PDF"
    for i, chunk in enumerate(chunks):
        data += f"""
        
            Details about Page number {str(i)}
            "chunk_id": {chunk.chunk_id},
            "page_number": {chunk.page_number},
            "text": {chunk.original_page_text},
            "previous_overlap": {chunk.previous_overlap},
            "next_overlap": {chunk.next_overlap},
            "overlap_info": {chunk.overlap_info}
        
        """
        
    documents = content_from_doc([7, 7])
    field_defintions: str= documents[0]
    system: str = documents[1]
    
    system_prompt = system.format(reference = cam.field_definitions, JSON_STRUCTURE = json.dumps(cam.structure))
            
    payload = [
        {
            "role": "system", "content": system_prompt  # will be filled by Ashruth 
        },
        {
            "role": "user", "content": data
        }
    ]

    response = llm_adapter.get_non_streaming_response(payload)

    message_content = response.choices[0].message.content

    try:
        message_dict = json.loads(message_content)
    except json.JSONDecodeError:
        try:
            # Handle single-quoted Python-style dicts
            message_dict = ast.literal_eval(message_content)
        except (ValueError, SyntaxError):
            # Fallback — wrap raw content
            message_dict = {"content": message_content}

    return message_dict

@router.post('/cam-single')
async def get_cam(
    assets: UploadFile 
):
    if not assets:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )
        
    if os.path.exists(f'./cached_pdfs/{assets.filename}.pkl'):
        print('Found the PDF analysis << --')
        with open(f'./cached_pdfs/{assets.filename}.pkl', 'rb') as file:
            chunks = pickle.load(file)
    else:
        chunker = PDFChunker(overlap_percentage=0.2)
        # Process the PDF from bytes
        chunks = chunker.process_pdf(await assets.read(), extract_tables=True)
        with open(f'./cached_pdfs/{assets.filename}.pkl', 'wb') as file:
            pickle.dump(chunks, file)
    
    # Initialize empty result dictionary for iterative updates
    message_dict = {}
    # Process each chunk iteratively
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)} - Page {chunk.page_number}")
        if i > 0:
            time.sleep(2)
        # Create data for this specific chunk
        chunk_data = f"""
        Here is the content from page {chunk.page_number} of the lease document:
        
        Page number: {chunk.page_number}
        Text content: {chunk.original_page_text}
        Previous overlap: {chunk.previous_overlap}
        Next overlap: {chunk.next_overlap}
        Overlap info: {chunk.overlap_info}
        """
        # try:
        documents = content_from_doc([6, 7])
        field_defintions: str= documents[0]
        system: str = documents[1]
    # Prepare system prompt for CAM analysis
        system_prompt = system
                
        payload = [
            {
                "role": "system", "content": system_prompt + cam.JSON_PROD_INSTRUCTIONS
            },
            {
                "role": "user", "content": chunk_data
            }
        ]
        
        # Get LLM response for this chunk
        

        # Update the result dictionary with this chunk's response
        try:
            response = llm_adapter.get_non_streaming_response(payload)
            message_content = response.choices[0].message.content
            message_dict = update_result_json(message_dict, message_content)

        except Exception as e:
            # print(response)
            print(f"Error processing chunk {i+1}: {str(e)}")
            # Continue with next chunk even if this one fails
            continue
        # except Exception as e:
        #     print(e)
        #     print('this was the error')

    return message_dict


@router.post("/amendments")
async def amendment_analysis(
    assets: UploadFile | None = File(None)
):
    try:
        if not assets:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )

        if os.path.exists(f'./cached_pdfs/{assets.filename}.pkl'):
            print('Found the PDF analysis << --')
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'rb') as file:
                chunks = pickle.load(file)
        else:
            chunker = PDFChunker(overlap_percentage=0.2)
            # Process the PDF from bytes
            chunks = chunker.process_pdf(await assets.read(), extract_tables=True)
            with open(f'./cached_pdfs/{assets.filename}.pkl', 'wb') as file:
                pickle.dump(chunks, file)
        
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
        
        resultant_filename = str(assets.filename).split(" amendment")[0] + ".pdf.json"
        path_to_json = f"./results/{resultant_filename}"
        if not os.path.exists(path_to_json):
            return {}
        
        with open(path_to_json, "r") as file:
            lease_output = json.load(file)
            
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
        

        try:
            message_dict = json.loads(message_content)
        except json.JSONDecodeError:
            try:
                # Handle single-quoted Python-style dicts
                message_dict = ast.literal_eval(message_content)
            except (ValueError, SyntaxError):
                # Fallback — wrap raw content
                message_dict = {"content": message_content}

        return message_dict
        
    except Exception as error:
        logger.error(error)
        return JSONResponse(
            content={
                "message": "Something went wrong, please contact support@stealth.com"
            },
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )