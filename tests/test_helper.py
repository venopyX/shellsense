from config.settings import Config

def test_config():
    assert Config.ACCOUNT_ID is not None
    assert Config.API_TOKEN is not None
    assert Config.MODEL_NAME is not None
