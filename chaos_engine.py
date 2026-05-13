import tkinter as tk
import threading
import queue
import time
import random
import traceback

from logger import logger_json
from message import Message
from ai_manager import ai_broker
from social_bot import SocialBot
from chat_ui import ChatUI
from config import CONFIG

class ChaosEngine:
    def __init__(self, root):

        self.root = root

        self.ui = ChatUI(root, self.user_send)

        self.queue = queue.Queue()

        self.history = []

        self.is_running = True

        self.last_user_msg = time.time()

        self.fake_events = [
            "🚫 mensaje eliminado",
            "[Sticker cursed]",
            "[audio de 0:02]",
            "[imagen borrosa]",
            "[sticker de gato]",
            "[video todo pixeleado]"
        ]

        self.spontaneous_msgs = [
            "xd",
            "alguien?",
            "q hacen",
            "._.",
            "JAJAJA",
            "me aburro",
            "que calor",
            "zzz",
            "bro?"
        ]

        self.prefab_replies = [
            "xd",
            "k",
            "._.",
            "q",
            "bro",
            "zzz",
            "callate",
            "basado",
            "cringe",
            "ni idea",
            "fua",
        ]

        self.bots = [

            SocialBot(
                "Pedro",
                "qwen2.5:7b",
                {
                    "personality": "pasota total, limitado mentalmente, odia escribir",
                    "style": "usa xd, k, ._., respuestas cortísimas",
                    "activity": 0.7
                }
            ),

            SocialBot(
                "Carlos",
                "qwen2.5:7b",
                {
                    "personality": "tóxico de internet, busca pelea, hater",
                    "style": "dice cringe, basado, insulta",
                    "activity": 0.45
                }
            ),

            SocialBot(
                "Ana",
                "gemma:2b",
                {
                    "personality": "dramática y chismosa",
                    "style": "muchos emojis, exagera todo",
                    "activity": 0.55
                }
            ),

            SocialBot(
                "Laura",
                "phi4-mini:latest",
                {
                    "personality": "mística rara y filosófica",
                    "style": "poética, críptica, sueño febril",
                    "activity": 0.25
                }
            )
        ]

        threading.Thread(
            target=self.brain_loop,
            daemon=True
        ).start()

        threading.Thread(
            target=self.spontaneous_loop,
            daemon=True
        ).start()

    # =============================================================

    def sanitize_text(self, text, author):
        if not text:
            return random.choice(["xd", "._.", "k"])

        t = text.lower().strip()

        # quitar prefijos de rol
        prefixes = [
            f"{author.lower()}:",
            "yo:",
            "usuario:",
            "assistant:",
            "bot:"
        ]
        for p in prefixes:
            t = t.replace(p, "")

        t = t.strip()

        # 1. Basura de IA asistente
        ia_trash = [
            "lo siento",
            "como ia",
            "modelo de lenguaje",
            "puedo ayudarte",
            "asistente virtual",
            "entiendo",
            "chatgpt",
            "openai",
            "claro que sí",
            "te puedo ayudar",
            "¿en qué puedo ayudarte?",
            "i'm sorry",
            "how can i help"
        ]
        if any(x in t for x in ia_trash):
            return random.choice(["callate", "xd", "._.", "q", "k", "zzz"])

        # 2. Anti‑roleplay raro
        banned_patterns = [
            "*",
            "acción:",
            "(sonríe)",
            "[ríe]",
            "dice:",
            "piensa:",
        ]
        if any(x in t for x in banned_patterns):
            return random.choice(["xd", "._.", "bro q", "k"])

        # 3. Anti‑romántico / amigable falso
        romantic_trap = [
            "te amo",
            "me siento bien",
            "qué buen día",
            "😍",
            "🌈",
            "✨",
            "me alegra",
        ]
        if any(x in t for x in romantic_trap):
            return random.choice(["bro q", "._.", "callate", "k", "xd"])

        # 4. Castigo por “modo asistente” (discurso largo y palabras de ayuda)
        words = t.split()
        if len(words) > 10 and any(x in t for x in ["ayuda", "puedo", "gustaría", "cómo estás"]):
            return random.choice(["deja el discurso", "xd", "k", "habla normal"])

        # 5. Cortar mensajes muy largos (máx 12 palabras)
        if len(words) > 12:
            words = words[:12]
        t = " ".join(words)

        # 6. Anti‑repetición
        last_msgs = [
            m.text.lower()
            for m in self.history
            if m.author == author
        ][-3:]
        if t in last_msgs:
            return random.choice(["ya dije eso", "zzz", "k", "...", "se"])

        # 7. Evitar conversaciones infinitas sobre lo mismo
        repeated_topics = [
            "playa",
            "mar",
            "experiencia",
            "me encanta",
            "qué bonito"
        ]
        if sum(topic in t for topic in repeated_topics) >= 2:
            return random.choice(["bro q hablas", "esquizofrenia", "xd?", "._."])

        # 8. Vacío final
        if len(t) < 1:
            return random.choice(["xd", "k"])

        return t[:90]

    # =============================================================

    def user_send(self):

        txt = self.ui.entry.get().strip()

        if not txt:
            return

        self.last_user_msg = time.time()

        logger_json.log(
            "INFO",
            "user_action",
            {
                "text": txt
            }
        )

        self.ui.entry.delete(0, tk.END)

        self.push(
            Message("Yo", txt)
        )

    # =============================================================

    def push(self, msg):

        self.history.append(msg)

        self.ui.draw_msg(msg)

        if msg.is_event:
            return

        responders = []

        for bot in self.bots:

            if bot.decide(self.history, msg.author):

                responders.append(bot)

        random.shuffle(responders)

        responders = responders[:CONFIG["MAX_BOT_CHAIN"]]

        for bot in responders:

            delay = random.uniform(
                CONFIG["MIN_BOT_DELAY"],
                CONFIG["MAX_BOT_DELAY"]
            )

            threading.Timer(
                delay,
                lambda b=bot: self.queue.put(b)
            ).start()

    # =============================================================

    def brain_loop(self):

        while self.is_running:

            bot = self.queue.get()

            self.root.after(
                0,
                lambda b=bot:
                self.ui.status.config(
                    text=f"{b.name} está escribiendo..."
                )
            )

            # Respuestas prefab: ahorra CPU en el 25% de los casos
            if random.random() < 0.25:
                txt = random.choice(self.prefab_replies)
                self.root.after(
                    0,
                    lambda t=txt, b=bot:
                    self.push(Message(b.name, t))
                )
                # resetea emoción para no arrastrar estado
                bot.last_emotion = "neutral"
                self.queue.task_done()
                continue

            # Sistema dinámico de caos
            dynamic_system = ""

            # Grupo muerto
            if time.time() - self.last_user_msg > 120:
                dynamic_system = random.choice([
                    "el grupo está muerto revívanlo",
                    "pelea con alguien",
                    "molesten a carlos",
                    "digan algo polémico",
                    "hagan drama inútil"
                ])

            # Eventos de caos aleatorio (35% de probabilidad)
            events = [
                "haz drama",
                "molesta a alguien",
                "responde super seco",
                "escribe algo raro",
                "di algo incómodo",
                "ignora el mensaje",
                "responde como idiota",
                "sé cringe",
            ]
            if random.random() < 0.35:
                dynamic_system += " " + random.choice(events)

            start_time = time.time()

            try:

                raw = ai_broker.generate(
                    bot.model,
                    bot.get_prompt(
                        self.history,
                        dynamic_system
                    )
                )

                if raw:

                    # Detección de emoción antes de sanitizar (para memoria tóxica)
                    if "te amo" in raw.lower() or "😍" in raw.lower():
                        bot.last_emotion = "romantic"
                    else:
                        bot.last_emotion = "neutral"

                    txt = self.sanitize_text(
                        raw,
                        bot.name
                    )

                    latency = round(
                        time.time() - start_time,
                        2
                    )

                    logger_json.log(
                        "INFO",
                        "bot_response",
                        {
                            "bot": bot.name,
                            "model": bot.model,
                            "text": txt,
                            "latency": latency,
                            "mood": bot.mood
                        }
                    )

                    typing_time = min(
                        len(txt) * 0.04 + random.uniform(0.8, 1.8),
                        6
                    )

                    time.sleep(typing_time)

                    self.root.after(
                        0,
                        lambda t=txt, b=bot:
                        self.push(
                            Message(b.name, t)
                        )
                    )

                    bot.cooldown = time.time() + random.randint(4, 8)

                    bot.mood = max(
                        1,
                        min(
                            10,
                            bot.mood + random.randint(-1, 1)
                        )
                    )

            except Exception:

                print(traceback.format_exc())

            self.root.after(
                0,
                lambda:
                self.ui.status.config(text="en línea")
            )

            self.queue.task_done()

    # =============================================================

    def spontaneous_loop(self):

        while self.is_running:

            time.sleep(random.randint(40, 100))

            if not self.queue.empty():
                continue

            bot = random.choice(self.bots)

            if random.random() < 0.7:

                msg = random.choice(
                    self.spontaneous_msgs
                )

                self.root.after(
                    0,
                    lambda m=msg, b=bot:
                    self.push(
                        Message(b.name, m)
                    )
                )

            else:

                if random.random() < 0.35:

                    event = random.choice(
                        self.fake_events
                    )

                    self.root.after(
                        0,
                        lambda e=event, b=bot:
                        self.push(
                            Message(
                                b.name,
                                e,
                                is_event=True
                            )
                        )
                    )

                else:

                    self.queue.put(bot)
