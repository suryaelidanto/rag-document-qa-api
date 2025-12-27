import os
import time
from typing import List

from openai import AsyncOpenAI

from .models import QAResponse

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_CHUNK_SIZE = 2000
MODEL_NAME = "gpt-4o-mini"


def chunk_document(text: str, max_size: int = MAX_CHUNK_SIZE) -> List[str]:
    """
    Splits long text documents into smaller, managable chunks. This helps in fitting content within LLM context limits.
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


async def process_rag_query(question: str, document_text: str):
    """
    Handles the end-to-end RAG flow:
    1. Chunks the document
    2. Constructs the prompt
    3. Fetches the answer form OpenAI
    """

    start_time = time.time()

    chunks = chunk_document(document_text)
    context = "\n\n".join(chunks)

    system_prompt = (
        "You are a professional assistant."
        "Answer questions based ONLY on the provided document context."
        "If the information is not present, state that you cannot find it."
    )

    user_prompt = f"Document Context:\n{context}\n\nUser Question: {question}"

    response = await client.chat.completions.create(
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

    processing_time_ms = int((time.time() - start_time) * 1000)

    answer = response.choices[0].message.content

    return QAResponse(
        answer=answer, chunks_used=len(chunks), processing_time_ms=processing_time_ms
    )
