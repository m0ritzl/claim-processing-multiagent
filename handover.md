# Handover

## Context

This session implemented the plan to remove Azure OpenAI key-based authentication, standardize deployment defaults, update Azure resource location handling, upgrade dependencies, and document deployment caveats.

The worktree is intentionally dirty with many modified files; no commit has been created.

## Main changes made

### Azure OpenAI authentication and model defaults

- Removed key-based Azure OpenAI auth assumptions from runtime code and docs.
- Standardized runtime clients on Microsoft Entra ID auth using `DefaultAzureCredential` / managed identity token flow.
- Set the default chat deployment/model to `gpt-5.3-chat`.
- Kept embeddings on `text-embedding-3-large`.
- Added shared backend defaults in `backend/app/core/config.py`.
- Updated Azure OpenAI usage in:
  - `backend/app/workflow/client.py`
  - `backend/app/workflow/tools.py`
  - `backend/app/workflow/policy_search.py`
  - `backend/app/services/scenario_generator.py`

### Agent Framework upgrade compatibility

- Backend dependency upgrade split OpenAI support into `agent-framework-openai`.
- Updated agent code from the previous `ChatAgent` / `AzureOpenAIChatClient` API to:
  - `agent_framework.Agent`
  - `agent_framework.openai.OpenAIChatClient`
- Updated specialist factories, registry, supervisor docs, and related spec docs accordingly.

### Azure infrastructure

- Updated Bicep defaults to `gpt-5.3-chat`.
- Changed Azure OpenAI chat and embedding deployment SKU from `Standard` to `GlobalStandard` in:
  - `infra/modules/cognitive-services.bicep`
  - `infra/main.json`
- Removed the hardcoded `${AZURE_LOCATION=eastus2}` fallback from `infra/main.parameters.json`; `AZURE_LOCATION` from azd should drive regional resources.
- Removed hardcoded `eastus2` Container Apps CORS origin from `backend/app/main.py`.
- `infra/main.json` was manually kept in sync because `az bicep build` timed out in this environment.

### Dependency upgrades

- Backend `pyproject.toml` / `uv.lock` upgraded to current major versions, including:
  - FastAPI `>=0.136.1`
  - Uvicorn `>=0.47.0`
  - OpenAI `>=2.37.0`
  - `agent-framework-core>=1.5.0`
  - `agent-framework-openai>=1.5.0`
  - SQLAlchemy `>=2.1.0b2`
  - pytest `>=9.0.3`
- Frontend `package.json` / `package-lock.json` upgraded, including:
  - Next.js `16.2.6`
  - React `19.2.6`
  - TypeScript `6.0.3`
  - ESLint `9.39.4`
  - Recharts `3.8.1`
  - Zod `4.4.3`
- `Makefile` now uses plain `npm install` instead of `npm install --legacy-peer-deps`.

### Frontend compatibility fixes

- Updated `frontend/eslint.config.mjs` to the Next.js 16 flat config style.
- Disabled newly introduced React compiler lint rules that flagged existing app patterns unrelated to this upgrade.
- Fixed `streamdown` prop typing in `frontend/components/ai-elements/reasoning.tsx`.
- Fixed Recharts 3 tooltip/legend typing in `frontend/components/ui/chart.tsx`.
- Next.js updated `frontend/tsconfig.json` during build (`jsx: react-jsx`, added `.next/dev/types/**/*.ts`).

### Documentation

- Updated root `AGENTS.md` with the current stack, commands, conventions, model/auth defaults, and azd extension caveat.
- Updated `README.md`, backend/frontend docs, env examples, and specs to remove API-key auth guidance and old model names.
- Documented the `azure.ai.agents` azd extension postdeploy issue:
  - This repo does not provision a Foundry AI Project.
  - If `azd up` fails with `AZURE_AI_PROJECT_ENDPOINT is not set`, it is caused by the optional preview `azure.ai.agents` extension, not this app.
  - User chose not to uninstall the extension; docs only were updated.

## Validation already run

- Backend tests:
  - `docker compose up -d postgres`
  - `cd backend && uv run pytest`
  - Result: `7 passed, 8 skipped, 4 warnings`
  - Postgres was stopped afterward with `docker compose stop postgres`.
- Frontend:
  - `cd frontend && npm run lint`
  - Result: passed with 3 existing `@next/next/no-img-element` warnings.
  - `cd frontend && npm run build`
  - Result: passed.
- Static checks:
  - `python3 -m json.tool infra/main.json`
  - `python3 -m json.tool infra/main.parameters.json`
  - `git --no-pager diff --check`
  - repo-wide searches for old key-auth/model/region strings returned clean after updates.
- Security audit:
  - `npm audit --audit-level=high` passed.
  - `npm audit` still reports moderate PostCSS findings via the current latest Next dependency; npm suggests a bad forced downgrade, so no forced audit fix was applied.

## Known caveats / follow-ups

- `az bicep build` and `az bicep version` timed out in this environment. `infra/main.json` was updated manually and validated as JSON, but a future session with working Bicep tooling should regenerate it from `infra/main.bicep`.
- The optional `azure.ai.agents` azd extension is installed locally and caused `azd up` to fail after resources deployed because `AZURE_AI_PROJECT_ENDPOINT` was not set. The app resources and services had already provisioned/deployed successfully. If rerunning deployment and the extension is not needed, consider `azd extension uninstall azure.ai.agents`.
- Lint still warns about three `<img>` usages:
  - `frontend/components/agent-outputs/conversation-step.tsx`
  - `frontend/components/claims/claim-detail.tsx`
- `infra/modules/cognitive-services.bicep` still uses chat model version `2024-11-20`; verify this version is correct for `gpt-5.3-chat` in the target Azure region/catalog.

## Useful commands for the next session

```bash
git --no-pager status --short
cd backend && uv run pytest
cd frontend && npm run lint
cd frontend && npm run build
python3 -m json.tool infra/main.json >/dev/null
python3 -m json.tool infra/main.parameters.json >/dev/null
git --no-pager diff --check
```

