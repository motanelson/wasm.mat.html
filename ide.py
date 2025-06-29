import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.font as tkfont
import os

class CodeEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Editor")
        self.root.geometry("800x600")
        self.root.configure(bg="yellow")

        self.keywords = self.load_keywords()
        #print(self.keywords)
        self.suggestion_box = None

        self.create_menu()
        self.create_text_widget()
        self.text.bind("<KeyRelease>", self.on_key_release)

    def load_keywords(self):
        try:
            with open("lang.csv", "r") as f:
                data = f.read()
                keywords = [kw.strip() for kw in data.split("\n") if kw.strip()]
                #print(keywords)
                return sorted(set(keywords))
        except FileNotFoundError:
            messagebox.showerror("Erro", "Ficheiro lang.csv não encontrado!")
            return []

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def create_text_widget(self):
        self.text = tk.Text(self.root, wrap="word", bg="yellow", fg="black", insertbackground="black")
        self.text.pack(expand=True, fill="both")

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Pas files", "*.pas")])
        if path:
            with open(path, "r") as f:
                content = f.read()
                self.text.delete("1.0", tk.END)
                self.text.insert("1.0", content)

    def save_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".pas", filetypes=[("Pas files", "*.pas")])
        if path:
            with open(path, "w") as f:
                content = self.text.get("1.0", tk.END)
                f.write(content.strip())

    def on_key_release(self, event):
        if event.keysym in ["space", "Return", "Up", "Down", "Left", "Right"]:
            self.destroy_suggestion_box()
            return

        word = self.get_current_word()
        if not word:
            self.destroy_suggestion_box()
            return

        suggestions = [kw for kw in self.keywords if kw.startswith(word)]
        if not suggestions:
            self.destroy_suggestion_box()
            return

        self.show_suggestions(suggestions[:8])

    def get_current_word(self):
        index = self.text.index("insert")
        line, col = map(int, index.split('.'))
        start = f"{line}.{max(0, col - 1)}"
        while col > 0:
            char = self.text.get(start)
            if not char.isalnum() and char != "_":
                break
            col -= 1
            start = f"{line}.{max(0, col - 1)}"
        word_start = f"{line}.{col}"
        word = self.text.get(word_start, index).strip()
        return word

    def show_suggestions(self, words):
        self.destroy_suggestion_box()

        try:
            x, y, _, _ = self.text.bbox("insert")
            x += self.text.winfo_rootx()
            y += self.text.winfo_rooty()

            # Corrigir a linha com o uso correto do font object
            font_obj = tkfont.Font(font=self.text.cget("font"))
            y += font_obj.metrics("linespace")
        except:
            return  # Não mostrar se houver erro no cálculo da posição

        self.suggestion_box = tk.Toplevel(self.root)
        self.suggestion_box.wm_overrideredirect(True)
        self.suggestion_box.wm_geometry("+%d+%d" % (x, y))
        self.suggestion_box.configure(bg="lightyellow", padx=5, pady=5)

        for w in words:
            label = tk.Label(self.suggestion_box, text=w, anchor="w", bg="lightyellow")
            label.pack(fill="x")
            label.bind("<Button-1>", lambda e, word=w: self.insert_suggestion(word))

    def insert_suggestion(self, word):
        index = self.text.index("insert")
        col = int(index.split(".")[1])
        self.text.delete(f"{index} - {len(self.get_current_word())}c", index)
        self.text.insert("insert", word + " ")
        self.destroy_suggestion_box()

    def destroy_suggestion_box(self):
        if self.suggestion_box:
            self.suggestion_box.destroy()
            self.suggestion_box = None

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEditorApp(root)
    root.mainloop()

