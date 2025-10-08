import base64
import re
import json 
import os 
from http import HTTPStatus
from typing import Any
from fastapi import (
    APIRouter,
    File,
    UploadFile,
)
from dotenv import load_dotenv
from fastapi.responses import JSONResponse, StreamingResponse
from utils.logs import logger
from utils.helpers import content_from_doc, get_llm_adapter, update_result_json
from utils.prompts import LEASE_ANALYSIS, LEASE_INFORMATION
from utils.references import charge_schedules, leaseInformation, otherLeaseProvisions, space, updated_lease_abstraction
# from utils.prompts import AMENDMENT_ANALYSIS
load_dotenv()
router = APIRouter()

llm_adapter = get_llm_adapter()


@router.post("/executive-summary")
async def executive_summary_analysis(
    assets: UploadFile | None = File(None)
):
    try:
        if not assets:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )
        
        with open("./utils/references/executive_summary.json") as file:
            original_lease_data_template = json.load(file)
            
        data = await assets.read()
        
        original_filename = assets.filename or "uploaded_file"
        base64_string = base64.b64encode(data).decode("utf-8")
        
        documents = content_from_doc([4, 5])
        field_defintions: str= documents[0]
        system: str = documents[1]
        system_prompt = system.format(reference = field_defintions, JSON_STRUCTURE = json.dumps(original_lease_data_template))
        
        payload = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user", "content": 
                [
                    {
                        "type": "input_file", 
                        "filename": original_filename,
                        "file_data": f"data:application/pdf;base64,{base64_string}"
                    },
                    {
                        "type": "input_text", 
                        "text": LEASE_ANALYSIS['user']
                    },
                    {
                        "type": "input_text",
                        "text": "THIS IS GOOD BUT MAKE SURE THE OUTPUT IS A VALID JSON"
                    }
                ]
            }
        ]
        response = llm_adapter.get_non_streaming_response(payload)
        return json.loads(response.output_text)

        
    except Exception as error:
        logger.error(error)
        return JSONResponse(
                content={
                    "message": "Something went wrong, please contact support@stealth.com"
                }, status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value
            )
    

@router.post("/info")
async def get_lease_info(
    assets: UploadFile = File(None)
):
    # try:
            
        data = await assets.read()
        original_filename = assets.filename or "uploaded_file"
        base64_string = base64.b64encode(data).decode("utf-8")
        documents = content_from_doc([0, 5])
        field_defintions: str= documents[0]
        system: str = documents[1]
        system_prompt = system.format(reference = field_defintions, JSON_STRUCTURE = json.dumps(leaseInformation.structure))
        
        payload = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user", "content": 
                [
                    {
                        "type": "input_file", 
                        "filename": original_filename,
                        "file_data": f"data:application/pdf;base64,{base64_string}"
                    },
                    {
                        "type": "input_text", 
                        "text": LEASE_ANALYSIS['user']
                    },
                    {
                        "type": "input_text",
                        "text": "THIS IS GOOD BUT MAKE SURE THE OUTPUT IS A VALID JSON"
                    }
                ]
            }
        ]
        response_stream = llm_adapter.get_non_streaming_response(payload)
        return json.loads(response_stream.output_text)

    
@router.post("/space")
async def get_space_info(
    assets: UploadFile | None = File(None)
):
    try:
        if not assets:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )
            
        data = await assets.read()
        original_filename = assets.filename or "uploaded_file"
        base64_string = base64.b64encode(data).decode("utf-8")
        
        documents = content_from_doc([1, 5])
        field_defintions: str= documents[0]
        system: str = documents[1]
        system_prompt = system.format(reference = field_defintions, JSON_STRUCTURE = json.dumps(space.structure))
        
        payload = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user", "content": 
                [
                    {
                        "type": "input_file", 
                        "filename": original_filename,
                        "file_data": f"data:application/pdf;base64,{base64_string}"
                    },
                    {
                        "type": "input_text", 
                        "text": LEASE_ANALYSIS['user']
                    },
                    {
                        "type": "input_text",
                        "text": "THIS IS GOOD BUT MAKE SURE THE OUTPUT IS A VALID JSON"
                    }
                ]
            }
        ]
        
        response = llm_adapter.get_non_streaming_response(payload)
        return json.loads(response.output_text)
        
    except Exception as error:
        logger.error(error)
        return JSONResponse(
                content={
                    "message": "Something went wrong, please contact support@stealth.com"
                }, status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value
            )

    
@router.post("/charge-schedules")
async def get_charge_schedules(
    assets: UploadFile | None = File(None)
):
    try:
        if not assets:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )
            
        data = await assets.read()
        original_filename = assets.filename or "uploaded_file"
        base64_string = base64.b64encode(data).decode("utf-8")
        documents = content_from_doc([2, 5])
        field_defintions: str= documents[0]
        system: str = documents[1]
        system_prompt = system.format(reference = field_defintions, JSON_STRUCTURE = json.dumps(charge_schedules.structure))
        
        
        payload = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user", "content": 
                [
                    {
                        "type": "input_file", 
                        "filename": original_filename,
                        "file_data": f"data:application/pdf;base64,{base64_string}"
                    },
                    {
                        "type": "input_text", 
                        "text": LEASE_ANALYSIS['user']
                    },
                    {
                        "type": "input_text",
                        "text": "THIS IS GOOD BUT MAKE SURE THE OUTPUT IS A VALID JSON"
                    }
                ]
            }
        ]
        response = llm_adapter.get_non_streaming_response(payload)
        return json.loads(response.output_text)
    
    except Exception as error:
        logger.error(error)
        return JSONResponse(
                content={
                    "message": "Something went wrong, please contact support@stealth.com"
                }, status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value
            )
        
@router.post("/miscellaneous")
async def get_miscellaneous_info(
    assets: UploadFile | None = File(None)
):
    try:
        if not assets:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )
            
        data = await assets.read()
        original_filename = assets.filename or "uploaded_file"
        base64_string = base64.b64encode(data).decode("utf-8")
        documents = content_from_doc([3, 5])
        field_defintions: str= documents[0]
        system: str = documents[1]
        system_prompt = system.format(reference = field_defintions, JSON_STRUCTURE = json.dumps(otherLeaseProvisions.structure))
        
        
        payload = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user", "content": 
                [
                    {
                        "type": "input_file", 
                        "filename": original_filename,
                        "file_data": f"data:application/pdf;base64,{base64_string}"
                    },
                    {
                        "type": "input_text", 
                        "text": LEASE_ANALYSIS['user']
                    },
                    {
                        "type": "input_text",
                        "text": "THIS IS GOOD BUT MAKE SURE THE OUTPUT IS A VALID JSON"
                    }
                ]
            }
        ]
        response = llm_adapter.get_non_streaming_response(payload)
        return json.loads(response.output_text)

    except Exception as error:
        logger.error(error)
        return JSONResponse(
                content={
                    "message": "Something went wrong, please contact support@stealth.com"
                }, status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value
            )

@router.post("/general")
async def get_general_info(
    assets: UploadFile | None = File(None)
):
    try:
        if not assets:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )
            
        data = await assets.read()
        original_filename = assets.filename or "uploaded_file"
        base64_string = base64.b64encode(data).decode("utf-8")
        payload = [
            {"role": "system", "content": LEASE_ANALYSIS['system'].format(JSON_STRUCTURE = json.dumps(updated_lease_abstraction.structure), DOCUMENT_NAME = original_filename, reference = None)},
            {
                "role": "user", "content": 
                [
                    {
                        "type": "input_file", 
                        "filename": original_filename,
                        "file_data": f"data:application/pdf;base64,{base64_string}"
                    },
                    {
                        "type": "input_text", 
                        "text": LEASE_ANALYSIS['user']
                    },
                    {
                        "type": "input_text",
                        "text": "THIS IS GOOD BUT MAKE SURE THE OUTPUT IS A VALID JSON"
                    }
                ]
            }
        ]
        response = llm_adapter.get_non_streaming_response(payload)
        return json.loads(response.output_text)

    except Exception as error:
        logger.error(error)
        return JSONResponse(
                content={
                    "message": "Something went wrong, please contact support@stealth.com"
                }, status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value
            )
     

