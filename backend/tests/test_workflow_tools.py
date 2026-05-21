import sys
from types import SimpleNamespace

from app.workflow import tools


class _FakeCompletions:
    def __init__(self) -> None:
        self.kwargs: dict | None = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content='{"category": "damage_photo", "summary": "Front bumper damage", "data_extracted": {}}'
                    )
                )
            ]
        )


def test_analyze_image_uses_gpt5_supported_chat_parameters(monkeypatch):
    completions = _FakeCompletions()
    client_kwargs = {}

    class FakeAzureOpenAI:
        def __init__(self, **kwargs) -> None:
            client_kwargs.update(kwargs)
            self.chat = SimpleNamespace(completions=completions)

    monkeypatch.setitem(
        sys.modules,
        "openai",
        SimpleNamespace(AzureOpenAI=FakeAzureOpenAI),
    )
    monkeypatch.setattr(tools, "_resolve_image", lambda image_path: b"image-bytes")
    monkeypatch.setattr(tools, "_get_openai_token_provider", lambda: object())
    monkeypatch.setattr(
        tools,
        "get_settings",
        lambda: SimpleNamespace(
            azure_openai_endpoint="https://example.openai.azure.com",
            azure_openai_api_version="preview",
            azure_openai_deployments_api_version="2024-10-21",
            azure_openai_deployment_name="gpt-5.3-chat",
        ),
    )

    result = tools.analyze_image("damage.jpg")

    assert result["status"] == "success"
    assert client_kwargs["api_version"] == "2024-10-21"
    assert completions.kwargs is not None
    assert completions.kwargs["response_format"] == {"type": "json_object"}
    assert "temperature" not in completions.kwargs
