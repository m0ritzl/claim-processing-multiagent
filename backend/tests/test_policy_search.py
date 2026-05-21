from types import SimpleNamespace

from app.core import config
from app.workflow import policy_search


def test_policy_search_embeddings_use_deployments_api_version(monkeypatch):
    embedding_kwargs = {}

    class FakeAzureOpenAIEmbeddings:
        def __init__(self, **kwargs) -> None:
            embedding_kwargs.update(kwargs)

    monkeypatch.setattr(policy_search, "AzureOpenAIEmbeddings", FakeAzureOpenAIEmbeddings)
    monkeypatch.setattr(
        config,
        "get_settings",
        lambda: SimpleNamespace(
            azure_openai_endpoint="https://example.openai.azure.com",
            azure_openai_embedding_model="text-embedding-3-large",
            azure_openai_api_version="preview",
            azure_openai_deployments_api_version="2024-10-21",
        ),
    )

    search = policy_search.PolicyVectorSearch()

    assert search.embeddings is not None
    assert embedding_kwargs["model"] == "text-embedding-3-large"
    assert embedding_kwargs["api_version"] == "2024-10-21"
