import threading

CONFIG = {
    "MAX_HISTORY": 12,

    "MIN_BOT_DELAY": 1,
    "MAX_BOT_DELAY": 4,

    "MAX_BOT_CHAIN": 2,

    "CTX_LEN": 1024,

    "AI_LOCK": threading.Lock(),

    "COLORS": {
        "bg": "#efeae2",
        "user": "#dcf8c6",
        "bot": "#ffffff",
        "header": "#075e54"
    }
}
