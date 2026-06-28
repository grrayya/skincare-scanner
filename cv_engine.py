import cv2
import mediapipe as mp
import numpy as np
import sys

def calculate_redness(face_roi) -> float:
    """Analyze the a* channel in LAB color space for inflammation."""
    lab = cv2.cvtColor(face_roi, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # The 'a' channel represents green-to-red. Higher = redder.
    # Normal skin is around 130. Acne/inflammation spikes higher.
    mean_a = np.mean(a)
    score = np.clip((mean_a - 130) / 30.0, 0.0, 1.0)
    return float(score)

def calculate_texture(face_roi) -> float:
    """Use Laplacian variance to measure skin roughness and wrinkle depth."""
    gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    
    # Laplacian detects edges. High variance = many edges (rough/wrinkled).
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    variance = laplacian.var()
    
    score = np.clip(variance / 1500.0, 0.0, 1.0)
    return float(score)

def calculate_oiliness(face_roi) -> float:
    """Detect specular highlights (shiny spots) to measure oil/sebum."""
    gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    
    # Count pixels that are extremely bright (glare from oily skin)
    _, bright_mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
    
    total_pixels = face_roi.shape[0] * face_roi.shape[1]
    oily_pixels = cv2.countNonZero(bright_mask)
    
    if total_pixels == 0: return 0.0
    
    ratio = oily_pixels / total_pixels
    score = np.clip(ratio * 15.0, 0.0, 1.0) 
    return float(score)

def process_image_with_cv(image_path: str) -> dict:
    """Load image, extract the face, and run OpenCV pixel algorithms."""
    print(f"\n[CV Engine] Booting up neural network...")
    
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(
        model_selection=1, 
        min_detection_confidence=0.5
    )

    image = cv2.imread(image_path)
    if image is None:
        print(f"\n[!] Fatal CV Error: Could not read image at '{image_path}'.")
        sys.exit(1)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    print(f"[CV Engine] Scanning for facial features...")
    results = face_detection.process(image_rgb)

    if not results.detections:
        print("\n[!] No face detected. Please try an image with clear lighting.")
        sys.exit(1)

    print("[CV Engine] ✅ Face detected! Running pixel analysis...")
    
    # 1. Extract the bounding box of the face
    detection = results.detections[0]
    bboxC = detection.location_data.relative_bounding_box
    ih, iw, _ = image.shape
    x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
    
    # Ensure coordinates are within image bounds
    x, y = max(0, x), max(0, y)
    
    # 2. Crop the image down to just the face region (Region of Interest)
    face_roi = image[y:y+h, x:x+w]

    # 3. Run the math
    detections = {
        "acne_severity": calculate_redness(face_roi),
        "dryness_level": calculate_texture(face_roi),
        "hyperpigmentation": calculate_redness(face_roi) * 0.8, # Mocked correlation for simplicity
        "wrinkle_depth": calculate_texture(face_roi) * 0.9    # Mocked correlation for simplicity
    }
    
    face_detection.close()
    return detections
