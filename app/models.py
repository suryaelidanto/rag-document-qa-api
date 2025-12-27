from pydantic import BaseModel, Field


class QARequest(BaseModel):
    question: str = Field(
        ...,
        min_length=5,
        description="The question user wants to ask based on the document",
    )
    document_text: str = Field(
        ...,
        min_length=10,
        description="The full text content of the document to be analyzed",
    )


class QAResponse(BaseModel):
    answer: str = Field(..., description="The AI-generated answer")
    chunks_used: int = Field(..., description="Number of text chunks processed")
    processing_time_ms: int = Field(..., description="Total time taken in milliseconds")
