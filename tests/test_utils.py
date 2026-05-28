from unittest.mock import MagicMock, patch

import pytest

from src.utils import get_greeting


@pytest.mark.parametrize(
    "hour, expected_greeting",
    [
        (8, "Добрый утро"),
        (14, "Добрый день"),
        (19, "Добрый вечер"),
        (2, "Доброй ночи"),
    ],
)
@patch("src.utils.datetime")  # ИСПРАВЛЕНО: Подменяем datetime внутри src.utils
def test_get_greeting(mock_datetime, hour, expected_greeting):
    mock_now = MagicMock()
    mock_now.hour = hour
    mock_datetime.now.return_value = mock_now
    assert get_greeting("31.12.2021") == expected_greeting
