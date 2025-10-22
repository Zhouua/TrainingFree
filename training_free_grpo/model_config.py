"""
Model configuration module for training_free_grpo.
Provides utilities to dynamically configure LLM models via environment variables.
Supports simplified provider names (qwen, gemini, deepseek, openai) that read 
model name and API key from .env file.
"""

import os


# Model provider configurations
MODEL_PROVIDERS = {
    "deepseek": {
        "env_prefix": "DEEPSEEK",
        "type": "chat.completions",
        "base_url": "https://api.deepseek.com/v1",
    },
    "qwen": {
        "env_prefix": "QWEN",
        "type": "chat.completions",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    },
    "gemini": {
        "env_prefix": "GEMINI",
        "type": "chat.completions",
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
    },
    "openai": {
        "env_prefix": "OPENAI",
        "type": "chat.completions",
        "base_url": "https://api.openai.com/v1",
    },
}


def get_supported_models():
    """
    Get list of supported model provider names.
    
    Returns:
        list: List of supported model provider names (qwen, gemini, deepseek, openai)
    """
    return list(MODEL_PROVIDERS.keys())


def setup_model_env(provider_name: str):
    """
    Set up environment variables for the specified model provider.
    Reads model name and API key from .env file based on provider prefix.
    
    For example, if provider_name is 'qwen', it will:
    1. Read QWEN_MODEL from .env (e.g., 'qwen3-8b')
    2. Read QWEN_API_KEY from .env
    3. Set UTU_LLM_MODEL, UTU_LLM_API_KEY, UTU_LLM_BASE_URL accordingly
    
    Args:
        provider_name: Model provider name (qwen, gemini, deepseek, openai)
        
    Raises:
        ValueError: If provider_name is not supported or required env vars are missing
    """
    if provider_name not in MODEL_PROVIDERS:
        raise ValueError(
            f"Unsupported model provider: {provider_name}. "
            f"Supported providers are: {', '.join(get_supported_models())}"
        )
    
    provider_config = MODEL_PROVIDERS[provider_name]
    env_prefix = provider_config["env_prefix"]
    
    # Read model name from environment (e.g., QWEN_MODEL=qwen3-8b)
    model_name_var = f"{env_prefix}_MODEL"
    model_name = os.getenv(model_name_var)
    
    if not model_name:
        raise ValueError(
            f"Model name not found. Please set {model_name_var} in your .env file."
        )
    
    # Read API key from environment (e.g., QWEN_API_KEY=sk-xxx)
    api_key_var = f"{env_prefix}_API_KEY"
    api_key = os.getenv(api_key_var)
    
    if not api_key:
        raise ValueError(
            f"API key not found. Please set {api_key_var} in your .env file."
        )
    
    # Set UTU_LLM_* environment variables
    os.environ["UTU_LLM_TYPE"] = provider_config["type"]
    os.environ["UTU_LLM_MODEL"] = model_name
    os.environ["UTU_LLM_BASE_URL"] = provider_config["base_url"]
    os.environ["UTU_LLM_API_KEY"] = api_key
    
    print(f"✓ Configured environment for model provider: {provider_name}")
    print(f"  - Model: {model_name}")
    print(f"  - Type: {provider_config['type']}")
    print(f"  - Base URL: {provider_config['base_url']}")
    print(f"  - API Key: {'*' * max(0, len(api_key) - 4) + api_key[-4:] if len(api_key) >= 4 else '****'}")
