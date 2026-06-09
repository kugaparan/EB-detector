# EB Detector

> A lightweight object-detection app: upload a photo, run inference with a custom-trained model, and get back an annotated image plus a JSON report.

<!-- TODO: replace "EB" / "[object]" throughout with what your model actually detects. -->

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![Model](https://img.shields.io/badge/Model-Roboflow-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## Demo

<!-- Drop a screenshot or GIF here once you have one (see DEMO TIPS in the publishing guide). -->
<p align="center">
  <img src="https://github.com/user-attachments/assets/d88c83ea-1468-4c37-b6d1-8202d9ea0ccd" alt="EB Detector result" width="400">
</p>

*The app draws a bounding box and confidence score around each detected EMPTY BUNCH OF PALM FRUIT, and flags **CODE RED** when confidence exceeds 85%.*

## What it does

You run the script, a file dialog opens, you pick a photo, and the app:

1. Sends the image to a custom-trained detection model hosted on Roboflow.
2. Draws bounding boxes with confidence scores on every detection.
3. Raises a **CODE RED** banner when any detection clears the 85% confidence threshold.
4. Saves an annotated `*_result.jpg` and a machine-readable `*_result.json` next to the original photo.

## Tech stack

- **Python** — core application
- **OpenCV** — image decoding, drawing, and display
- **Roboflow** — hosted inference for the custom-trained model
- **Tkinter** — native file-upload dialog
- **requests** — HTTP calls to the inference API

## Getting started

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/eb-detector.git
cd eb-detector
pip install -r requirements.txt
```

### 2. Set your Roboflow API key

The key is read from an environment variable so it never ends up in the repo.

**Windows (PowerShell)**
```powershell
setx ROBOFLOW_API_KEY "your_key_here"
```
(restart the terminal after running `setx`)

**macOS / Linux**
```bash
export ROBOFLOW_API_KEY="your_key_here"
```

You can find your key in the Roboflow dashboard under your workspace settings.

### 3. Run

```bash
python eb_detector.py
```

Pick an image in the dialog. The annotated result opens in a window and is saved alongside the original file.

## How it works

```
photo ──▶ Roboflow model ──▶ predictions ──▶ OpenCV draws boxes ──▶ annotated.jpg + results.json
```

Each prediction returns a center point (`x`, `y`), a `width`/`height`, a `confidence`, and a `class`. The app converts the center box to corner coordinates, draws the rectangle and label, and writes everything to JSON.

## Model

- **Task:** object detection
- **Classes:** `EB` <!-- list your real classes -->
- **Training images:** [N] <!-- fill in -->
- **mAP / precision / recall:** [fill in from your Roboflow training page]
- **Platform:** Roboflow (custom-trained)

## Project structure

```
eb-detector/
├── eb_detector.py      # main app: upload → detect → annotate → save
├── requirements.txt    # Python dependencies
├── .env.example        # template for your API key
├── .gitignore
├── LICENSE
└── README.md
```

## Roadmap

- [ ] Batch mode: process an entire folder of images at once
- [ ] Web demo (Gradio / Streamlit) so anyone can try it in the browser
- [ ] Export detections to CSV for analysis
- [ ] Confidence threshold as a command-line argument

## License

Released under the MIT License — see [LICENSE](LICENSE).

## Author

**Kugaparan** — [LinkedIn](https://www.linkedin.com/in/kugaparan) · [GitHub](https://github.com/kugaparan)
