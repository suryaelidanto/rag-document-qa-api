from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
from typing import List
import dotenv

dotenv.load_dotenv()

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_CHUNK_SIZE = 2000
MODEL_NAME = "gpt-4o-mini"


class RAGRequest(BaseModel):
    document_text: str
    question: str


class RAGResponse(BaseModel):
    answer: str
    chunks_used: int


def chunk_document(text: str, max_size: int = MAX_CHUNK_SIZE) -> List[str]:
    """
    Splits a long document into smaller chunks. This simulates what we did in pdf-cleaner project.
    """

    chunks = []
    words = text.split()
    current_chunk = []
    current_length = 0

    for word in words:
        word_length = len(word) + 1
        if current_length + word_length > max_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


@app.post("/rag-query", response_model=RAGResponse)
async def rag_query(request: RAGRequest):
    """
    RAG Flow:
    1. Chunk the document
    2. Build context from chunks
    3. Send to OpenAI with user question
    4. Return AI Answer
    """

    try:
        chunks = chunk_document(request.document_text)

        if not chunks:
            raise HTTPException(status_code=400, detail="Document is empty")

        context = "\n\n".join(chunks)

        system_prompt = """You are a helpful assistant that answers questions based ONLY on the provided document context.
        If the answer is not in the context, say 'I cannot find this information in the document.'
        """

        user_prompt = f"""Context from document: {context}
        Question: {request.question}
        Answer: 
        """

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )

        answer = response.choices[0].message.content

        return RAGResponse(answer=answer, chunks_used=len(chunks))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG processing failed: {str(e)}")


@app.get("/")
async def root():
    return {"service": "RAG Expert", "status": "running", "endpoints": ["/rag-query"]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
