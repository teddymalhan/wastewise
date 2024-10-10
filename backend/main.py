import os
from fastapi import FastAPI, HTTPException, requests
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from model.garbage_model import classify_object  # Reusing your existing function
from typing import Dict
import openai
import boto3
from botocore.exceptions import NoCredentialsError
from openai import OpenAI
from fastapi import FastAPI, File, UploadFile, HTTPException
from dotenv import load_dotenv

# Initialize the FastAPI app
app = FastAPI()
load_dotenv()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


R2_ENDPOINT_URL = "https://22cd0c0ab575858f5c908a2265cf8fd6.r2.cloudflarestorage.com/image-pipeline"
R2_PUBLIC_URL = "https://pub-9521fd3eff274d20a3f9da1ab742e301.r2.dev"
R2_BUCKET_NAME = "image-pipeline"
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
R2_REGION = "wnam"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai = OpenAI(api_key=OPENAI_API_KEY)

s3_client = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT_URL,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    region_name=R2_REGION,
)


@app.post("/upload/")
async def upload_and_detect_and_run_model_and_response(file: UploadFile = File(...)):
    """
    Upload an image to the R2 endpoint.
    """
    print(f"File uploaded: {file.filename}")    
    if not os.path.exists("images"):
        os.makedirs("images")
    
    file_path = f"images/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # print(f"File saved: {file_path}")

    s3_client.upload_file(file_path, R2_BUCKET_NAME, file.filename)
    # print(f"File uploaded to R2: {file.filename}")
    # Save the image to the R2 endpoint
    image_url = f"{R2_PUBLIC_URL}/{R2_BUCKET_NAME}/{file.filename}"
    # print(f"File uploaded Successfully: {image_url}")
 
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image? I want to detect it for the purpose of sorting it for garbage. Reply in a word or two. Please do not write anything else. It is very important that you only write the object name."},
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                    },
                ],
                }
            ],
            max_tokens=300,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in GPT-4 Vision call: {str(e)}")

    result = response.choices[0].message.content

    return classify_object(result)
    


# Run the FastAPI app with Uvicorn if this script is executed as the main program
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
