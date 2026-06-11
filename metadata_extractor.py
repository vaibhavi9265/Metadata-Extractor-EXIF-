import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import exifread
import os

# ---------------- FUNCTIONS ---------------- #

def select_image():
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")
        ]
    )

    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)
        show_preview(file_path)


def show_preview(path):
    try:
        img = Image.open(path)
        img.thumbnail((200, 200))

        photo = ImageTk.PhotoImage(img)

        preview_label.config(image=photo)
        preview_label.image = photo

    except Exception as e:
        messagebox.showerror("Preview Error", str(e))


def extract_metadata():
    path = entry_path.get()

    if not path:
        messagebox.showerror("Error", "Please select an image file!")
        return

    output_box.delete(1.0, tk.END)

    try:
        # BASIC INFO
        img = Image.open(path)

        file_name = os.path.basename(path)
        file_size = os.path.getsize(path) / 1024

        output_box.insert(tk.END, "========== BASIC IMAGE INFO ==========\n\n")

        output_box.insert(tk.END, f"File Name : {file_name}\n")
        output_box.insert(tk.END, f"File Size : {file_size:.2f} KB\n")
        output_box.insert(tk.END, f"Format    : {img.format}\n")
        output_box.insert(tk.END, f"Dimensions: {img.size}\n")
        output_box.insert(tk.END, f"Color Mode: {img.mode}\n\n")

        # EXIF DATA
        output_box.insert(tk.END, "========== EXIF METADATA ==========\n\n")

        with open(path, "rb") as f:
            tags = exifread.process_file(f)

            if not tags:
                output_box.insert(
                    tk.END,
                    "No EXIF metadata found!\n\n"
                )
            else:
                count = 0

                for tag in tags:
                    if tag not in (
                        "JPEGThumbnail",
                        "TIFFThumbnail",
                        "Filename",
                        "EXIF MakerNote"
                    ):
                        output_box.insert(
                            tk.END,
                            f"{tag}: {tags[tag]}\n"
                        )
                        count += 1

                output_box.insert(
                    tk.END,
                    f"\nTotal Metadata Fields: {count}"
                )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def save_report():
    data = output_box.get(1.0, tk.END)

    if not data.strip():
        messagebox.showwarning(
            "Warning",
            "No metadata available to save!"
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text File", "*.txt")]
    )

    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(data)

        messagebox.showinfo(
            "Success",
            "Report saved successfully!"
        )


def clear_output():
    output_box.delete(1.0, tk.END)
    entry_path.delete(0, tk.END)

    preview_label.config(image="")
    preview_label.image = None


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Image Metadata Extractor")
root.geometry("900x700")
root.configure(bg="#1e1e1e")

# Title

title = tk.Label(
    root,
    text="Image Metadata Extractor",
    font=("Arial", 20, "bold"),
    fg="white",
    bg="#1e1e1e"
)
title.pack(pady=15)

# File Selection Frame

file_frame = tk.Frame(root, bg="#1e1e1e")
file_frame.pack(pady=10)

entry_path = tk.Entry(
    file_frame,
    width=60,
    font=("Arial", 10)
)
entry_path.pack(side=tk.LEFT, padx=5)

browse_btn = tk.Button(
    file_frame,
    text="Browse",
    command=select_image,
    width=10
)
browse_btn.pack(side=tk.LEFT)

# Buttons Frame

btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=10)

extract_btn = tk.Button(
    btn_frame,
    text="Extract Metadata",
    command=extract_metadata,
    bg="green",
    fg="white",
    width=18
)
extract_btn.pack(side=tk.LEFT, padx=5)

save_btn = tk.Button(
    btn_frame,
    text="Save Report",
    command=save_report,
    bg="blue",
    fg="white",
    width=15
)
save_btn.pack(side=tk.LEFT, padx=5)

clear_btn = tk.Button(
    btn_frame,
    text="Clear",
    command=clear_output,
    bg="red",
    fg="white",
    width=10
)
clear_btn.pack(side=tk.LEFT, padx=5)

# Image Preview

preview_frame = tk.Frame(root, bg="#1e1e1e")
preview_frame.pack(pady=10)

preview_label = tk.Label(
    preview_frame,
    bg="#1e1e1e"
)
preview_label.pack()

# Output Box

output_box = scrolledtext.ScrolledText(
    root,
    width=100,
    height=22,
    font=("Consolas", 10)
)
output_box.pack(padx=10, pady=10)

# Run Application

root.mainloop()