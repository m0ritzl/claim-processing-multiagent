from types import SimpleNamespace

import pytest

from app.models.scenario import (
    ClaimType,
    Complexity,
    Locale,
    ScenarioGenerationOutput,
    ScenarioGenerationRequest,
)
from app.services.scenario_generator import (
    SCENARIO_MAX_COMPLETION_TOKENS,
    ScenarioGenerator,
)
from app.services import scenario_generator


class _FakeCompletions:
    def __init__(self, parsed_output: ScenarioGenerationOutput) -> None:
        self.kwargs: dict | None = None
        self._response = SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(parsed=parsed_output, refusal=None),
                )
            ]
        )

    def parse(self, **kwargs):
        self.kwargs = kwargs
        return self._response


def _scenario_output() -> ScenarioGenerationOutput:
    return ScenarioGenerationOutput.model_validate(
        {
            "scenario_name": "Seattle Auto Collision",
            "claim": {
                "claimant_name": "Jordan Lee",
                "incident_date": "2026-05-01",
                "claim_type": "Auto Collision",
                "description": "A rear-end collision caused bumper damage.",
                "estimated_damage": 2400,
                "location": "Seattle, WA",
                "police_report": False,
                "photos_provided": True,
                "witness_statements": "none",
                "vehicle_info": {
                    "vin": "1HGCM82633A004352",
                    "make": "Honda",
                    "model": "Accord",
                    "year": 2022,
                    "license_plate": "ABC1234",
                },
                "customer_info": {
                    "name": "Jordan Lee",
                    "email": "jordan@example.com",
                    "phone": "+1-555-0100",
                },
            },
            "policy": {
                "policy_type": "Comprehensive Auto",
                "coverage_type": "Auto",
                "effective_date": "2026-01-01",
                "expiration_date": "2026-12-31",
            },
        }
    )


def test_scenario_generator_uses_deployments_api_version(monkeypatch):
    client_kwargs = {}

    class FakeAzureOpenAI:
        def __init__(self, **kwargs) -> None:
            client_kwargs.update(kwargs)

    monkeypatch.setattr(scenario_generator, "AzureOpenAI", FakeAzureOpenAI)
    monkeypatch.setattr(scenario_generator, "DefaultAzureCredential", lambda: object())
    monkeypatch.setattr(scenario_generator, "get_bearer_token_provider", lambda *args: object())
    monkeypatch.setattr(
        scenario_generator,
        "get_settings",
        lambda: SimpleNamespace(
            azure_openai_endpoint="https://example.openai.azure.com",
            azure_openai_deployment_name="gpt-5.3-chat",
            azure_openai_api_version="preview",
            azure_openai_deployments_api_version="2024-10-21",
        ),
    )

    generator = ScenarioGenerator()

    assert generator.deployment == "gpt-5.3-chat"
    assert client_kwargs["api_version"] == "2024-10-21"


@pytest.mark.asyncio
async def test_scenario_generator_uses_gpt5_completion_token_parameter():
    completions = _FakeCompletions(_scenario_output())
    generator = ScenarioGenerator.__new__(ScenarioGenerator)
    generator.client = SimpleNamespace(
        beta=SimpleNamespace(
            chat=SimpleNamespace(
                completions=completions,
            )
        )
    )
    generator.deployment = "gpt-5.3-chat"

    request = ScenarioGenerationRequest(
        locale=Locale.US,
        claim_type=ClaimType.AUTO,
        complexity=Complexity.MODERATE,
    )

    await generator._generate_internal(request, max_retries=0)

    assert completions.kwargs is not None
    assert completions.kwargs["max_completion_tokens"] == SCENARIO_MAX_COMPLETION_TOKENS
    assert "max_tokens" not in completions.kwargs
    assert "temperature" not in completions.kwargs
