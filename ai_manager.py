import ollama
import random
import traceback

from config import CONFIG
from logger import logger_json

class AIManager:
    def generate(self, model, prompt, system_extra=""):
        with CONFIG["AI_LOCK"]:
            try:
                full_prompt = f"""
{system_extra}

{prompt}
"""

                response = ollama.chat(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": full_prompt
                        }
                    ],
                    options={
                        "temperature": 0.65,
                        "top_p": 0.5,
                        "repeat_penalty": 1.2,
                        "num_predict": 35,
                        "num_ctx": CONFIG["CTX_LEN"],
                        "stop": [
                            "\n",
                            "yo:",
                            "user:",
                            "assistant:"
                        ]
                    }
                )

                raw = response["message"]["content"].strip()

                # Filtro anti‑ChatGPT: si el modelo intenta ser asistente, lo matamos
                if "cómo puedo ayudarte" in raw.lower():
                    return random.choice(["xd", "k", "._."])

                return raw

            except Exception as e:

                logger_json.log(
                    "ERROR",
                    "ai_error",
                    {
                        "model": model,
                        "error": str(e),
                        "traceback": traceback.format_exc()
                    }
                )

                return None


ai_broker = AIManager()
