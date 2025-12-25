import pytest
from unittest.mock import MagicMock, patch
from klipper_sdk import KlipperClient, ClipboardItem

@pytest.fixture
def mock_dbus():
    with patch('klipper_sdk.client.open_dbus_connection') as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        yield mock_conn

def test_set_clipboard(mock_dbus):
    client = KlipperClient()
    client.set_clipboard("hello world")
    
    # Check if send_and_get_reply was called (jeepney sends one msg)
    assert mock_dbus.send_and_get_reply.called

def test_get_history(mock_dbus):
    client = KlipperClient()
    
    # Mock return values for getClipboardHistoryItem
    # Let's say it returns "item 1", "item 2", then ""
    mock_dbus.send_and_get_reply.side_effect = [
        ("item 1",),
        ("item 2",),
        ("",)
    ]
    
    history = client.get_history()
    assert len(history) == 2
    assert history[0].content == "item 1"
    assert history[1].content == "item 2"

def test_clear_history(mock_dbus):
    client = KlipperClient()
    client.clear_history()
    assert mock_dbus.send_and_get_reply.called