@router.post("/amendment-analysis")
async def amendment_analysis(
    amendment: UploadFile | None = File(None)
):
    try:
        # step 1: accept multipart pdf named 'amendment'
        if not amendment:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )

        # step 2: compare amendment filename to existing fileid directories
        original_filename = amendment.filename or "uploaded_file.pdf"
        base_name = os.path.splitext(os.path.basename(original_filename))[0]

        # First try name-only matching: extract leading alphabetic name (e.g., "Bayer")
        name_match = re.match(r"\s*([A-Za-z]+)", base_name or "")
        candidate_dir = None
        candidate_fileid = None
        if name_match:
            name_key = name_match.group(1).lower()
            try:
                dirs = [d for d in os.listdir(".") if os.path.isdir(os.path.join(".", d))]
                # Prefer directories starting with the name; fallback to containing the name
                starts_with = [d for d in dirs if d.lower().startswith(name_key)]
                contains = [d for d in dirs if (name_key in d.lower())]
                chosen = starts_with[0] if starts_with else (contains[0] if contains else None)
                if chosen:
                    candidate_dir = os.path.join(".", chosen)
                    candidate_fileid = chosen
            except Exception:
                pass

        # If no name-only match , return the no-matches-found response
        if not candidate_dir:
            return JSONResponse(
                content={"message": "Please provide original lease first. Original abstraction unavailable."},
                status_code=HTTPStatus.NOT_FOUND.value,
            )

        # step 3: if directory somehow missing, return specified response
        if not os.path.isdir(candidate_dir):
            return JSONResponse(
                content={"message": "Please provide original lease first. Original abstraction unavailable."},
                status_code=HTTPStatus.NOT_FOUND.value,
            )

        # Match exists: load latest original lease JSON (original_lease.json or original_lease_<x>.json)
        pattern = re.compile(r"^(?:original|orignal)_lease(?:_(\d+))?\.json$", re.IGNORECASE)
        versions = []
        try:
            for name in os.listdir(candidate_dir):
                match = pattern.match(name)
                if match:
                    version = int(match.group(1)) if match.group(1) else 0
                    versions.append((version, name))
        except Exception:
            versions = []

        if not versions:
            return JSONResponse(
                content={
                    "message": "Original abstraction files not found in matched directory.",
                    "fileid": candidate_fileid,
                },
                status_code=HTTPStatus.NOT_FOUND.value,
            )

        versions.sort(key=lambda x: x[0])
        latest_version, latest_file = versions[-1]
        latest_path = os.path.join(candidate_dir, latest_file)

        input_json = None
        try:
            with open(latest_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
            try:
                input_json = json.loads(raw_text)
            except Exception:
                input_json = raw_text
        except Exception:
            input_json = None
        # Read amendment file and create base64 for the payload
        data = await amendment.read()
        base64_string = base64.b64encode(data).decode("utf-8")
        amendment_filename = amendment.filename or "amendment.pdf"

        # Load schema for amendment analysis as JSON_STRUCTURE
        with open("./utils/references/lease_abstraction.json") as file:
            original_lease_data_template = json.load(file)

        payload = [
            {"role": "system", "content": AMENDMENT_ANALYSIS['system'].format(INPUT_JSON = json.dumps(input_json), JSON_STRUCTURE = json.dumps(original_lease_data_template), DOCUMENT_NAME = amendment_filename)},
            {
                "role": "user", "content": 
                [
                    {
                        "type": "input_file", 
                        "filename": amendment_filename,
                        "file_data": f"data:application/pdf;base64,{base64_string}"
                    },
                    {
                        "type": "input_text", 
                        "text": AMENDMENT_ANALYSIS['user']
                    }
                ]
            }
        ]
        
        print(payload[0]['content'])
        print('i got here')
        print('streaming start')
        response = llm_adapter.get_non_streaming_response(payload)
        full_text_response = response.output_text
        # for event in response:
        #     if event.type == "response.output_text.delta":
        #         full_text_response+= event.delta
        #         print(event.delta, end="", flush=True)
        #     elif event.type == "response.completed":
        #         print()  # finish with a newline        # Store the response as the next version: original_lease_<x>.json
        try:
            next_version = (max(v for v, _ in versions) + 1) if versions else 0
            new_output_path = os.path.join(candidate_dir, f"original_lease_{next_version}.json")
            result_text = full_text_response 
            
            try:
                parsed_json = json.loads(result_text)
                with open(new_output_path, "w", encoding="utf-8") as out_file:
                    json.dump(parsed_json, out_file, ensure_ascii=False, indent=2)
                return parsed_json

            except json.JSONDecodeError:
                # Try to recover by extracting content between first { and last }
                first_open = result_text.find('{')
                last_close = result_text.rfind('}')
                json_substring = result_text[first_open:last_close]
                parsed_json = json.loads(json_substring)
                # if first_open != -1 and last_close != -1 and first_open < last_close:
                #     json_substring = result_text[first_open:last_close + 1]
                #     print('json substring here --->>> ')
                #     print(json_substring)
                #     try:
                #         parsed_json = json.loads(json_substring)
                #         with open(new_output_path, "w", encoding="utf-8") as out_file:
                #             json.dump(parsed_json, out_file, ensure_ascii=False, indent=2)
                #         return parsed_json
                #     except json.JSONDecodeError:
                #         print("Failed to parse even after trimming to JSON substring.")
                # else:
                #     print("Could not find valid JSON boundaries.")
                # with open(new_output_path, "w", encoding="utf-8") as out_file:
                #     out_file.write(result_text)
        except Exception as write_error:
            logger.error(write_error)

        # Return the model output directly, consistent with get_lease_abstraction
        return {}
    except Exception as error:
        logger.error(error)
        return JSONResponse(
            content={
                "message": "Something went wrong, please contact support@stealth.com"
            },
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )