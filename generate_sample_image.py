"""
Generate a sample test image with text for OCR testing.
"""

import cv2
import numpy as np
from pathlib import Path


def create_sample_image(output_path):
    """Create a simple test image with text."""
    # Create a white background
    height, width = 400, 800
    image = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Add text to the image
    texts = [
        ("EasyOCR Demo", (50, 80), 2.0),
        ("This is a sample image for OCR testing.", (50, 160), 0.8),
        ("Convert images to text easily!", (50, 220), 0.8),
        ("Supports multiple languages.", (50, 280), 0.8),
        ("Phone: +1-234-567-8900", (50, 340), 0.6),
    ]
    
    for text, position, scale in texts:
        cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX,
                   scale, (0, 0, 0), 2, cv2.LINE_AA)
    
    # Add a box around the image
    cv2.rectangle(image, (20, 20), (width-20, height-20), (0, 0, 255), 3)
    
    # Save the image
    cv2.imwrite(str(output_path), image)
    print(f"Sample image created: {output_path}")


def main():
    """Generate sample images."""
    # Create sample_images directory if it doesn't exist
    sample_dir = Path("sample_images")
    sample_dir.mkdir(exist_ok=True)
    
    # Create sample image
    output_path = sample_dir / "sample_text.jpg"
    create_sample_image(output_path)
    
    print("\nSample image generated successfully!")
    print(f"Location: {output_path}")
    print("\nYou can now test the OCR model with:")
    print(f"  python demo.py {output_path}")


if __name__ == "__main__":
    main()
