import cv2
from deepface import DeepFace
import customtkinter as ctk
from PIL import Image, ImageTk

# ---------- Function for advice ----------
def give_advice(emotion):
    if emotion == "angry":
        return "Take a deep breath. Stay calm. Try solving problems step by step."
    elif emotion == "sad":
        return "Don't worry, things will get better. Talk to a friend, listen to music, or go for a walk."
    elif emotion == "happy":
        return "Keep smiling, happiness looks good on you! Spread positivity around."
    else:
        return "Stay positive, everything will be okay."

# ---------- Globals ----------
running = False
emotion = "neutral"
advice = "Press Start to begin."
cap = None
frame_count = 0

# ---------- Camera Start ----------
def start_camera():
    global running, cap
    running = True

    # Get user choice
    choice = camera_choice.get()
    if choice == "Laptop Webcam":
        cap = cv2.VideoCapture(0)  # Laptop webcam
    else:
        # 📱 Change IP address to your actual phone IP Webcam stream
        url = "http://10.110.83.37:8080/video"
        cap = cv2.VideoCapture(url)

    update_frame()

def stop_camera():
    global running, cap
    running = False
    if cap:
        cap.release()
    video_label.configure(image='')

def update_frame():
    global cap, emotion, advice, frame_count

    if running and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame_count += 1

            # Resize for speed
            frame = cv2.resize(frame, (640, 480))

            # Analyze every 10th frame
            if frame_count % 10 == 0:
                try:
                    result = DeepFace.analyze(
                        frame,
                        actions=['emotion'],
                        enforce_detection=False,
                        detector_backend="opencv"
                    )
                    emotion = result[0]['dominant_emotion']
                    advice = give_advice(emotion)
                except Exception as e:
                    print("Error:", e)

            # Convert frame to Tkinter image
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)

            # Update text
            emotion_label.configure(text=f"Emotion: {emotion}")
            advice_label.configure(text=f"Advice: {advice}")

    if running:
        app.after(50, update_frame)

# ---------- GUI ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Fast Emotion Detector (Webcam / IP Webcam)")
app.geometry("900x750")

title_label = ctk.CTkLabel(app, text="😊 Emotion Detector + Advice", font=("Arial", 28, "bold"))
title_label.pack(pady=15)

# Camera selection dropdown
camera_choice = ctk.StringVar(value="Laptop Webcam")
camera_menu = ctk.CTkOptionMenu(app, variable=camera_choice, values=["Laptop Webcam", "Mobile IP Webcam"])
camera_menu.pack(pady=10)

video_label = ctk.CTkLabel(app, text="", width=800, height=400, fg_color="black")
video_label.pack(pady=10)

emotion_label = ctk.CTkLabel(app, text="Emotion: ---", font=("Arial", 20))
emotion_label.pack(pady=10)

advice_label = ctk.CTkLabel(app, text="Advice: ---", font=("Arial", 16), wraplength=700)
advice_label.pack(pady=10)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=20)

start_btn = ctk.CTkButton(button_frame, text="▶ Start", command=start_camera, width=120)
start_btn.grid(row=0, column=0, padx=20)

stop_btn = ctk.CTkButton(button_frame, text="⏹ Stop", command=stop_camera, width=120, fg_color="red")
stop_btn.grid(row=0, column=1, padx=20)

app.mainloop()