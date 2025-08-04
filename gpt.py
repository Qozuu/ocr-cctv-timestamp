import cv2
import numpy as np
from matplotlib import pyplot as plt

def normalize_patch(img, w, h):
    """ Normalize the patch to have zero mean. """
    mean = np.mean(img)
    return img - mean

def match_pattern(roi, pattern):
    """ Perform normalized cross-correlation matching. """
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

    return sorted(detections, key=lambda x: (x[0][1], x[0][0]))

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

# ==== Contoh penggunaan ====
# 1. Ambil ROI dari frame video CCTV
# 2. Load font pattern dari direktori ("fonts/")
# 3. Jalankan matching dan visualisasi

frame = cv2.imread('cctv.jpg', 0)

x, y, w, h = 50, 50, 400, 100
roi = frame[y:y+h, x:x+w]  # Tentukan ROI secara manual

patterns = load_patterns("fonts")
results = detect_timestamp(roi, patterns)
visualize_matches(roi, results)
