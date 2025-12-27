import dotenv
from fastapi import FastAPI, HTTPException

from .models import QARequest, QAResponse
from .services import process_rag_query

dotenv.load_dotenv()

app = FastAPI()


@app.post("/rag-query", response_model=QAResponse)
async def query_endpoint(request: QARequest):
    try:
        return await process_rag_query(request.question, request.document_text)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occured during RAG processing: {str(e)}"
        )


@app.get("/")
async def root():
    return {"service": "RAG Expert", "status": "running", "endpoints": ["/rag-query"]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
