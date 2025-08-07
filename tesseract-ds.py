import cv2
import pytesseract
import numpy as np

# Set path Tesseract (sesuaikan dengan instalasi Anda)
pytesseract.pytesseract.tesseract_cmd = r'D:/Program Files/Tesseract-OCR/tesseract.exe'

# 1. Load gambar dengan pengecekan
img_path = "cctv.jpg"  # Ganti dengan path absolut jika perlu
img = cv2.imread(img_path)

if img is None:
    print(f"Error: Gambar tidak bisa dibaca di path: {img_path}")
    print("Pastikan:")
    print("- File ada di lokasi yang benar")
    print("- Format didukung (JPEG/PNG/BMP)")
    print("- Path tidak mengandung karakter khusus")
    exit()

print("Dimensi gambar:", img.shape)  # Harus menampilkan (height, width, channels)

# 2. Tentukan ROI (sesuaikan dengan posisi timestamp)
height, width = img.shape[:2]

# Contoh ROI untuk timestamp di bagian bawah
roi_y1 = height - 100  # Mulai 100px dari bawah
roi_y2 = height - 50   # Sampai 50px dari bawah
roi_x1 = width // 4    # Mulai 1/4 lebar
roi_x2 = 3 * width //4 # Sampai 3/4 lebar

roi = img[roi_y1:roi_y2, roi_x1:roi_x2]

if roi.size == 0:
    print("Error: ROI kosong!")
    print(f"Pastikan koordinat dalam range (0-{width}, 0-{height})")
    exit()

# 3. Preprocessing untuk timestamp CCTV
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# 4. OCR dengan konfigurasi khusus timestamp (FIXED)
config = r'--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789:-'  # Perhatikan perubahan di sini
text = pytesseract.image_to_string(thresh, config=config)
clean_text = " ".join(text.split())  # Hilangkan spasi berlebihan

print("Timestamp Terdeteksi:", clean_text)

# 5. Tampilkan hasil
cv2.imshow('ROI', roi)
cv2.imshow('Threshold', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()