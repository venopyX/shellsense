from config.config_loader import load_env

def test_load_env():
    env = load_env()
    assert "OPENAI_API_KEY" in env
    assert isinstance(env["OPENAI_API_KEY"], str)
