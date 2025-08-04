import cv2
import numpy as np
import pytesseract
from PIL import Image

# 1. Load gambar
image = cv2.imread("cctv.jpg")  # Ganti dengan path gambar Anda
if image is None:
    raise FileNotFoundError("Gambar tidak ditemukan!")

# 2. Crop ROI timestamp (sesuaikan koordinatnya)
# Format: roi = image[y1:y2, x1:x2]
roi = image[30:80, 100:500]  # Contoh koordinat, sesuaikan!

# 3. Preprocessing
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# 4. OCR dengan Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Sesuaikan path
text = pytesseract.image_to_string(thresh, config='--psm 6 -c tessedit_char_whitelist=0123456789-:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
clean_text = " ".join(text.split())  # Hilangkan spasi berlebihan

print("Timestamp Terdeteksi:", clean_text)

# 5. Tampilkan hasil
cv2.imshow("ROI", roi)
cv2.imshow("Threshold", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()