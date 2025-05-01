import pytest

pytest_plugins = "pytest_asyncio"


def pytest_configure():
    pytest.asyncio_default_fixture_loop_scope = "function"
