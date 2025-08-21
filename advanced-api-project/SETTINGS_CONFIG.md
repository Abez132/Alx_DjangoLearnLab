# Django Settings Configuration

This document outlines the necessary changes to configure Django REST Framework in the settings.py file.

## Required Settings Changes

### INSTALLED_APPS
Add the following to the INSTALLED_APPS list:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'api',
]
```

### REST Framework Configuration (Optional)
For additional DRF configuration, you can add:
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

Note: The REST_FRAMEWORK configuration is optional and can be added based on project requirements.