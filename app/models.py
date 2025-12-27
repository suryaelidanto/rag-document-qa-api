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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "Who is the CEO of ExampleCorp?",
                    "document_text": "ExampleCorp is a tech company founded in 2020. The CEO is John Doe.",
                }
            ]
        }
    }


class QAResponse(BaseModel):
    answer: str = Field(..., description="The AI-generated answer")
    chunks_used: int = Field(..., description="Number of text chunks processed")
    processing_time_ms: int = Field(..., description="Total time taken in milliseconds")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "answer": "The CEO of ExampleCorp is John Doe.",
                    "chunks_used": 1,
                    "processing_time_ms": 1150,
                }
            ]
        }
    }
