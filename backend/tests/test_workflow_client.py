from types import SimpleNamespace

from app.workflow import client as workflow_client


def test_agent_framework_chat_client_uses_latest_azure_preview_api(monkeypatch):
    monkeypatch.setattr(
        workflow_client,
        "get_settings",
        lambda: SimpleNamespace(
            azure_openai_endpoint="https://example.openai.azure.com",
            azure_openai_deployment_name="gpt-5.3-chat",
            azure_openai_api_version="preview",
        ),
    )
    monkeypatch.setattr(workflow_client, "DefaultAzureCredential", lambda: object())

    chat_client = workflow_client.build_chat_client()

    assert chat_client.model == "gpt-5.3-chat"
    assert chat_client.api_version == "preview"
    assert str(chat_client.client.base_url) == "https://example.openai.azure.com/openai/v1/"
