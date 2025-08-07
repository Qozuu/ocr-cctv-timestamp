import pytesseract
import cv2
import numpy as np

# Tentukan path Tesseract
pytesseract.pytesseract.tesseract_cmd = r"D:/Program Files/Tesseract-OCR/tesseract.exe"  # Sesuaikan dengan path Tesseract di sistemmu

def detect_timestamp(image_path, crop_box=None):
    try:
        # Membaca gambar menggunakan OpenCV
        image = cv2.imread(image_path)
        
        if image is None:
            return f"Error: Gagal membaca gambar dari path '{image_path}'."

        # Jika crop_box disediakan, potong gambar
        if crop_box:
            x, y, w, h = crop_box[0], crop_box[1], crop_box[2], crop_box[3]
            # Pastikan koordinat valid sebelum memotong
            if x >= 0 and y >= 0 and x+w <= image.shape[1] and y+h <= image.shape[0]:
                image = image[y:y+h, x:x+w]
            else:
                return "Error: Koordinat crop_box tidak valid."

        # --- Pra-pemrosesan Gambar untuk Meningkatkan Akurasi OCR ---
        # 1. Konversi ke skala abu-abu
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 2. Gunakan Canny Edge Detection untuk membantu meningkatkan kontras gambar
        edges = cv2.Canny(gray_image, 100, 200)

        # 3. Gunakan adaptive thresholding yang lebih lembut
        adaptive_thresh_image = cv2.adaptiveThreshold(edges, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                                     cv2.THRESH_BINARY_INV, 11, 2)

        # 4. Resize gambar untuk memperbesar teks
        rescaled_image = cv2.resize(adaptive_thresh_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # Menampilkan gambar yang diproses untuk verifikasi
        cv2.imshow("Processed Image", rescaled_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Konfigurasi Tesseract
        config = '--psm 6 --oem 3'  # --psm 6 untuk teks yang teratur dalam satu blok
        # Lakukan OCR pada gambar yang telah diproses
        raw_text = pytesseract.image_to_string(rescaled_image, config=config)
        cleaned_text = raw_text.strip()

        return cleaned_text
    
    except FileNotFoundError:
        return f"Error: File '{image_path}' tidak ditemukan."
    except Exception as e:
        return f"Terjadi kesalahan: {e}"

if __name__ == "__main__":
    # Ganti dengan path ke gambar Anda
    image_file = 'cctv.jpg'

    # Tentukan area (kotak) di mana timestamp berada (kiri, atas, kanan, bawah).
    # Format: (x, y, w, h)
    # Sesuaikan nilai-nilai ini dengan posisi timestamp dalam gambar.
    timestamp_area = (0, 0, 600, 100)  # Sesuaikan dengan posisi dan ukuran timestamp

    print(f"Mendeteksi timestamp dari gambar: {image_file}...")

    # Panggil fungsi untuk mendeteksi timestamp
    extracted_timestamp = detect_timestamp(image_file, crop_box=timestamp_area)
    
    # Tampilkan hasilnya
    if extracted_timestamp:
        print(f"Timestamp yang terdeteksi: '{extracted_timestamp}'")
    else:
        print("Tidak ada teks timestamp yang terdeteksi.")
        
    print("\n--- Panduan Pemecahan Masalah ---")
    print("1. Jika 'Tidak terdeteksi', ubah koordinat 'timestamp_area' (x, y, w, h).")
    print("2. Pastikan Tesseract sudah terinstal dengan benar.")
