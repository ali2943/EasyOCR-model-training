"""
Script to generate sample OCR training dataset
Creates simple text images with corresponding labels
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_image(text, filename, size=(300, 100)):
    """Create a simple image with text."""
    # Create white background
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a basic font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except (IOError, OSError):
        font = ImageFont.load_default()
    
    # Calculate text position (centered)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    
    # Draw text
    draw.text(position, text, fill='black', font=font)
    
    # Save image
    img.save(filename)
    print(f"Created: {filename}")

def main():
    """Generate sample dataset."""
    # Sample texts for OCR training
    samples = [
        ("Hello World", "image_001.jpg"),
        ("Machine Learning", "image_002.jpg"),
        ("Optical Character Recognition", "image_003.jpg"),
        ("Deep Learning OCR", "image_004.jpg"),
        ("Training Dataset", "image_005.jpg"),
        ("Sample Text 123", "image_006.jpg"),
        ("Python FastAPI", "image_007.jpg"),
        ("EasyOCR Model", "image_008.jpg"),
    ]
    
    # Create images directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create labels file
    labels_path = os.path.join(script_dir, 'labels.txt')
    with open(labels_path, 'w') as f:
        for text, filename in samples:
            # Create image
            image_path = os.path.join(script_dir, filename)
            create_sample_image(text, image_path)
            
            # Write label (format: filename<TAB>text)
            f.write(f"{filename}\t{text}\n")
    
    print(f"\nCreated labels file: {labels_path}")
    print(f"Dataset created with {len(samples)} samples")

if __name__ == "__main__":
    main()
