"""
Initialize utils package
"""
from .config import load_config
from .lead_manager import LeadDataManager

__all__ = ['load_config', 'LeadDataManager']
