import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Cloud Monitoring Diary")
root.geometry("900x650")
root.configure(bg="#000000")
root.resizable(False, False)

# ===== CLOUDS (ДЕКОР) =====
from PIL import Image, ImageTk

# ===== CLOUD 1 =====
cloud1_img = Image.open("assets/cloud1.png")
cloud1_img.thumbnail((120, 120))
cloud1_photo = ImageTk.PhotoImage(cloud1_img)

cloud1 = tk.Label(root, image=cloud1_photo, bg="#000000", border=0)
cloud1.place(x=40, y=120)
cloud1.image = cloud1_photo

# ===== CLOUD 2 =====
cloud2_img = Image.open("assets/cloud1.png")
cloud2_img.thumbnail((180, 180))   # ДРУГОЙ РАЗМЕР
cloud2_photo = ImageTk.PhotoImage(cloud2_img)

cloud2 = tk.Label(root, image=cloud2_photo, bg="#000000", border=0)
cloud2.place(x=720, y=180)
cloud2.image = cloud2_photo

# ===== CLOUD 3 =====
cloud3_img = Image.open("assets/cloud1.png")
cloud3_img.thumbnail((160, 160))
cloud3_photo = ImageTk.PhotoImage(cloud3_img)

cloud3 = tk.Label(root, image=cloud3_photo, bg="#000000", border=0)
cloud3.place(x=110, y=260)  # чуть левее, безопаснее

cloud3.image = cloud3_photo

# ===== CLOUD 4 =====
cloud4_img = Image.open("assets/cloud1.png")
cloud4_img.thumbnail((110, 110))
cloud4_photo = ImageTk.PhotoImage(cloud4_img)

cloud4 = tk.Label(root, image=cloud4_photo, bg="#000000", border=0)
cloud4.place(x=650, y=380)

cloud4.image = cloud4_photo


# ===== CLOUD 5 =====
cloud5_img = Image.open("assets/cloud1.png")
cloud5_img.thumbnail((130, 130))
cloud5_photo = ImageTk.PhotoImage(cloud5_img)

cloud5 = tk.Label(root, image=cloud5_photo, bg="#000000", border=0)
cloud5.place(x=100, y=420)

cloud5.image = cloud5_photo
# ===== TITLE =====
title = tk.Label(
    root,
    text="☁ Cloud Monitoring Diary 🌩️",
    font=("Old English Text MT", 43, "bold"),
    bg="#000000",
    fg="#828EA3"
)
title.pack(pady=15)

# ===== IMAGE DISPLAY (УБРАЛИ БЕЛЫЙ FRAME) =====
image_label = tk.Label(root, bg="#000000")
image_label.pack(pady=20)

# ===== RESULT LABEL =====
result_label = tk.Label(
    root,
    text="upload an image to start",
    font=("Castellar", 20),
    bg="#000000",
    fg="#aec9e6"
)
result_label.pack(pady=10)

# ===== FUNCTION =====
def upload_image():
    file_path = filedialog.askopenfilename()

    if file_path:
        img = Image.open(file_path)
        img = img.resize((350, 350))

        img_tk = ImageTk.PhotoImage(img)

        image_label.configure(image=img_tk)
        image_label.image = img_tk

        result_label.config(text="Image loaded ✔ (prediction later)")

# ===== BUTTON =====
upload_btn = tk.Button(
    root,
    text="📁 upload Image",
    command=upload_image,
    font=("Castellar", 14),
    bg="#50606b",
    fg="white",
    padx=20,
    pady=10,
    relief="flat"
)

upload_btn.pack(pady=20)

root.mainloop()