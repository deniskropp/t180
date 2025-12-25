from typing import List, Optional
from jeepney import DBusAddress, new_method_call
from jeepney.io.blocking import open_dbus_connection

from .models import ClipboardItem

class KlipperClient:
    """A client to interact with the KDE Klipper D-Bus service."""
    
    BUS_NAME = "org.kde.klipper"
    OBJECT_PATH = "/klipper"
    INTERFACE = "org.kde.klipper.klipper"

    def __init__(self):
        self._connection = None
        self._address = DBusAddress(self.OBJECT_PATH, bus_name=self.BUS_NAME, interface=self.INTERFACE)

    def _get_connection(self):
        if self._connection is None:
            self._connection = open_dbus_connection(bus='SESSION')
        return self._connection

    def get_current_content(self) -> Optional[str]:
        """Retrieves the current clipboard content."""
        try:
            msg = new_method_call(self._address, "getClipboardContents")
            reply = self._get_connection().send_and_get_reply(msg)
            return reply[0]
        except Exception:
            return None

    def set_clipboard(self, text: str) -> None:
        """Sets the current system clipboard content."""
        msg = new_method_call(self._address, "setClipboardContents", "s", (text,))
        self._get_connection().send_and_get_reply(msg)

    def get_history(self) -> List[ClipboardItem]:
        """Retrieves the full clipboard history."""
        # Klipper doesn't have a direct 'get all' but we can iterate or use getClipboardHistoryMenu
        # For this SDK, we'll try to fetch items by index until we hit an error or empty
        history = []
        for i in range(20):  # Reasonable limit for now
            try:
                msg = new_method_call(self._address, "getClipboardHistoryItem", "i", (i,))
                reply = self._get_connection().send_and_get_reply(msg)
                content = reply[0]
                if not content:
                    break
                history.append(ClipboardItem.from_raw(i, content))
            except Exception:
                break
        return history

    def clear_history(self) -> None:
        """Clears the entire clipboard history."""
        msg = new_method_call(self._address, "clearClipboardHistory")
        self._get_connection().send_and_get_reply(msg)

    def select_item(self, index: int) -> None:
        """Selects a history item by index and makes it active."""
        # Klipper doesn't have a direct 'select by index' method in its basic D-Bus API
        # but setting it via setClipboardContents works if we have the content.
        items = self.get_history()
        if 0 <= index < len(items):
            self.set_clipboard(items[index].content)
        else:
            raise IndexError("Clipboard history index out of range")
