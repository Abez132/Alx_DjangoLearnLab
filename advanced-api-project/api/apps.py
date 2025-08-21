"""
App configuration for the API application.

This module contains the configuration class for the API app.
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Configuration class for the API application.
    
    This class defines the configuration for the API Django app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'