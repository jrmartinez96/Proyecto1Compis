import PyDecaf
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Text Editor Application - {filepath}")

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    window.title(f"Text Editor Application - {filepath}")

def compile_file():
    with open('Decaf/test_files/to_compile.txt', "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    
    errorsList = PyDecaf.compile_file('Decaf/test_files/to_compile.txt')

    console.config(state=tk.NORMAL) # se activa la edicion
    console.delete(1.0, tk.END)
    for error in errorsList:
        console.insert(tk.END, '- ' + error + '\n')

    if len(errorsList) == 0:
        console.insert(tk.END, 'Semantic analysis successful.')
    
    console.config(state=tk.DISABLED) # se desactiva la edicion
    


window = tk.Tk()
window.title("Text Editor Application")
window.rowconfigure(0, weight=3)
window.rowconfigure(1, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
txt_edit.config(height=30)
console = tk.Text(window)
console.config(state=tk.DISABLED, height=10)
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
btn_save = tk.Button(fr_buttons, text="Save As...", command=save_file)
btn_compile = tk.Button(fr_buttons, text="Compile", command=compile_file)
console_label = tk.Label(window, text='Console')

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_compile.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")
console.grid(row=1, column=1, sticky="nsew")
console_label.grid(row=1, column=0, sticky="ns")

window.mainloop()
