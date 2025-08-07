from PIL import Image, ImageDraw, ImageFont
import os

# Load font
font_path = 'digital-7.regular.ttf'
font_size = 50
font = ImageFont.truetype(font_path, font_size)

# Folder untuk menyimpan gambar karakter
output_folder = "fonts"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Daftar karakter yang akan dipotong (sesuaikan dengan yang ada di gambar)
characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.:!?-"

# Membuat gambar untuk setiap karakter
for idx, char in enumerate(characters):
    # Buat gambar kosong
    img = Image.new('L', (font_size, font_size), color=255)  # 'L' untuk grayscale
    draw = ImageDraw.Draw(img)
    
    # Menggambar karakter pada gambar
    draw.text((5, 5), char, font=font, fill=0)  # posisi (x, y) untuk menggambar
    
    # Simpan gambar karakter
    img_filename = os.path.join(output_folder, f"{char}.png")
    img.save(img_filename)
    print(f"Gambar karakter '{char}' disimpan di: {img_filename}")
