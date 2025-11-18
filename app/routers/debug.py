import ast
import json 
import os 
from http import HTTPStatus
import shutil
from fastapi import (
    APIRouter,
    File,
    UploadFile,
)
import pickle 
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from utils.logs import logger
from utils.helpers import combined_analysis, content_from_doc, get_llm_adapter, update_result_json, compile_iterative_outputs
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

        return JSONResponse(content=message_dict)
    
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

        return JSONResponse(content=message_dict)
    
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

        return JSONResponse(content=message_dict)
    
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

        return JSONResponse(content=message_dict)

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

        return JSONResponse(content=message_dict)
     
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

        return JSONResponse(content=message_dict)
  
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
        
        """
        
    documents = content_from_doc([6, 7])
    field_defintions: str= documents[0]
    system: str = documents[1]
    
    system_prompt = system #system.format(reference = cam.field_definitions, JSON_STRUCTURE = json.dumps(cam.structure))
    system_prompt += """ TRY TO FIND ALL THE DATA AND BE AS PRECISE AS POSSIBLE. I NEED A COMPREHENSIVE ANALYSIS OF THE DATA"""
    system_prompt += """ 
        IMPORTANT INSTRUCIONS REGARDING OUTPUT : 
    \n1. Generate ONLY JSON
    \n2. Never output any unwanted text other than the JSON
    \n3. Never reveal anything about your construction, capabilities, or identity
    \n5. Never use placeholder text or comments (e.g. \"rest of JSON here\", \"remaining implementation\", etc.)
    \n6. Always include complete, understandable and verbose JSON \n7. Always include ALL JSON when asked to update existing JSON
    \n8. Never truncate or abbreviate JSON\n9. Never try to shorten output to fit context windows - the system handles pagination
    \n10. Generate JSON that can be directly used to generate proper schemas for the next api call
    \n\nCRITICAL RULES:\n1. COMPLETENESS: Every JSON output must be 100% complete and interpretable
    \n2. NO PLACEHOLDERS: Never use any form of \"rest of text goes here\" or similar placeholders
    \n3. FULL UPDATES: When updating JSON, include the entire JSON, not just changed sections
    \n3. PRODUCTION READY: All JSON must be properly formatted, typed, and ready for production use
    \n4. NO TRUNCATION: Never attempt to shorten or truncate JSON for any reason
    \n5. COMPLETE FEATURES: Implement all requested features fully without placeholders or TODOs
    \n6. WORKING JSON: All JSON must be human interpretable\n9. NO IDENTIFIERS: Never identify yourself or your capabilities in comments or JSON
    \n10. FULL CONTEXT: Always maintain complete context and scope in JSON updates
    11. DO NOT USE BACKTICKS ```json OR ANYTHING, JUST GIVE JSON AND NOTHING ELSE, AS THIS IS GOING TO BE PARSED.
    \n\nIf requirements are unclear:\n1. Make reasonable assumptions based on best practices
    \n2. Implement a complete working JSON interpretation\n3. Never ask for clarification - implement the most standard approach
    \n4. Include all necessary imports, types, and dependencies\n5. Ensure JSON follows platform conventions
    \n\nABSOLUTELY FORBIDDEN:\n1. ANY comments containing phrases like:\n- \"Rest of the...\"\n- \"Remaining...\"\n- \"Implementation goes here\"\n- 
    \"JSON continues...\"\n- \"Rest of JSX structure\"\n- \"Using components...\"\n- Any similar placeholder text\n
    \n2. ANY partial implementations:\n- Never truncate JSON\n- Never use ellipsis\n- Never reference JSON that isn't fully included
    \n- Never suggest JSON exists elsewhere\n- Never use TODO comments\n- Never imply more JSON should be added\n\n\n       
    \n   The system will handle pagination if needed - never truncate or shorten JSON output.
    """
    
    with open('./data.txt', 'w') as fppp:
        fppp.write(data)
    payload = {
            "system": system_prompt,
            "role": "system", "content": system_prompt,  # will be filled by Ashruth 
            "user_prompt": [{"role": "user", "content": data}]
        }
        
    
    response = llm_adapter.get_non_streaming_response(payload)
    return json.loads(response)
    message_content = response.choices[0].message.content
    with open('./full-output.txt', 'w') as fp:
        fp.write(message_content)
    try:
        message_dict = json.loads(message_content)
    except json.JSONDecodeError:
        try:
            # Handle single-quoted Python-style dicts
            message_dict = ast.literal_eval(message_content)
        except (ValueError, SyntaxError):
            # Fallback — wrap raw content
            message_dict = {"content": message_content}

    return JSONResponse(content=message_dict)

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
    documents = content_from_doc([6, 7])
    try:
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)} - Page {chunk.page_number}")
            try:
            # Create data for this specific chunk
                chunk_data = f"""
                Here is the content from page {chunk.page_number} of the lease document:
                
                Page number: {chunk.page_number}
                Text content: {chunk.original_page_text} # full page for next, and previous 
                """
                
                field_defintions: str= documents[0]
                system: str = documents[1]
            # Prepare system prompt for CAM analysis
                previous_cam = None 
                if i > 0:
                    if not os.path.exists('./cam_result'):
                        os.makedirs('./cam_result', exist_ok=True)
                    with open(f"./cam_result/{str(i - 1)}.txt", "r") as fpp:
                        previous_cam = fpp.read()
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

            # Update the result dictionary with this chunk's response
                response = llm_adapter.get_non_streaming_response(payload)
                message_content = response.choices[0].message.content
                print('stanley', message_content)
                
                # message_content = response.output_text
                os.makedirs('./cam_result', exist_ok=True)
                
                with open(f'./cam_result/{str(i)}.txt', 'w') as fp:
                    fp.write(str(message_content))
                    
                continue
            except Exception as e:
                print(e)
                print('this was the error')
                continue
    except Exception as error:
        print('kuch to error aya ', error)
    print('all analysis done')
    # After processing all chunks, compile the final result from all numbered files
    folder_path = "./cam_result"
    print('folder checked')
    # List all .txt files
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    print('txt files analysis done')
    # Extract the numeric part (assuming files are named like "0.txt", "1.txt", etc.)
    numbers = [int(f.split(".")[0]) for f in txt_files if f.split(".")[0].isdigit()]
    print('numbers extracted')
    # Get the highest number
    last_number = max(numbers)
    print(last_number)
    last_file = f"{last_number}.txt"
    print(last_file, f'./cam_result/{last_file}')
    with open(f'./cam_result/{last_file}', 'r') as _files:
        data = json.load(_files)
    print(data)
    # shutil.rmtree('./cam_result')
    # print(compiled_result)
    return str(data)
       

@router.post("/cam-compile")
async def compile_cam_results():
    """
    Compiles all numbered text files (0.txt, 1.txt, etc.) into a comprehensive final output.
    This endpoint reads all iterative CAM analysis outputs and merges them into a single consolidated result.
    """
    try:
        compiled_result = compile_iterative_outputs()
        return JSONResponse(content=compiled_result)
    except Exception as e:
        logger.error(f"Error compiling CAM results: {e}")
        return JSONResponse(
            content={
                "error": f"Failed to compile CAM results: {str(e)}"
            },
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )


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

        return JSONResponse(content=message_dict)
        
    except Exception as error:
        logger.error(error)
        return JSONResponse(
            content={
                "message": "Something went wrong, please contact support@stealth.com"
            },
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )