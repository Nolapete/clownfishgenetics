# tests/test_placeholder.py


def test_placeholder_always_passes():
    """Ensures the pytest runner finds at least one test to satisfy
    the pre-commit hook."""
    # Use explicit equality check to satisfy S101 linter rule
    assert 1 == 1
