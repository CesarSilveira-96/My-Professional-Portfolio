from PIL import  ImageDraw, ImageFont
import PIL.Image as PilImg
from tkinter import *
from tkinter import filedialog, messagebox

base_img_path = None
logo_img_path = None

def upload_image():
    global base_img_path
    base_img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if base_img_path:
        messagebox.showinfo("Success", "Image was successfully uploaded!")

def upload_logo():
    global logo_img_path
    logo_img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
    if base_img_path:
        messagebox.showinfo("Success", "Logo was successfully uploaded!")

def add_watermark():
    if not base_img_path:
        messagebox.showerror("Error", "Please select a base image.")
        return

    bg_img = PilImg.open(base_img_path).convert("RGBA")
    bg_w, bg_h = bg_img.size
    draw = ImageDraw.Draw(bg_img)

    # Adding text
    text = watermark_text.get()
    if text:
        try:
            font = ImageFont.truetype("arial.ttf", size=int(bg_h * 0.05))
        except:
            font = ImageFont.load_default()

        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        position = (bg_w - text_w - 10, bg_h - text_h - 10)
        draw.text(position, text, font=font, fill=(255, 255, 255, 180))

    # Adding logo/water mark image
    if logo_img_path:
        watermark = PilImg.open(logo_img_path).convert("RGBA")
        r, g, b, a = watermark.split()
        new_alpha = a.point(lambda p: int(p * 0.5))
        transparent_logo = PilImg.merge("RGBA", (r, g, b, new_alpha))

        wm_width = int(bg_w * 0.2)
        aspect_ratio = transparent_logo.height / transparent_logo.width
        wm_height = int(wm_width * aspect_ratio)
        resized_logo = transparent_logo.resize((wm_width, wm_height))

        position = (bg_w - wm_width - 10, bg_h - wm_height - 10)
        bg_img.paste(resized_logo, position, resized_logo)

    # Save the final image
    save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png")])
    if save_path:
        bg_img.save(save_path)
        messagebox.showinfo("Sucesso", "Imagem salva com marca d'água!")
        bg_img.show()

# >>>>>>>>>> TK Interface <<<<<<<<<<<
window = Tk()
window.title("Water Mark'd")
window.config(pady=50,padx=50,bg="white")

try:
    logo_img = PhotoImage(file="imgs/logo.png")
    logo_canvas = Canvas(window, width=60, height=60, bg="white", highlightthickness=0)
    logo_canvas.create_image(30, 30, image=logo_img)
    logo_canvas.grid(row=0, column=0, columnspan=3)
except:
    pass

# Labels
title_label = Label(text="Water Marky", font=("Arial", 22, "bold"), bg="white")
title_label.grid(row= 1, column= 0, columnspan=3, pady=(10, 20))

wm_label = Label(text="Water Mark Text", font=("Arial", 11), bg="white")
wm_label.grid(row=3, column=0, pady=10, sticky=E)

# Entries
watermark_text = Entry(width=30, font=("Arial", 10))
watermark_text.grid(row=3, column=2, padx=10)

# Buttons
btn_style={"font": ("Arial", 11), "bg": "#f0f0f0", "padx": 10, "pady": 6}

upload_img_btn = Button(text="Upload Image", width=15, command=upload_image, **btn_style)
upload_img_btn.grid(row=2, column=0, padx=10, pady=5)

upload_logo_btn = Button(text="Upload Logo", width=15, command=upload_logo, **btn_style)
upload_logo_btn.grid(row=2, column=2, padx=0, pady=5)

add_btn = Button(text="Add Water Mark",font=("Arial", 12, "bold"), width=40, bg="#d6eaff", command=add_watermark )
add_btn.grid(row=4, column=0, columnspan=3, pady=30)

window.mainloop()