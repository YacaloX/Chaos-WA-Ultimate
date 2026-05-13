from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class Message:
    author: str
    text: str
    time: str = field(default_factory=lambda: datetime.now().strftime("%H:%M"))
    is_event: bool = False
