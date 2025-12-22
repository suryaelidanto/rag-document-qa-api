# RAG Document QA API

Context-aware RAG API for document Q&A using GPT-4o with dynamic text chunking strategies.

## Setup

1. **Install Dependencies**
   ```bash
   uv sync
   ```

2. **Set OpenAI API Key**
   Create a `.env` file:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

## Running the Service

```bash
uv run uvicorn main:app --reload
```

Server runs at: `http://localhost:8000`

## API Endpoints

### GET / - Health Check

```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "service": "RAG Expert",
  "status": "running",
  "endpoints": ["/rag-query"]
}
```

### POST /rag-query - Ask Questions About Documents

**Request:**
```bash
curl -X POST http://localhost:8000/rag-query \
  -H "Content-Type: application/json" \
  -d '{
    "document_text": "ExampleCorp is a technology company founded in 2020. The CEO is John Doe. The company specializes in AI automation and has 50 employees.",
    "question": "Who is the CEO of ExampleCorp?"
  }'
```

**Response:**
```json
{
  "answer": "The CEO of ExampleCorp is John Doe.",
  "chunks_used": 1
}
```

### Example: Contract Analysis

**Request:**
```bash
curl -X POST http://localhost:8000/rag-query \
  -H "Content-Type: application/json" \
  -d '{
    "document_text": "INDEPENDENT CONTRACTOR AGREEMENT. This Agreement is entered into on December 21, 2025, between ExampleCorp.com (the Company) and Surya Elidanto (the Contractor). The Contractor shall provide services as an AI Software Engineer. The Company shall pay the Contractor a fixed monthly fee of $3,333.33 USD payable via Deel/Wise on the last day of each calendar month. This Agreement may be terminated by either party upon thirty (30) days written notice.",
    "question": "What is the monthly salary?"
  }'
```

**Response:**
```json
{
  "answer": "The monthly salary is $3,333.33 USD.",
  "chunks_used": 1
}
```

### Example: Information Not Found

**Request:**
```bash
curl -X POST http://localhost:8000/rag-query \
  -H "Content-Type: application/json" \
  -d '{
    "document_text": "ExampleCorp is a technology company founded in 2020. The CEO is John Doe.",
    "question": "What is the company revenue?"
  }'
```

**Response:**
```json
{
  "answer": "I cannot find this information in the document.",
  "chunks_used": 1
}
```

## How It Works

1. **Chunking**: Long documents are split into 2000-character chunks
2. **Context Building**: Chunks are combined into a single context
3. **AI Query**: OpenAI GPT-4o-mini answers based on the context
4. **Response**: Returns the answer with chunk count

## Use Cases

- Legal document Q&A (contracts, agreements)
- HR policy queries (employee handbooks, SOPs)
- Customer support (product manuals, FAQs)
- Research analysis (papers, reports)
