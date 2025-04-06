import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

SEARCH_PATH = r"your file"
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

def search_files(keyword, search_content=False):
    results = []
    for root, dirs, files in os.walk(SEARCH_PATH):
        for dir in dirs:
            if keyword.lower() in dir.lower():
                results.append(os.path.join(root, dir))
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if file.lower().endswith(IMAGE_EXTENSIONS):
                    if keyword.lower() in file.lower():
                        results.append(file_path)
                elif search_content:
                    with open(file_path, 'r', errors='ignore') as f:
                        if keyword.lower() in f.read().lower():
                            results.append(file_path)
            except Exception as e:
                print(f"Erreur avec {file_path} : {e}")
    return results

def start_search():
    keyword = entry.get()
    if not keyword:
        messagebox.showwarning("Erreur", "Tu dois entrer un mot-clé.")
        return

    results = search_files(keyword, var.get() == "content")
    listbox.delete(0, tk.END)

    if results:
        for path in results:
            listbox.insert(tk.END, path)
    else:
        listbox.insert(tk.END, "Aucun résultat trouvé.")

def open_file(event):
    selection = listbox.curselection()
    if not selection:
        return

    filepath = listbox.get(selection[0])
    if not os.path.exists(filepath):
        return

    ext = os.path.splitext(filepath)[1].lower()
    if ext in IMAGE_EXTENSIONS:
        show_image(filepath)
    else:
        os.startfile(filepath)

def show_image(path):
    try:
        img_win = tk.Toplevel(root)
        img_win.title(os.path.basename(path))

        img = Image.open(path)
        img.thumbnail((800, 600))
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(img_win, image=img_tk)
        label.image = img_tk
        label.pack()
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'afficher l'image : {e}")

def on_enter(event):
    start_search()

root = tk.Tk()
root.title("Recherche")
root.geometry("700x450")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.X)

entry = ttk.Entry(frame, width=50)
entry.pack(side=tk.LEFT, padx=(0, 10), expand=True, fill=tk.X)
entry.bind("<Return>", on_enter)

var = tk.StringVar(value="name")
ttk.Radiobutton(frame, text="Par nom", variable=var, value="name").pack(side=tk.LEFT)
ttk.Radiobutton(frame, text="Par contenu", variable=var, value="content").pack(side=tk.LEFT)

ttk.Button(frame, text="Rechercher", command=start_search).pack(side=tk.LEFT, padx=10)

listbox = tk.Listbox(root, font=("Consolas", 10))
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
listbox.bind("<Double-Button-1>", open_file)

root.mainloop()
