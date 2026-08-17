import re
import tkinter as tk
from tkinter import font

def check_password_strength(pwd):
    score = 0
    tips = []

    if len(pwd) >= 8:
        score += 1
    else:
        tips.append("❌ Try to make it at least 8 characters")

    if len(pwd) >= 12:
        score += 1

    if re.search(r"[A-Z]", pwd):
        score += 1
    else:
        tips.append("❌ Throw in at least one capital letter")

    if re.search(r"[a-z]", pwd):
        score += 1
    else:
        tips.append("❌ You need a lowercase letter somewhere too")

    if re.search(r"\d", pwd):
        score += 1
    else:
        tips.append("❌ Add a number in there")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
        score += 1
    else:
        tips.append("❌ A symbol like @ # $ ! would help a lot")

    overused = ["password", "123456", "qwerty", "admin", "letmein", "welcome"]
    if pwd.lower() in overused:
        score = 0
        tips = ["❌ Come on, that's one of the most common passwords out there"]

    if score <= 2:
        verdict = "Weak"
        color = "#e74c3c"
    elif score <= 4:
        verdict = "Medium"
        color = "#f39c12"
    else:
        verdict = "Strong"
        color = "#27ae60"

    return verdict, score, tips, color

def on_check():
    pwd = entry.get()
    if not pwd:
        result_label.config(text="Please type a password first", fg="#888")
        tips_label.config(text="")
        bar.place(width=0)
        return

    verdict, score, tips, color = check_password_strength(pwd)

    result_label.config(text=f"{verdict}  ({score}/6)", fg=color)

    bar_width = int((score / 6) * 360)
    bar.place(width=bar_width)
    bar.config(bg=color)

    if tips:
        tips_label.config(text="\n".join(tips), fg="#555")
    else:
        tips_label.config(text="✅ Solid password, nothing to fix here!", fg="#27ae60")


def on_key_release(event):
    on_check()


def toggle_visibility():
    if entry.cget("show") == "*":
        entry.config(show="")
        show_btn.config(text="Hide")
    else:
        entry.config(show="*")
        show_btn.config(text="Show")


root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("420x380")
root.resizable(False, False)
root.config(bg="#f4f6f8")

title_font = font.Font(family="Segoe UI", size=16, weight="bold")
normal_font = font.Font(family="Segoe UI", size=10)

tk.Label(root, text="🔐 Password Strength Checker", font=title_font, bg="#f4f6f8", fg="#2c3e50").pack(pady=(20, 15))

entry_frame = tk.Frame(root, bg="#f4f6f8")
entry_frame.pack(pady=5)

entry = tk.Entry(entry_frame, width=25, font=("Segoe UI", 12), show="*", relief="solid", bd=1)
entry.pack(side="left", ipady=6, padx=(0, 8))
entry.bind("<KeyRelease>", on_key_release)

show_btn = tk.Button(entry_frame, text="Show", command=toggle_visibility, relief="flat", bg="#dfe6e9")
show_btn.pack(side="left")

bar_bg = tk.Frame(root, bg="#dcdde1", width=360, height=10)
bar_bg.pack(pady=(15, 5))
bar_bg.pack_propagate(False)

bar = tk.Frame(bar_bg, bg="#e74c3c", width=0, height=10)
bar.place(x=0, y=0, width=0)

result_label = tk.Label(root, text="", font=("Segoe UI", 13, "bold"), bg="#f4f6f8")
result_label.pack(pady=(10, 5))

tips_label = tk.Label(root, text="", font=normal_font, bg="#f4f6f8", justify="left", wraplength=360)
tips_label.pack(pady=5)

root.mainloop()