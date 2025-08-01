
from fastapi import FastAPI, HTTPException, Query
import boto3
import os
import json
from dotenv import load_dotenv
import logging
from botocore.exceptions import BotoCoreError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve and validate AWS configuration from environment variables
AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
MODEL_ID = os.getenv("MODEL_ID")
KNOWLEDGE_BASE_ID = os.getenv("OR2VV9ZQBY")
MODEL_ARN = os.getenv("meta.llama3-3-70b-instruct-v1:0")

# Validate mandatory environment variables
if not AWS_REGION:
    raise ValueError("AWS_REGION environment variable is missing.")

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "FastAPI is running!"}

# Initialize AWS clients once during application startup
try:
    bedrock_client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    bedrock_agent_client = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)
except (BotoCoreError, ClientError) as e:
    logger.error(f"Failed to initialize AWS clients: {e}")
    raise

@app.get("/bedrock/invoke")
async def invoke_model(text: str = Query(..., description="Input text for the model")):
    """
    Endpoint for invoking the Llama 3 model.
    """
    if not MODEL_ID:
        raise HTTPException(status_code=500, detail="MODEL_ID is not configured.")
    
    try:
        # Format the prompt according to Llama 3's requirements
        formatted_prompt = f"""
        <|begin_of_text|><|start_header_id|>user<|end_header_id|>
        {text}
        <|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
        """

        # Construct the request payload
        request_payload = {
            "prompt": formatted_prompt,
            "max_gen_len": 512,
            "temperature": 0.5
        }

        # Invoke the model
        response = bedrock_client.invoke_model(
            modelId=MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_payload)
        )

        # Read and parse the response body
        response_body = json.loads(response['body'].read().decode('utf-8'))

        # Extract the generated text
        generated_text = response_body.get("generation", "")

        if not generated_text:
            logger.error("Model did not return any content.")
            raise HTTPException(status_code=500, detail="Model did not return any content.")
        
        return {"response": generated_text}
    except ClientError as e:
        logger.error(f"AWS ClientError: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"AWS ClientError: {e.response['Error']['Message']}")
    except BotoCoreError as e:
        logger.error(f"AWS BotoCoreError: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="AWS BotoCore error occurred.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")



@app.get("/bedrock/query")
async def query_with_knowledge_base(text: str = Query(..., description="Input text for the model")):
    """
    Endpoint for model invocation with knowledge base retrieval and generation.
    """
    if not KNOWLEDGE_BASE_ID or not MODEL_ARN:
        raise HTTPException(status_code=500, detail="Knowledge base configuration is missing.")
    
    try:
        response = bedrock_agent_client.retrieve_and_generate(
            input={"text": text},
            retrieveAndGenerateConfiguration={
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                    "modelArn": MODEL_ARN
                },
                "type": "KNOWLEDGE_BASE"
            }
        )
        return {"response": response["output"]["text"]}
    except ClientError as e:
        logger.error(f"AWS ClientError: {e}")
        raise HTTPException(status_code=500, detail="AWS Client error occurred.")
    except BotoCoreError as e:
        logger.error(f"AWS BotoCoreError: {e}")
        raise HTTPException(status_code=500, detail="AWS BotoCore error occurred.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
