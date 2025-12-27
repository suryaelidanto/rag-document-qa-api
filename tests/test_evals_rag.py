import pytest
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase
from app.services import process_rag_query


@pytest.mark.asyncio
async def test_rag_faithfulness():
    question = "What is the capital of Indonesia?"
    context = "Jakarta is the capital city of Indonesia."

    result = await process_rag_query(question, context)

    test_case = LLMTestCase(
        input=question, actual_output=result.answer, retrieval_context=[context]
    )

    metric = FaithfulnessMetric(threshold=0.7)
    metric.measure(test_case)

    assert metric.is_successful(), f"RAG is not faithful! Score: {metric.score}"
