import tkinter as tk
from tkinter import ttk

from config import CONFIG

class ChatUI:
    def __init__(self, root, send_callback):

        self.root = root

        self.root.title("Chaos WA Ultimate - by YacaloX")
        self.root.geometry("420x700")

        self.root.configure(bg=CONFIG["COLORS"]["bg"])

        header = tk.Frame(
            root,
            bg=CONFIG["COLORS"]["header"],
            height=60
        )

        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Los Pendejos de Silicio",
            fg="white",
            bg=CONFIG["COLORS"]["header"],
            font=("Segoe UI", 12, "bold")
        ).pack(pady=15)

        self.status = tk.Label(
            root,
            text="en línea",
            bg="#eeeeee",
            font=("Segoe UI", 7)
        )

        self.status.pack(fill=tk.X)

        # canvas

        container = tk.Frame(root)

        container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            container,
            bg=CONFIG["COLORS"]["bg"],
            highlightthickness=0
        )

        self.scroll = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=self.scroll.set
        )

        self.canvas.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        self.scroll.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        self.y_pos = 20

        # input

        bottom = tk.Frame(root, bg="white")

        bottom.pack(fill=tk.X, side=tk.BOTTOM)

        self.entry = tk.Entry(
            bottom,
            font=("Segoe UI", 11),
            bd=0
        )

        self.entry.pack(
            fill=tk.X,
            padx=15,
            pady=15
        )

        self.entry.bind(
            "<Return>",
            lambda e: send_callback()
        )

        self.entry.focus_set()

    def draw_msg(self, msg):

        side = "right" if msg.author == "Yo" else "left"

        color = (
            CONFIG["COLORS"]["user"]
            if side == "right"
            else CONFIG["COLORS"]["bot"]
        )

        anchor = "ne" if side == "right" else "nw"

        x = 390 if side == "right" else 20

        bubble = tk.Frame(
            self.canvas,
            bg=color,
            padx=10,
            pady=7
        )

        if not msg.is_event:

            tk.Label(
                bubble,
                text=msg.author,
                font=("Segoe UI", 8, "bold"),
                bg=color,
                fg="#075e54"
            ).pack(anchor="w")

        tk.Label(
            bubble,
            text=msg.text,
            font=("Segoe UI", 10),
            bg=color,
            wraplength=240,
            justify="left"
        ).pack(anchor="w")

        tk.Label(
            bubble,
            text=msg.time,
            font=("Segoe UI", 6),
            bg=color,
            fg="gray"
        ).pack(anchor="e")

        self.canvas.create_window(
            x,
            self.y_pos,
            window=bubble,
            anchor=anchor
        )

        self.root.update_idletasks()

        self.y_pos += bubble.winfo_reqheight() + 15

        self.canvas.config(
            scrollregion=(0, 0, 400, self.y_pos)
        )

        self.canvas.yview_moveto(1.0)
