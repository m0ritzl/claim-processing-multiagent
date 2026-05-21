# Insurance Multi-Agent Development Guidelines

Last updated: 2026-05-20

## Active Technologies

- Python 3.12 backend with FastAPI, Uvicorn, SQLAlchemy, Alembic, asyncpg, Microsoft Agent Framework (`agent-framework-core` + `agent-framework-openai`), Azure Identity, OpenAI SDK, LangChain vector-search packages, FAISS, and Pydantic Settings.
- TypeScript 6 frontend with Next.js 16, React 19, shadcn/ui/Radix UI, Tailwind CSS 4, TanStack Table, Recharts 3, Streamdown, and Zod 4.
- Azure infrastructure uses azd + Bicep for Azure Container Apps, Azure Container Registry, PostgreSQL Flexible Server, managed identity, and Azure OpenAI.

## Project Structure

```text
backend/
  app/
  tests/
  pyproject.toml
  uv.lock
frontend/
  app/
  components/
  hooks/
  lib/
  package.json
  package-lock.json
infra/
  main.bicep
  main.parameters.json
  modules/
azure.yaml
compose.yaml
```

## Commands

- Install dependencies: `make install`
- Start local Postgres: `docker compose up -d postgres`
- Run backend tests: `cd backend && uv run pytest`
- Run frontend lint: `cd frontend && npm run lint`
- Run frontend build: `cd frontend && npm run build`
- Run the local stack: `make dev`
- Stop local Postgres: `docker compose stop postgres`

## Code Style

- Python 3.12 and TypeScript 6: follow existing project conventions and preserve type safety.
- Use `uv` for backend dependency management and `npm` for frontend dependency management.
- Do not use API-key based Azure OpenAI authentication. Runtime Azure OpenAI clients must use `DefaultAzureCredential`/managed identity token flow.
- The default chat deployment/model is `gpt-5.3-chat`; keep backend config, Bicep defaults, env examples, and docs aligned.
- Let `AZURE_LOCATION` from azd drive regional Azure resources. Do not add hardcoded regional fallbacks such as `eastus2`; Azure-global resources may still use `global` where required by Azure.
- This app does not provision a Foundry AI Project. If `azd up` fails in an `azure.ai.agents` postdeploy hook because `AZURE_AI_PROJECT_ENDPOINT` is unset, the failure comes from the optional preview azd extension, not this repo.

## Recent Changes

- 2026-05-20: Switched Azure OpenAI runtime configuration to managed identity / `DefaultAzureCredential`, disabled key-based auth guidance, and standardized the default chat deployment to `gpt-5.3-chat`.
- 2026-05-20: Upgraded backend libraries to current major versions, including `agent-framework-core`/`agent-framework-openai` 1.5, OpenAI 2.37, FastAPI 0.136, SQLAlchemy 2.1 beta, and pytest 9.
- 2026-05-20: Upgraded frontend stack to Next.js 16.2, React 19.2, TypeScript 6.0, ESLint 9, Recharts 3, and Zod 4.
- 2026-05-20: Documented the optional `azure.ai.agents` azd extension postdeploy conflict for deployments that do not use Foundry AI Project endpoints.

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
