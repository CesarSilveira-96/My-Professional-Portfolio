from PIL import Image, ImageFilter

# bg_img = Image.open("images/windmill_thumb.png")
water_mark = Image.open("imgs/logo.png")

# Show
# img.show()

# convert image's format
# img_rgb = img.convert("RGB")
# img_rgb.save("images/logo.jpeg")

# resize image
size1 = (60,60)
water_mark.thumbnail(size1)
water_mark.save("imgs/logo.png")

# edit images
# rotate
# img.rotate(180).save("images/windmill-rotate.png")
# edit colors
# img.convert("L").save("images/windmill-grey.png")
# img.filter(ImageFilter.GaussianBlur(10)).save("images/windmill-blur.png") # aplly filters
# adding transparency
# water_mark = Image.open("images/logo.png").convert("RGBA")
#     # split channels (R, G, B, A)
# r, g, b, a = water_mark.split()
#
#     # Adjust alpha channel: lower opacity (more transparency)
#     # Ex: multiply alpha by 0.5 → 50% transparency
# new_alpha = a.point(lambda p: int(p * 0.5))  # Values from 0 to 255
#
# # Rejoin Channels with new alpha
# water_mark_transparent = Image.merge("RGBA", (r, g, b, new_alpha))
# water_mark_transparent.save("images/logo_transparency.png")
# size_wm = (50,50)
# # water_mark_transparent.thumbnail(size_wm)
# #
# # water_mark_transparent.show()
#
#
# # Overlaying images together
# w_m = water_mark_transparent.resize(size_wm)
# # where will it be pasted
# # Obter tamanhos
# bg_w, bg_h = bg_img.size
# wm_w, wm_h = w_m.size
#
# # Calcular posição no canto inferior direito com margem (ex: 10px)
# margin = 10
# position = (bg_w - wm_w - margin, bg_h - wm_h - margin)
#
# # pasting img with transparency
# bg_img.paste(w_m, position, w_m)
# bg_img.save("images/full_img.png")
# # Show
# bg_img.show()