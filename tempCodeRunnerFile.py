import os
import sqlite3
from datetime import datetime

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk

from predict import predict_image


# ================= STATE =================
current_prediction = None
current_confidence = None


# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BG_PATH = os.path.join(BASE_DIR, "assets", "cloud1.png")


# ================= DATABASE =================
conn = sqlite3.connect("cloud_history.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    prediction TEXT,
    confidence REAL
)
""")

conn.commit()


def save_to_db(prediction, confidence):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO history (timestamp, prediction, confidence)
        VALUES (?, ?, ?)
    """, (now, prediction, confidence))

    conn.commit()


# ================= SAVE =================
def save_current_prediction():
    global current_prediction, current_confidence

    if current_prediction is None:
        result_label.config(text="No prediction yet ⚠")
        return

    save_to_db(current_prediction, current_confidence)
    result_label.config(text="Saved to journal ✔")


# ================= JOURNAL =================
def open_history_window():
    win = tk.Toplevel(root)
    win.title("Cloud Journal")
    win.geometry("700x400")
    win.configure(bg="#0f0f0f")

    tk.Label(
        win,
        text="☁ Cloud Journal",
        font=("Castellar", 16),
        bg="#0f0f0f",
        fg="#aec9e6"
    ).pack(pady=10)

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("time", "cloud", "conf"), show="headings")

    tree.heading("time", text="Time")
    tree.heading("cloud", text="Cloud Type")
    tree.heading("conf", text="Confidence")

    tree.column("time", width=220)
    tree.column("cloud", width=200)
    tree.column("conf", width=100)

    cursor.execute("""
        SELECT timestamp, prediction, confidence
        FROM history
        ORDER BY id DESC
    """)

    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

    tree.pack(fill="both", expand=True)


# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("Cloud Monitoring Diary")
root.geometry("900x650")
root.resizable(False, False)


# ================= BACKGROUND =================
canvas = tk.Canvas(root, width=900, height=650, highlightthickness=0)
canvas.place(x=0, y=0)

bg_image = Image.open(BG_PATH)
bg_image = bg_image.resize((900, 650))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas.create_image(0, 0, image=bg_photo, anchor="nw")
canvas.bg_photo = bg_photo


# ================= MAIN LAYOUT =================
main_frame = tk.Frame(root, bg="#0f0f0f")
canvas.create_window(450, 325, window=main_frame)


# ================= TITLE =================
title = tk.Label(
    main_frame,
    text="☁ Cloud Monitoring Diary 🌩️",
    font=("Old English Text MT", 35, "bold"),
    bg="#0f0f0f",
    fg="#828EA3"
)
title.pack(pady=10)


# ================= CONTENT =================
content = tk.Frame(main_frame, bg="#0f0f0f")
content.pack()

left = tk.Frame(content, bg="#0f0f0f")
left.pack(side="left", padx=40)

right = tk.Frame(content, bg="#0f0f0f")
right.pack(side="right", padx=40)


# ================= IMAGE =================
image_label = tk.Label(left, bg="#0f0f0f")
image_label.pack(pady=20)


# ================= RESULT =================
result_label = tk.Label(
    right,
    text="upload an image to start",
    font=("Castellar", 18),
    bg="#0f0f0f",
    fg="#aec9e6"
)
result_label.pack(pady=10)


# ================= SAVE BUTTON =================
save_btn = tk.Button(
    right,
    text="📝 Save to Journal",
    command=save_current_prediction,
    font=("Castellar", 12),
    bg="#445566",
    fg="white",
    relief="flat"
)
save_btn.pack(pady=10)   # 👈 ВСЕГДА ВИДНА


# ================= UPLOAD =================
def upload_image():
    global current_prediction, current_confidence

    file_path = filedialog.askopenfilename()

    if file_path:
        img = Image.open(file_path)
        img = img.resize((350, 350))

        img_tk = ImageTk.PhotoImage(img)

        image_label.configure(image=img_tk)
        image_label.image = img_tk

        prediction, confidence = predict_image(file_path)

        current_prediction = prediction
        current_confidence = confidence

        result_label.config(
            text=f"{prediction}\nConfidence: {confidence:.1f}%"
        )


# ================= BUTTONS =================
upload_btn = tk.Button(
    right,
    text="📁 Upload Image",
    command=upload_image,
    font=("Castellar", 14),
    bg="#50606b",
    fg="white",
    padx=20,
    pady=10,
    relief="flat"
)
upload_btn.pack(pady=20)


history_btn = tk.Button(
    right,
    text="📖 Open Journal",
    command=open_history_window,
    font=("Castellar", 12),
    bg="#303b45",
    fg="white",
    relief="flat"
)
history_btn.pack(pady=5)


# ================= RUN =================
root.mainloop()