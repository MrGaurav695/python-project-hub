# 🖼️ Background Remover

Remove the background from an image using Python and the `rembg` library.

## Features

- Remove backgrounds automatically
- Supports JPG, JPEG, PNG, and WebP images
- Saves the output as a transparent PNG
- Simple command-line interface

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Example

Input:
```
Enter input image name: car.jpg
```

Output:
```
Enter output image name: car_no_bg.png
```

Result:
```
✅ Background removed successfully!
📁 Saved as: car_no_bg.png
```

## Technologies Used

- Python
- rembg
- Pillow
- ONNX Runtime