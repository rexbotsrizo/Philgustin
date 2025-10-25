"""
Configuration module - Loads environment variables and settings
"""
import os
from dotenv import load_dotenv


def load_config():
    """Load configuration for the app.

    Priority order:
    1. Streamlit secrets (st.secrets) if available (used on Streamlit Cloud)
    2. Environment variables
    3. .env file values

    Returns a dict with keys: openai_api_key, model, temperature, max_tokens
    """

    # Load .env into environment as fallback
    load_dotenv()

    def _get(key, default=None):
        # Try Streamlit secrets first (only on Streamlit Cloud)
        try:
            import streamlit as _st
            return _st.secrets.get(key, os.getenv(key, default))
        except Exception:
            # Not on Streamlit or no secrets file - use env vars
            return os.getenv(key, default)

    config = {
        "openai_api_key": _get("OPENAI_API_KEY", ""),
        "model": _get("MODEL_NAME", "gpt-4"),
        "temperature": float(_get("TEMPERATURE", "0.7")),
        "max_tokens": int(_get("MAX_TOKENS", "1000"))
    }

    return config
