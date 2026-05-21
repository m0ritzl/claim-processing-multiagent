# Quickstart: Microsoft Agent Framework Migration

**Feature**: 001-migrate-ms-agents  
**Date**: 2026-01-17

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Azure OpenAI resource with a deployed model (default: gpt-5.3-chat)
- Azure CLI authenticated (`az login`) with access to the Azure OpenAI resource

## Environment Setup

### 1. Clone and checkout the feature branch

```bash
cd /path/to/simple-insurance-multi-agent
git checkout 001-migrate-ms-agents
```

### 2. Install dependencies

```bash
cd backend
uv sync
```

### 3. Configure environment variables

Create or update `.env` in the `backend/` directory:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5.3-chat
AZURE_OPENAI_API_VERSION=preview
AZURE_OPENAI_DEPLOYMENTS_API_VERSION=2024-10-21

# Authentication uses DefaultAzureCredential.
# Run `az login` locally; managed identity is used in Azure.
```

## Running the Backend

### Development server

```bash
cd backend
uv run python -m app.main
```

The API will be available at `http://localhost:8000`.

### Verify the migration

1. **Health check**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **List sample claims**:
   ```bash
   curl http://localhost:8000/api/v1/workflow/sample-claims
   ```

3. **Process a claim**:
   ```bash
   curl -X POST http://localhost:8000/api/v1/workflow/run \
     -H "Content-Type: application/json" \
     -d '{"claim_id": "CLM-2026-001"}'
   ```

4. **Test individual agent**:
   ```bash
   curl -X POST http://localhost:8000/api/v1/agent/claim_assessor/run \
     -H "Content-Type: application/json" \
     -d '{"claim_id": "CLM-2026-001"}'
   ```

## Running Tests

```bash
cd backend
uv run pytest
```

### Run specific test categories

```bash
# Unit tests
uv run pytest tests/unit/

# Integration tests (requires Azure OpenAI)
uv run pytest tests/integration/

# Test with verbose output
uv run pytest -v --tb=short
```

## Running the Frontend

The frontend requires no changes for this migration.

```bash
cd frontend
npm install
npm run dev
```

Access the UI at `http://localhost:3000`.

## Verifying the Migration

### Expected behavior parity

| Scenario | Expected Result |
|----------|-----------------|
| Process claim via API | Returns same JSON structure with `conversation_grouped`, `conversation_chronological`, `decision`, `confidence` |
| Individual agent invocation | Returns agent output with same format |
| Frontend workflow visualization | Shows agent progression in real-time |
| Missing Azure OpenAI | Falls back to mock responses |

### Key files changed

```
backend/
├── pyproject.toml                      # Dependencies updated
├── app/workflow/
│   ├── supervisor.py                   # MS Agent Framework orchestration
│   ├── registry.py                     # Agent registration
│   ├── tools.py                        # Tool signatures updated
│   └── agents/
│       ├── claim_assessor.py           # Agent factory
│       ├── policy_checker.py           # Agent factory
│       ├── risk_analyst.py             # Agent factory
│       └── communication_agent.py      # Agent factory
└── app/services/
    └── single_agent.py                 # Single agent invocation
```

### Files unchanged (verify no modifications)

```
backend/app/api/v1/endpoints/workflow.py   # API contract preserved
backend/app/api/v1/endpoints/agent.py      # API contract preserved
backend/app/models/                        # Data models unchanged
frontend/                                  # No frontend changes
```

## Troubleshooting

### "Module not found: agent_framework"

```bash
cd backend
uv sync  # Re-sync dependencies
```

### "Azure OpenAI authentication failed"

Run `az login` and ensure the logged-in user or managed identity has the `Cognitive Services OpenAI User` role.

### "Streaming not working"

Check that the workflow is using async iteration:
```python
async for event in workflow.run_stream(task=...):
    ...
```

### "Tool not being called"

Verify tool function has:
- Type hints with `Annotated[type, Field(description=...)]`
- A docstring describing the function
- Correct return type annotation

## Performance Comparison

After migration, compare performance:

```bash
# Time a claim processing request
time curl -X POST http://localhost:8000/api/v1/workflow/run \
  -H "Content-Type: application/json" \
  -d '{"claim_id": "CLM-2026-001"}'
```

Expected: Within ±10% of previous LangGraph implementation.
