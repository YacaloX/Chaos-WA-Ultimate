import tkinter as tk

from chaos_engine import ChaosEngine

if __name__ == "__main__":
    root = tk.Tk()

    root.minsize(400, 500)

    engine = ChaosEngine(root)

    root.protocol(
        "WM_DELETE_WINDOW",
        lambda: (
            setattr(engine, "is_running", False),
            root.destroy()
        )
    )

    root.mainloop()
