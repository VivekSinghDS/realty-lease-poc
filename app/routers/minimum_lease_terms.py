import base64
import json 
import os 
from http import HTTPStatus
from fastapi import (
    APIRouter,
    BackgroundTasks,
    File,
    UploadFile,
)
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from utils.helpers import save_response_to_file
from utils.logs import logger
from utils.helpers import get_llm_adapter
from utils.prompts import LEASE_ANALYSIS
load_dotenv()
router = APIRouter()

llm_adapter = get_llm_adapter()

@router.post("")
async def get_minimum_lease_terms(
    background_task: BackgroundTasks,
    asset: UploadFile | None = File(None),
):
    try:
        if not asset:
            return JSONResponse(
                content={"error": {"asset": "is invalid"}}, status_code=HTTPStatus.BAD_REQUEST.value
            )
        data = await asset.read()
        base64_string = base64.b64encode(data).decode("utf-8")
        
        with open("./utils/references/original_lease_data.json") as file:
            original_lease_data_template = json.load(file)
            
        payload = [
            {"role": "system", "content": LEASE_ANALYSIS['system'].format(JSON_STRUCTURE = json.dumps(original_lease_data_template))},
            {
                "role": "user", "content": 
                [
                    {
                        "type": "input_file", 
                        "filename": "draconomicon.pdf",
                        "file_data": f"data:application/pdf;base64,{base64_string}"
                    },
                    {
                        "type": "input_text", 
                        "text": LEASE_ANALYSIS['user']
                    }
                ]
            }
        ]
        print(payload[0]['content'])
        response = llm_adapter.get_non_streaming_response(payload)
        
        background_task.add_task(
            save_response_to_file, 
            response.output_text, 
            str(asset.filename)
        )
        return response.output_text

        
    except Exception as error:
        logger.error(error)
        return JSONResponse(
                content={
                    "message": "Something went wrong, please contact support@stealth.com"
                }, status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value
            )
    

