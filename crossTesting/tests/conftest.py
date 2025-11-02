import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_fmtIt(mocker):
    """Mocks the fmtIt function and returns the mock object."""
    return mocker.patch("pyUpdatedto3.fmtIt.fmtIt", new_callable=MagicMock)


@pytest.fixture
def mock_newPhen(mocker):
    """Mocks the newPhen function and returns the mock object."""
    return mocker.patch("pyUpdatedto3.newPhen.newPhen", new_callable=MagicMock)
