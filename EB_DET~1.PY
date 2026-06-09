"""
EB Detector — upload a photo, run object detection, get annotated results.

Usage:
    1. Set your Roboflow API key as an environment variable:
         Windows (PowerShell):  setx ROBOFLOW_API_KEY "your_key_here"
         macOS/Linux:           export ROBOFLOW_API_KEY="your_key_here"
    2. Run:  python eb_detector.py
    3. Pick a photo in the file dialog. Results are saved next to the original.
"""

import cv2
import requests
import json
import os
import tkinter as tk
from tkinter import filedialog

# Read the API key from the environment — never hard-code secrets in a public repo.
API_KEY = os.environ.get("ROBOFLOW_API_KEY")
MODEL_URL = "https://serverless.roboflow.com/eb_detector/2"

CONF_RED = 0.85  # confidence threshold for "CODE RED"


def detect(frame):
    """Send an image to Roboflow and return the list of predictions."""
    _, img_encoded = cv2.imencode(".jpg", frame)
    response = requests.post(
        MODEL_URL,
        params={"api_key": API_KEY},
        files={"file": ("image.jpg", img_encoded.tobytes(), "image/jpeg")},
    )
    data = response.json()
    return data.get("predictions", [])


def draw(frame, predictions):
    """Draw boxes/labels on the image. Returns True if any detection is CODE RED."""
    code_red = False
    for p in predictions:
        x, y = int(p["x"]), int(p["y"])
        w, h = int(p["width"]), int(p["height"])
        conf = p["confidence"]

        x1, y1 = x - w // 2, y - h // 2
        x2, y2 = x + w // 2, y + h // 2

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame, f"EB {conf*100:.1f}%", (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2,
        )
        if conf > CONF_RED:
            code_red = True

    if code_red:
        cv2.putText(
            frame, "CODE RED", (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3,
        )
    return code_red


def main():
    if not API_KEY:
        raise SystemExit(
            "ROBOFLOW_API_KEY is not set. See the README for setup instructions."
        )

    # Open a file-picker dialog to upload a photo
    root = tk.Tk()
    root.withdraw()  # hide the empty tk window
    path = filedialog.askopenfilename(
        title="Select a photo to detect",
        filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.webp"), ("All files", "*.*")],
    )
    if not path:
        print("No file selected.")
        return

    frame = cv2.imread(path)
    if frame is None:
        print(f"Could not read image: {path}")
        return

    predictions = detect(frame)
    code_red = draw(frame, predictions)

    # Print results
    print(f"\nImage: {os.path.basename(path)}")
    print(f"Detections: {len(predictions)}")
    if code_red:
        print("!!! CODE RED !!!")
    for i, p in enumerate(predictions, 1):
        print(f"  {i}. {p.get('class', 'EB')}  confidence={p['confidence']*100:.1f}%")

    # Save annotated image + JSON next to the original
    base, _ = os.path.splitext(path)
    out_img = base + "_result.jpg"
    out_json = base + "_result.json"
    cv2.imwrite(out_img, frame)
    with open(out_json, "w") as f:
        json.dump(
            {
                "image": os.path.basename(path),
                "detections": len(predictions),
                "code_red": code_red,
                "predictions": predictions,
            },
            f, indent=2,
        )
    print(f"\nSaved: {out_img}")
    print(f"Saved: {out_json}")

    # Show the annotated image (press any key to close)
    cv2.imshow("EB Detector - Result", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
