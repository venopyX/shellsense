from pyplugin.utils.helper import OpenAIProvider

def test_openai_provider_chat():
    provider = OpenAIProvider()
    response = provider.chat("Hello, this is a test.")
    assert isinstance(response, str)
