import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
import ollama
from fastapi.middleware.cors import CORSMiddleware



load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

if not API_KEY:
    raise ValueError("No API key found. Please check your .env file.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#gemini things
class PromptRequest(BaseModel):
    prompt: str

class AIResponse(BaseModel):
    input_prompt: str
    generated_response: str

#for mistral7B
class MistralRequest(BaseModel):
    prompt: str

class MistralResponse(BaseModel):
    input_prompt: str
    generated_response: str

#llama3.3
class LlamaRequest(BaseModel):
    prompt: str

class LlamaResponse(BaseModel):
    input_prompt: str
    generated_response: str

#gpt2
class GPT2Request(BaseModel):
    prompt: str

class GPT2Response(BaseModel):
    input_prompt: str
    generated_response: str

@app.post("/gemini/", response_model=AIResponse)
async def generate_content(request: PromptRequest):
    try:
        response = model.generate_content(request.prompt)
        
        return {
            "input_prompt": request.prompt,
            "generated_response": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.post("/mistral/", response_model=MistralResponse)
async def generate_with_mistral(request: MistralRequest):
    try:
        HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
        if not HUGGINGFACE_API_KEY:
            raise ValueError("HuggingFace API key not configured")

        repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
        llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            max_length=128,
            temperature=0.7,
            api=HUGGINGFACE_API_KEY
        )

        response_text = llm.invoke(request.prompt)

        if not response_text:
            raise ValueError("No response generated by the model")

        return {
            "input_prompt": request.prompt,
            "generated_response": response_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/llama/", response_model=LlamaResponse)
async def generate_with_llama(request: LlamaRequest):
    try:
        HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
        if not HUGGINGFACE_API_KEY:
            raise ValueError("HuggingFace API key not configured")

        repo_id = "meta-llama/Llama-2-7b-chat-hf"
        llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            max_length=128,
            temperature=0.7,
            api=HUGGINGFACE_API_KEY,
        )

        response_text = llm.invoke(request.prompt)

        if not response_text:
            raise ValueError("No response generated by the model")

        return {
            "input_prompt": request.prompt,
            "generated_response": response_text,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    

@app.post("/gpt2/", response_model=GPT2Response)
async def generate_with_gpt2(request: GPT2Request):
    try:
        HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
        if not HUGGINGFACE_API_KEY:
            raise ValueError("HuggingFace API key not configured")

        repo_id = "gpt2"  # GPT-2 model from HuggingFace
        llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            max_length=128,
            temperature=0.7,
            api=HUGGINGFACE_API_KEY,
        )

        response_text = llm.invoke(request.prompt)
        if not response_text:
            raise ValueError("No response generated by the model")

        return {
            "input_prompt": request.prompt,
            "generated_response": response_text,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))