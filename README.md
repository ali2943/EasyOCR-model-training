# EasyOCR Image-to-Text Model

This project implements an OCR (Optical Character Recognition) model using the EasyOCR approach to convert images containing text into machine-readable text.

## Features

- 🖼️ Convert images to text using state-of-the-art EasyOCR
- 📝 Extract text with confidence scores
- 🎯 Draw bounding boxes around detected text
- 🌍 Support for multiple languages
- 🚀 Easy-to-use API
- 💻 Works with both CPU and GPU

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ali2943/EasyOCR-model-training.git
cd EasyOCR-model-training
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Generate a Sample Image
```bash
python generate_sample_image.py
```

### Run the Demo
```bash
python demo.py sample_images/sample_text.jpg
```

### Use in Your Code

```python
from src.easy_ocr_model import EasyOCRModel

# Initialize the model
model = EasyOCRModel(languages=['en'], gpu=False)

# Read text from an image
results = model.read_image('path/to/your/image.jpg')

# Get only the text
text_list = model.extract_text_only('path/to/your/image.jpg')

# Get concatenated text
full_text = model.get_full_text('path/to/your/image.jpg')

# Get text with confidence scores
text_with_conf = model.get_text_with_confidence('path/to/your/image.jpg')

# Draw bounding boxes and save
model.draw_bounding_boxes('path/to/image.jpg', 'output/annotated.jpg')
```

## API Reference

### EasyOCRModel

Main class for performing OCR on images.

#### `__init__(languages=['en'], gpu=False)`
Initialize the EasyOCR model.
- **languages**: List of language codes (default: ['en'])
- **gpu**: Whether to use GPU (default: False)

#### `read_image(image_path)`
Read text from an image file.
- **Returns**: List of tuples (bounding_box, text, confidence)

#### `extract_text_only(image_path)`
Extract only the text content.
- **Returns**: List of text strings

#### `get_full_text(image_path, separator=' ')`
Get all text as a single concatenated string.
- **Returns**: Full text string

#### `get_text_with_confidence(image_path)`
Get text with confidence scores.
- **Returns**: List of tuples (text, confidence)

#### `draw_bounding_boxes(image_path, output_path=None)`
Draw bounding boxes on detected text regions.
- **Returns**: Annotated image array

## Supported Languages

EasyOCR supports 80+ languages. Common ones include:
- English (`en`)
- Chinese (`ch_sim`, `ch_tra`)
- Spanish (`es`)
- French (`fr`)
- German (`de`)
- Japanese (`ja`)
- Korean (`ko`)
- And many more...

To use multiple languages:
```python
model = EasyOCRModel(languages=['en', 'fr', 'de'], gpu=False)
```

## Project Structure

```
EasyOCR-model-training/
├── src/
│   └── easy_ocr_model.py      # Main OCR model implementation
├── sample_images/              # Sample images for testing
├── output/                     # Output directory for annotated images
├── demo.py                     # Demo script
├── generate_sample_image.py   # Script to generate test images
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Requirements

- Python 3.7+
- easyocr >= 1.6.2
- opencv-python >= 4.5.0
- pillow >= 9.0.0
- numpy >= 1.21.0
- torch >= 1.9.0
- torchvision >= 0.10.0

## How It Works

The EasyOCR approach uses deep learning models to:
1. **Detect** text regions in the image
2. **Recognize** the text in each region
3. **Return** the text with bounding boxes and confidence scores

This implementation wraps the EasyOCR library to provide a simple, easy-to-use interface for common OCR tasks.

## Examples

### Example 1: Basic Text Extraction
```python
model = EasyOCRModel()
text = model.get_full_text('invoice.jpg')
print(text)
```

### Example 2: Multi-language OCR
```python
model = EasyOCRModel(languages=['en', 'es'])
results = model.read_image('multilingual_document.jpg')
for bbox, text, conf in results:
    print(f"{text} (confidence: {conf:.2f})")
```

### Example 3: Processing with Confidence Threshold
```python
model = EasyOCRModel()
results = model.get_text_with_confidence('image.jpg')
filtered = [text for text, conf in results if conf > 0.5]
print(filtered)
```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- Uses PyTorch for deep learning
- OpenCV for image processing
