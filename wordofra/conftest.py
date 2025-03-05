import pytest
from django.conf import settings

def pytest_configure():
    """Override some Django settings for testing."""
    settings.DEBUG = False
    settings.USE_TZ = True

@pytest.fixture(autouse=True)
def disable_throttling(settings):
    settings.REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []