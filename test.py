import cv2
import numpy as np
import math
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
from threading import Thread

# ===== MODEL SETTINGS =====
offset = 20
imgSize = 300
labels = ["A", "B", "C", "D","E","F", "G", "H", "I", "J","K","L","M","N"]
labels1=["O","P","Q","R","S","T","U","V","W","X","Y","Z","SPACE","DELETE"]
labels2=["D","I","L"]


# ===== MODEL LOAD =====
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model(AN).h5", "Model/labels(AN).txt")
classifier1 = Classifier("Model1/keras_model(OZ).h5", "Model1/labels(OZ).txt")
classifier2 = Classifier("Model2/keras_model(DIL).h5", "Model2/labels(DIL).txt")

# ===== THREADING CAMERA READER =====
class VideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.grabbed, self.frame = self.stream.read()
        self.stopped = False
        Thread(target=self.update, args=(), daemon=True).start()

    def update(self):
        while not self.stopped:
            self.grabbed, self.frame = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.stream.release()

# ===== TKINTER MAIN WINDOW =====
root = tk.Tk()
root.title("Real-Time Sign Language Recognition")

# Webcam display
lmain = tk.Label(root)
lmain.grid(row=0, column=0, columnspan=3)

# Text box for output
text_box = tk.Text(root, height=5, width=50, font=("Arial", 14))
text_box.grid(row=1, column=0, columnspan=3, pady=10)

# ===== BUTTON FUNCTIONS =====
def clear_text():
    global sentence
    sentence = ""
    text_box.delete("1.0", tk.END)

def save_to_file():
    content = text_box.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Empty", "No text to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Text saved to {file_path}")

def quit_app():
    try:
        cap.stop()
    except:
        pass
    root.destroy()
    cv2.destroyAllWindows()

# === NEW FUNCTION: Show ASL Alphabet Chart in a new window ===
def show_asl_chart():
    try:
        chart_window = tk.Toplevel(root)
        chart_window.title("ASL Alphabet Chart")

        # Load and resize the image
        asl_img = Image.open("asl_alphabet.jpg")  # Change path if needed
        asl_img = asl_img.resize((500, 600), Image.LANCZOS)
        asl_img_tk = ImageTk.PhotoImage(asl_img)

        # Show the image
        lbl = tk.Label(chart_window, image=asl_img_tk)
        lbl.image = asl_img_tk  # Keep reference
        lbl.pack(padx=10, pady=10)

        # Close button
        tk.Button(chart_window, text="Close", command=chart_window.destroy,
                  bg="red", fg="white", font=("Arial", 12)).pack(pady=5)

    except Exception as e:
        messagebox.showerror("Image Error", f"Could not load ASL chart:\n{e}")

# Buttons
tk.Button(root, text="Clear All", command=clear_text, bg="yellow", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
tk.Button(root, text="Save to a Text File", command=save_to_file, bg="lightgreen", font=("Arial", 12)).grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Quit", command=quit_app, bg="red", fg="white", font=("Arial", 12)).grid(row=2, column=2, padx=5, pady=5)

# New button to open ASL chart
tk.Button(root, text="Show ASL Chart", command=show_asl_chart,
          bg="lightblue", font=("Arial", 12)).grid(row=4, column=0, columnspan=3, pady=5)

# ===== CAMERA SETUP =====
phone_url = "http://10.110.83.37:8080/video"  # Change to your phone's URL
cap = VideoStream(phone_url)
if cap.read() is None:
    print("⚠ Phone camera not found, switching to laptop webcam...")
    cap = VideoStream(0)

# Variables for sentence & delay logic
sentence = ""
last_letter = ""
frame_buffer = 0
required_frames = 9

def show_frame():
    global sentence, last_letter, frame_buffer
    img = cap.read()
    if img is None:
        root.after(10, show_frame)
        return

    imgOutput = img.copy()
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        x1 = max(0, x - offset)
        y1 = max(0, y - offset)
        x2 = min(img.shape[1], x + w + offset)
        y2 = min(img.shape[0], y + h + offset)

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y1:y2, x1:x2]

        if imgCrop.size != 0:
            aspectRatio = h / w
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize

            prediction1, index1 = classifier.getPrediction(imgWhite, draw=False)
            prediction2, index2 = classifier1.getPrediction(imgWhite, draw=False)
            prediction3, index3 = classifier2.getPrediction(imgWhite, draw=False)

            # Compare confidence and choose best
            if prediction1[index1] > prediction2[index2]:
                letter = labels[index1]  # From A-E
            elif prediction2[index2]>prediction3[index3]:
                letter = labels1[index2]
    
            else:
                letter = labels2[index3]  # From F-J

            if letter == last_letter:
                frame_buffer += 1
            else:
                frame_buffer = 0
                last_letter = letter

            if frame_buffer == required_frames:
                if letter == "SPACE":
                    sentence += " "
                elif letter == "DELETE":
                    sentence = sentence[:-1]  # remove last character
                else:
                    sentence += letter

                # update text box
                text_box.delete("1.0", tk.END)
                text_box.insert(tk.END, sentence)

            cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                          (x - offset + 90, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
            cv2.putText(imgOutput, letter, (x, y - 26), cv2.FONT_HERSHEY_COMPLEX,
                        1.7, (255, 255, 255), 2)
            cv2.rectangle(imgOutput, (x - offset, y - offset),
                          (x + w + offset, y + h + offset), (255, 0, 255), 4)

    imgRGB = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)
    imgRGB = Image.fromarray(imgRGB)
    imgtk = ImageTk.PhotoImage(image=imgRGB)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    root.after(5, show_frame)  # Faster update

show_frame()
root.mainloop()
