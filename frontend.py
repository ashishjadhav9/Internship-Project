import customtkinter as ctk
import subprocess
from tkinter import messagebox

# Setup
ctk.set_appearance_mode("dark")   # Dark mode
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Project")
app.geometry("900x700")  # slightly larger window

# Title
title = ctk.CTkLabel(app, text="✨ Real Time Sign Detection ✨",
                     font=("Helvetica", 32, "bold"))
title.pack(pady=(20, 5))

subtitle = ctk.CTkLabel(app, text="Presented by Team OASIS",
                        font=("Helvetica", 18))
subtitle.pack(pady=(0, 30))

# Frame for cards
frame = ctk.CTkFrame(app, fg_color="transparent")
frame.pack(pady=30)

# Function to create cards
def create_card(parent, title_text, command):
    card = ctk.CTkFrame(parent, corner_radius=20, fg_color="#1e2a38")
    card.pack_propagate(False)
    card.configure(width=350, height=200)   # 🔹 bigger card

    label = ctk.CTkLabel(card, text=title_text,
                         font=("Helvetica", 20, "bold"))  # 🔹 bigger font
    label.pack(pady=(25, 15))

    btn = ctk.CTkButton(card, text="Run Project", command=command,
                        fg_color="#4CAF50", hover_color="#45a049",
                        font=("Helvetica", 16, "bold"), width=200, height=50)  # 🔹 larger button
    btn.pack(pady=10)

    return card

# Button actions
def run_project1():
    subprocess.Popen(["python", "test.py"])
    messagebox.showinfo("Running", "Real-time Sign Language Converter started!")

def run_project2():
    subprocess.Popen(["python", r"project text to sign/text_to_sign.py"])
    messagebox.showinfo("Running", "Text to Sign Converter started!")

def run_project3():
    subprocess.Popen(["python", "emotion.py"])
    messagebox.showinfo("Running", "Face Detection started!")

# Layout (2 cards in first row, 1 in second row)
row1 = ctk.CTkFrame(frame, fg_color="transparent")
row1.pack(pady=15)

card1 = create_card(row1, "Real-time Sign Language Converter", run_project1)
card1.pack(side="left", padx=30)

card2 = create_card(row1, "✍ Text to Sign Converter", run_project2)
card2.pack(side="left", padx=30)

row2 = ctk.CTkFrame(frame, fg_color="transparent")
row2.pack(pady=20)

card3 = create_card(row2, "😊 Face Detection", run_project3)
card3.pack()

# Footer
footer = ctk.CTkLabel(app, text="© 2025 Team OASIS | AI & ML Internship Project",
                      font=("Helvetica", 14))
footer.pack(side="bottom", pady=25)

app.mainloop()
