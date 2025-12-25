from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ClipboardItem(BaseModel):
    """Represents a single item in the Klipper clipboard history."""
    id: str = Field(..., description="Unique identifier for the clipboard item")
    content: str = Field(..., description="The text content of the clipboard item")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the item was added or seen")
    preview: Optional[str] = Field(None, description="A short preview of the content")

    @classmethod
    def from_raw(cls, index: int, content: str) -> "ClipboardItem":
        # Using index as part of ID for simplicity, or a hash of content
        import hashlib
        item_id = hashlib.md5(content.encode('utf-8')).hexdigest()[:8]
        return cls(
            id=f"{index}_{item_id}",
            content=content,
            preview=content[:50] + "..." if len(content) > 50 else content
        )
