import random
import string
import math
import tkinter as tk
from tkinter import messagebox

def generate_password(length=12, include_numbers=True, include_symbols=True):
    character_pool = string.ascii_lowercase
    password_chars = [random.choice(string.ascii_lowercase)]

    if include_numbers:
        character_pool += string.digits
        password_chars.append(random.choice(string.digits))

    if include_symbols:
        symbols = "!@#$%^&*?"
        character_pool += symbols
        password_chars.append(random.choice(symbols))

    remaining_length = length - len(password_chars)
    if remaining_length > 0:
        password_chars.extend(random.choices(character_pool, k=remaining_length))

    random.shuffle(password_chars)
    return "".join(password_chars)

def estimate_entropy(password: str) -> float:
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(c in "!@#$%^&*?" for c in password): pool += 10

    if pool == 0:
        pool = len(set(password)) or 2

    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)

def strength_label(entropy_bits: float):
    if entropy_bits < 28:
        return "Very Weak", "red"
    elif entropy_bits < 36:
        return "Weak", "orange"
    elif entropy_bits < 60:
        return "Reasonable", "yellow"
    elif entropy_bits < 128:
        return "Strong", "lightgreen"
    else:
        return "Very Strong", "green"

def on_generate():
    try:
        length = length_var.get()
        include_numbers = num_var.get()
        include_symbols = sym_var.get()

        password = generate_password(length, include_numbers, include_symbols)
        output_var.set(password)

        entropy = estimate_entropy(password)
        label, color = strength_label(entropy)
        strength_var.set(f"{label} ({entropy} bits)")
        strength_label_widget.config(fg=color)

    except ValueError:
        messagebox.showerror("Input Error", "An unexpected error occurred.")

def on_copy():
    password = output_var.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("No Password", "Generate a password first.")

root = tk.Tk()
root.title("🔐 Password Generator")
root.geometry("480x400")
root.configure(bg="black")

FONT = ("Consolas", 12, "bold")
FG_COLOR = "#c084fc"
BG_COLOR = "black"
BTN_COLOR = "#9333ea"
ENTRY_COLOR = "#1e1b29"

length_var = tk.IntVar(value=12)

tk.Label(root, text="Password Length", font=FONT, fg=FG_COLOR, bg=BG_COLOR).pack(pady=(10, 0))
length_slider = tk.Scale(
    root,
    from_=8,
    to=32,
    orient="horizontal",
    variable=length_var,
    font=FONT,
    fg=FG_COLOR,
    bg=BG_COLOR,
    highlightthickness=0,
    troughcolor=ENTRY_COLOR,
    activebackground=BTN_COLOR,
    sliderlength=30,
    length=250
)
length_slider.pack(pady=5)

num_var = tk.BooleanVar(value=True)
sym_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include numbers", variable=num_var, font=FONT, fg=FG_COLOR,
              bg=BG_COLOR, selectcolor=BG_COLOR, activebackground=BG_COLOR).pack()
tk.Checkbutton(root, text="Include symbols", variable=sym_var, font=FONT, fg=FG_COLOR,
              bg=BG_COLOR, selectcolor=BG_COLOR, activebackground=BG_COLOR).pack()

tk.Button(root, text="Generate Password", font=FONT, fg="white", bg=BTN_COLOR,
          activebackground=FG_COLOR, activeforeground="black", command=on_generate).pack(pady=10)

output_var = tk.StringVar()
output_entry = tk.Entry(root, textvariable=output_var, font=FONT, bg=ENTRY_COLOR,
                        fg=FG_COLOR, justify="center", width=40, relief="flat", state="readonly")
output_entry.pack(pady=5)

strength_var = tk.StringVar(value="Password Strength: N/A")
strength_label_widget = tk.Label(root, textvariable=strength_var,
                                 font=("Consolas", 12, "bold"), bg=BG_COLOR, fg="gray")
strength_label_widget.pack(pady=5)

tk.Button(root, text="Copy to Clipboard", font=FONT, fg="white", bg=BTN_COLOR,
          activebackground=FG_COLOR, activeforeground="black", command=on_copy).pack(pady=10)

root.mainloop()