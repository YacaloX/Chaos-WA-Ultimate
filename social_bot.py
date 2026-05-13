import random
import time

class SocialBot:
    def __init__(self, name, model, traits):
        self.name = name
        self.model = model
        self.traits = traits

        self.mood = random.randint(3, 10)
        self.cooldown = 0

        # Memoria social real
        self.favorite_person = random.choice([
            "Carlos",
            "Pedro",
            "Ana",
            "Laura",
            "Yo"
        ])
        self.enemies = random.sample([
            "Carlos",
            "Pedro",
            "Ana",
            "Laura"
        ], 2)

        # Memoria tóxica para romper ciclos románticos/asistenciales
        self.last_emotion = "neutral"

        self.relationships = {}

    def decide(self, history, last_author):
        if last_author == self.name:
            return False

        if time.time() < self.cooldown:
            return False

        chance = self.traits["activity"]

        # afecto → más ganas de hablar
        if last_author == self.favorite_person:
            chance += 0.25

        # enemigos → menos
        if last_author in self.enemies:
            chance -= 0.15

        # humor
        chance += (self.mood - 5) * 0.03

        # Si el último mensaje fue romántico, el bot se apaga un 40%
        if self.last_emotion == "romantic":
            chance *= 0.6

        return random.random() < max(0.05, min(chance, 0.95))

    def get_prompt(self, history, dynamic_system=""):
        h = history[-10:]
        h_str = "\n".join(
            [f"{m.author}: {m.text}" for m in h]
        )

        return f"""
ERES {self.name}.

ESTO NO ES UN ASISTENTE.
ES UN GRUPO DE WHATSAPP.

PROHIBIDO:
- ayudar
- explicar cosas
- hablar formal
- actuar como IA
- escribir párrafos
- hablar bonito
- decir "¿cómo puedo ayudarte?"
- escribir mucho
- roleplay
- narrar acciones
- ser cariñoso
- decir "te amo"
- ser amable excesivo
- hablar como chatbot útil
- responder como terapeuta

PERSONALIDAD:
{self.traits["personality"]}

ESTILO:
{self.traits["style"]}

REGLAS:
- máximo 5 palabras
- usa minúsculas
- puedes ignorar gente
- puedes responder incoherencias
- escribe como humano real
- sé seco
- sé raro
- puedes ser tóxico
- NO seas amable siempre
- NO hables de playa
- mensajes cortos = mejor

{dynamic_system}

CHAT:

{h_str}

RESPONDE SOLO EL MENSAJE.
"""
