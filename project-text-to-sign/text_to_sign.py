import tkinter as tk
from tkinter import messagebox, Scrollbar, Canvas
from PIL import Image, ImageTk
import os

# Path to folder containing sign language images
IMAGE_FOLDER = "project text to sign\sign_images"

def show_sign_images(text):
    """Display each letter's sign language image."""
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    if not text.strip():
        messagebox.showwarning("Input Required", "Please enter some text.")
        return

    for char in text.upper():
        if char.isalpha():  # Only letters A-Z
            found = False
            for ext in [".jpg", ".png", ".jpeg"]:
                image_path = os.path.join(IMAGE_FOLDER, f"{char}{ext}")
                if os.path.exists(image_path):
                    img = Image.open(image_path)
                    img = img.resize((120, 120))
                    photo = ImageTk.PhotoImage(img)

                    label = tk.Label(scrollable_frame, image=photo, bg="#e8f5e9")
                    label.image = photo
                    label.pack(side=tk.LEFT, padx=5, pady=5)
                    found = True
                    break
            if not found:
                tk.Label(scrollable_frame, text=f"[{char}]", font=("Arial", 14, "bold"),
                         bg="#e8f5e9", fg="red").pack(side=tk.LEFT, padx=5)
        elif char == " ":
            space_label = tk.Label(scrollable_frame, text="   ", bg="#e8f5e9")
            space_label.pack(side=tk.LEFT, padx=20)

def on_submit():
    user_text = entry.get()
    show_sign_images(user_text)

def on_enter(e):
    e.widget['background'] = "#388E3C"

def on_leave(e):
    e.widget['background'] = "#4CAF50"

def on_quit_enter(e):
    e.widget['background'] = "#d32f2f"

def on_quit_leave(e):
    e.widget['background'] = "#FF4C4C"

# Create main window
root = tk.Tk()
root.title("Text to Sign Language Converter")
root.geometry("1050x600")
root.config(bg="#f9f9f9")

# Title Frame with gradient-like effect
title_frame = tk.Frame(root, bg="#4CAF50")
title_frame.pack(fill=tk.X)

title_label = tk.Label(title_frame, text="🖐 Text to Sign Language Converter",
                       font=("Arial", 22, "bold"), bg="#4CAF50", fg="white", pady=15)
title_label.pack()

# Input frame
input_frame = tk.Frame(root, bg="#f9f9f9")
input_frame.pack(pady=20)

tk.Label(input_frame, text="Enter Text:", font=("Arial", 14, "bold"), bg="#f9f9f9").pack(side=tk.LEFT, padx=10)
entry = tk.Entry(input_frame, width=40, font=("Arial", 14), relief="solid", bd=1)
entry.pack(side=tk.LEFT, padx=10, ipady=3)

# Convert Button
submit_btn = tk.Button(input_frame, text="Convert", font=("Arial", 12, "bold"),
                       bg="#4CAF50", fg="white", activeforeground="white", relief="flat", command=on_submit)
submit_btn.pack(side=tk.LEFT, padx=10)
submit_btn.bind("<Enter>", on_enter)
submit_btn.bind("<Leave>", on_leave)

# Scrollable output area
output_container = tk.Frame(root, bg="#c8e6c9", bd=2, relief=tk.GROOVE)
output_container.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

canvas = Canvas(output_container, bg="#e8f5e9", highlightthickness=0)
scrollbar = Scrollbar(output_container, orient=tk.HORIZONTAL, command=canvas.xview)
scrollable_frame = tk.Frame(canvas, bg="#e8f5e9")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(xscrollcommand=scrollbar.set)

canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# Quit Button
quit_btn = tk.Button(root, text="Quit", font=("Arial", 12, "bold"),
                     bg="#FF4C4C", fg="white", relief="flat", activeforeground="white", command=root.destroy)
quit_btn.pack(pady=10)
quit_btn.bind("<Enter>", on_quit_enter)
quit_btn.bind("<Leave>", on_quit_leave)

root.mainloop()
