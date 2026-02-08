import tkinter as tk
from tkinter import ttk

class ChatBotGUI:
    def __init__(self, root):
        from bot_logic import get_bot_response
        self.root = root
        self.get_bot_response_fn = get_bot_response

        self.root.title("Conversational Knowledge Bot")
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
        # make the scrollable_frame a window inside the canvas and keep its id
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        # ensure the embedded frame always matches the canvas width so children can expand
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

        # Track user bubble widgets to update their wraplength on resize
        self.user_bubbles = []
        self.bubble_max_width_percentage = 0.6  # user bubble max width as fraction of visible chat area
        # initial wraplength (will be updated on first resize event)
        self.user_wraplength = max(100, int(self.canvas.winfo_width() * self.bubble_max_width_percentage))
        # Bind resize event to adjust bubble sizes
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
        response = self.get_bot_response_fn(user_text)
        self.add_bot_bubble(response)

    def add_user_bubble(self, text):
        bubble_frame = tk.Frame(self.scrollable_frame, bg="#ece5dd")
        bubble_frame.pack(fill="x", anchor="e", pady=5, padx=10)

        bubble = tk.Label(
            bubble_frame, text=text, bg="#25d366", fg="white",
            font=("Helvetica", 11), wraplength=400, justify="left",
            padx=12, pady=8
        )
        bubble.pack(anchor="e", padx=5)
        # apply current responsive wraplength and keep reference
        try:
            bubble.config(wraplength=self.user_wraplength)
        except Exception:
            pass
        self.user_bubbles.append(bubble)
        self.scroll_to_bottom()

    def auto_resize_text(self, text_widget):
        text_widget.update_idletasks()
        lines = int(text_widget.index('end-1c').split('.')[0])
        text_widget.config(height=lines)

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
        # Recompute wraplength based on canvas (visible chat area) width
        try:
            width = self.canvas.winfo_width() or self.root.winfo_width()
            new_wrap = max(100, int(width * self.bubble_max_width_percentage))
            if new_wrap != self.user_wraplength:
                self.user_wraplength = new_wrap
                # update existing user bubble labels
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
    root = tk.Tk()
    gui = ChatBotGUI(root)
    root.mainloop()
