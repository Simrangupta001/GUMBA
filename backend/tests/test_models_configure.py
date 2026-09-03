# backend/tests/test_models_configure.py
"""
Sanity check: verify all SQLAlchemy model relationships are configured
correctly. Catches mismatched back_populates pairs (e.g. one side pointing
to a property name that doesn't exist on the other model) at test time
instead of on the first real request in production.
"""
import pytest


def test_all_mappers_configure_without_error():
    import app.models  # noqa: F401  (imports every model so all mappers register)
    from sqlalchemy.orm import configure_mappers

    try:
        configure_mappers()
    except Exception as e:
        pytest.fail(f"SQLAlchemy mapper configuration failed: {e}")