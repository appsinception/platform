from contextvars import ContextVar

import pytest

from backend.services.context_vars_manager import ContextEnvVarsManager
from tests.testing_utils import TEST_USER_ID


@pytest.fixture(autouse=True)
def reset_context_vars():
    # Reset the context variable to its default state before each test
    ContextEnvVarsManager.context_vars = ContextVar("context_vars")
    yield
    # No teardown needed, but you could add one if necessary


def test_set_method():
    # Test setting a new environment variable
    ContextEnvVarsManager.set("new_key", "new_value")
    assert ContextEnvVarsManager.get("new_key") == "new_value"


def test_get_method_success():
    ContextEnvVarsManager.set("user_id", TEST_USER_ID)
    assert ContextEnvVarsManager.get("user_id") == TEST_USER_ID


def test_get_method_no_key():
    ContextEnvVarsManager.set("some_key", "some_value")
    assert ContextEnvVarsManager.get("nonexistent_key") is None


def test_get_all_method_success():
    ContextEnvVarsManager.set("user_id", TEST_USER_ID)
    assert ContextEnvVarsManager.get_all() == {"user_id": TEST_USER_ID}


def test_get_all_method_empty():
    assert ContextEnvVarsManager.get_all() == {}


def test_set_method_edge_cases():
    ContextEnvVarsManager.set("", "empty_key")
    ContextEnvVarsManager.set("none_value", None)
    assert ContextEnvVarsManager.get("") == "empty_key"
    assert ContextEnvVarsManager.get("none_value") is None


def test_get_method_without_setting():
    """
    Test getting an environment variable without setting the context variable.
    This should trigger the LookupError branch and return None.
    """
    # Temporarily replace the class's ContextVar with a fresh one
    original_var = ContextEnvVarsManager.context_vars
    try:
        # Use a fresh ContextVar to ensure no data is set
        ContextEnvVarsManager.context_vars = ContextVar("test_context_vars")

        # Attempt to get a value, which should return None due to the LookupError
        assert ContextEnvVarsManager.get("unset_key") is None
    finally:
        # Restore the original ContextVar to avoid affecting other tests
        ContextEnvVarsManager.context_vars = original_var
