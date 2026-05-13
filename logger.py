import json
import os
from datetime import datetime

class JSONLogger:
    def __init__(self, filename="chat_logs.jsonl"):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8"):
                pass

    def log(self, level, event_type, data):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "type": event_type,
            "payload": data
        }

        try:
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        except Exception as e:
            print("error escribiendo log:", e)


logger_json = JSONLogger()
