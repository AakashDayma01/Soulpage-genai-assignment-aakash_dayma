import tkinter as tk
from tkinter import ttk

class StockBotGUI:
    def __init__(self, root, llm_analyst, llm_collector, llm_general):
        self.root = root
        self.llm_analyst = llm_analyst
        self.llm_collector = llm_collector
        self.llm_general = llm_general

        self.root.title("StockBot Chat")
        self.root.geometry("700x600")
        self.root.configure(bg="#ece5dd")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Scrollable chat frame
        self.chat_frame = tk.Frame(root, bg="#ece5dd")
        self.chat_frame.grid(row=0, column=0, sticky="nsew")
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.chat_frame, bg="#ece5dd", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#ece5dd")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.window_id, width=e.width))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.bind_mousewheel(self.canvas)

        # Bottom frame for input
        self.bottom_frame = tk.Frame(root, bg="#f0f0f0")
        self.bottom_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.bottom_frame.grid_columnconfigure(0, weight=1)

        self.user_input = tk.Entry(self.bottom_frame, font=("Helvetica", 12))
        self.user_input.grid(row=0, column=0, sticky="ew", padx=(10,5), pady=10, ipady=6)
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = ttk.Button(self.bottom_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=(0,10), pady=10)

        # Track user bubble widgets for responsive resizing
        self.user_bubbles = []
        self.bubble_max_width_percentage = 0.6
        self.user_wraplength = max(100, int(self.canvas.winfo_width() * self.bubble_max_width_percentage))
        self.root.bind("<Configure>", self.on_resize)

    def bind_mousewheel(self, widget):
        if widget.winfo_exists():
            widget.bind_all("<MouseWheel>", self.on_mousewheel)   # Windows
            widget.bind_all("<Button-4>", self.on_mousewheel)     # Linux scroll up
            widget.bind_all("<Button-5>", self.on_mousewheel)     # Linux scroll down

    def on_mousewheel(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(-int(event.delta / 120), "units")

    def send_message(self, event=None):
        user_text = self.user_input.get().strip()
        if not user_text:
            return
        self.add_user_bubble(user_text)
        self.user_input.delete(0, tk.END)
        self.root.after(100, lambda: self.get_bot_response(user_text))

    def get_bot_response(self, user_text):
        from main import Orchestrator
        import re
        response = Orchestrator(
            user_text,
            llm_analyst=self.llm_analyst,
            llm_collector=self.llm_collector,
            llm_general=self.llm_general
        )
        response = re.sub(r'\x1b\[.*?m', '', response)
        self.add_bot_bubble(response)

    def add_user_bubble(self, text):
        bubble_frame = tk.Frame(self.scrollable_frame, bg="#ece5dd")
        bubble_frame.pack(fill="x", anchor="e", pady=5, padx=10)

        bubble = tk.Label(
            bubble_frame, text=text, bg="#25d366", fg="white",
            font=("Helvetica", 11), wraplength=self.user_wraplength,
            justify="left", padx=12, pady=8
        )
        bubble.pack(anchor="e", padx=5)
        self.user_bubbles.append(bubble)
        self.scroll_to_bottom()

    def add_bot_bubble(self, text):
        bubble_frame = tk.Frame(self.scrollable_frame, bg="#ece5dd")
        bubble_frame.pack(fill="x", anchor="w", pady=5, padx=10)

        text_widget = tk.Text(
            bubble_frame, bg="#ffffff", fg="#000000",
            font=("Helvetica", 11), wrap="word", padx=12, pady=8,
            bd=0, relief="flat", height=1
        )
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")
        self.auto_resize_text(text_widget)
        self.scroll_to_bottom()

    def auto_resize_text(self, text_widget):
        text_widget.update_idletasks()
        lines = int(text_widget.index('end-1c').split('.')[0])
        text_widget.config(height=lines)

    def on_resize(self, event):
        try:
            width = self.canvas.winfo_width() or self.root.winfo_width()
            new_wrap = max(100, int(width * self.bubble_max_width_percentage))
            if new_wrap != self.user_wraplength:
                self.user_wraplength = new_wrap
                for lbl in list(self.user_bubbles):
                    try:
                        lbl.config(wraplength=self.user_wraplength)
                    except Exception:
                        try:
                            self.user_bubbles.remove(lbl)
                        except Exception:
                            pass
        except Exception:
            pass

    def scroll_to_bottom(self):
        self.root.update_idletasks()
        self.canvas.yview_moveto(1)


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from langchain_groq import ChatGroq

    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    llm_collector = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama-3.1-8b-instant", temperature=0)
    llm_analyst = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama-3.1-8b-instant", temperature=0)
    llm_general = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama-3.1-8b-instant", temperature=0.7)

    root = tk.Tk()
    gui = StockBotGUI(root, llm_analyst, llm_collector, llm_general)
    root.mainloop()
