import pytesseract
import cv2

# Tentukan path Tesseract
pytesseract.pytesseract.tesseract_cmd = r"D:/Program Files/Tesseract-OCR/tesseract.exe"  # Sesuaikan dengan path Tesseract di sistemmu

# Fungsi untuk mendeteksi timestamp
def detect_timestamp(image, roi=(0, 0, 600, 100)):
    # Potong ROI untuk timestamp
    timestamp_roi = image[roi[1]:roi[3], roi[0]:roi[2]]
    
    # Gunakan Tesseract untuk membaca timestamp
    timestamp_text = pytesseract.image_to_string(timestamp_roi, config='--psm 6')  # --psm 6 untuk satu blok teks
    return timestamp_text.strip()

# Membaca gambar
image = cv2.imread('cctv.jpg')

# Tentukan area (kotak) di mana timestamp berada (kiri, atas, kanan, bawah).
# Format: (x, y, w, h)
# Sesuaikan nilai-nilai ini dengan posisi timestamp dalam gambar.
timestamp_area = (0, 0, 600, 100)  # Sesuaikan dengan posisi dan ukuran timestamp

# Deteksi timestamp dari gambar
timestamp = detect_timestamp(image, roi=timestamp_area)
print(f"Timestamp yang terdeteksi: {timestamp}")

# Menampilkan gambar untuk verifikasi
cv2.imshow('Detected Timestamp', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
