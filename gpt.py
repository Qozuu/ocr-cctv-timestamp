import cv2
import pytesseract
import numpy as np
from matplotlib import pyplot as plt

# Tentukan path Tesseract
pytesseract.pytesseract.tesseract_cmd = r"D:/Program Files/Tesseract-OCR/tesseract.exe"

def normalize_patch(img, w, h):
    """ Normalize the patch to have zero mean. """
    mean = np.mean(img)
    return img - mean

def match_pattern(roi, pattern):
    """ Perform normalized cross-correlation matching. """
    if pattern.shape[0] > roi.shape[0] or pattern.shape[1] > roi.shape[1]:
        print("Pola lebih besar dari ROI! Resize pola...")
        pattern = cv2.resize(pattern, (roi.shape[1], roi.shape[0])) 
    result = cv2.matchTemplate(roi, pattern, method=cv2.TM_CCOEFF_NORMED)
    return result

def load_patterns(font_dir):
    """ Load all digit and separator patterns from a folder. """
    import os
    patterns = {}
    for file in os.listdir(font_dir):
        if file.endswith(".png"):
            char_label = os.path.splitext(file)[0]
            pattern_img = cv2.imread(os.path.join(font_dir, file), 0)
            patterns[char_label] = pattern_img
    return patterns

def detect_timestamp(roi, patterns, threshold=0.5):
    """ Detect characters in the ROI using pattern matching. """
    h, w = list(patterns.values())[0].shape
    detections = []
    for char, pattern in patterns.items():
        match = match_pattern(roi, pattern)
        loc = np.where(match >= threshold)
        for pt in zip(*loc[::-1]):
            detections.append((pt, char, match[pt[1], pt[0]]))
    
    # Menyusun teks berdasarkan deteksi karakter
    detected_text = ''.join([char for _, char, _ in sorted(detections, key=lambda x: (x[0][1], x[0][0]))])
    return detected_text, detections

def visualize_matches(roi, detections):
    """ Display matched characters on the ROI. """
    vis = cv2.cvtColor(roi.copy(), cv2.COLOR_GRAY2BGR)
    for (x, y), char, score in detections:
        cv2.rectangle(vis, (x, y), (x + 16, y + 24), (0, 255, 0), 1)
        cv2.putText(vis, char, (x, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    plt.imshow(vis)
    plt.title("Detected Characters")
    plt.axis("off")
    plt.show()

# ====== Contoh Penggunaan ======
# Membaca gambar
frame = cv2.imread('cctv.jpg', 0)

# Tentukan ROI secara manual (jika perlu)
x, y, w, h = 0, 0, 600, 100
roi = frame[y:y+h, x:x+w] # Menggunakan seluruh gambar karena hanya ada timestamp

# Muat pola dari folder
patterns = load_patterns("fonts")

# Deteksi timestamp
detected_text, results = detect_timestamp(roi, patterns)
print("Detected Text:", detected_text)

# Visualisasi hasil deteksi
visualize_matches(roi, results)

# Menggunakan Tesseract untuk mengekstrak teks dari ROI yang telah dipotong (timestamp)
timestamp = pytesseract.image_to_string(roi)

# Menampilkan hasil deteksi teks
print("Timestamp yang terdeteksi:", timestamp)