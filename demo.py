"""
Demo script for EasyOCR Image-to-Text Model
This script demonstrates how to use the EasyOCRModel to extract text from images.
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from easy_ocr_model import EasyOCRModel


def demo_basic_usage():
    """Demonstrate basic usage of the EasyOCR model."""
    print("=" * 70)
    print("EasyOCR Image-to-Text Model - Demo")
    print("=" * 70)
    
    # Initialize the model
    print("\n[1] Initializing EasyOCR model...")
    print("    Languages: English")
    print("    GPU: False (using CPU)")
    
    model = EasyOCRModel(languages=['en'], gpu=False)
    print("    ✓ Model initialized successfully!")
    
    return model


def process_sample_image(model, image_path):
    """Process a sample image and display results."""
    if not Path(image_path).exists():
        print(f"\n⚠️  Image not found: {image_path}")
        print("    Please provide a valid image path.")
        return False
    
    print(f"\n[2] Processing image: {image_path}")
    
    try:
        # Get full OCR results
        results = model.read_image(image_path)
        
        print(f"\n    ✓ Found {len(results)} text region(s)")
        print("\n" + "=" * 70)
        print("RESULTS:")
        print("=" * 70)
        
        # Display detailed results
        for i, (bbox, text, confidence) in enumerate(results, 1):
            print(f"\n[{i}] Text: {text}")
            print(f"    Confidence: {confidence:.2%}")
            print(f"    Bounding Box: {bbox}")
        
        # Display concatenated text
        print("\n" + "=" * 70)
        print("FULL TEXT (Concatenated):")
        print("=" * 70)
        full_text = model.get_full_text(image_path)
        print(full_text)
        
        # Draw bounding boxes (if output directory exists)
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"annotated_{Path(image_path).name}"
        
        print(f"\n[3] Saving annotated image...")
        model.draw_bounding_boxes(image_path, output_path)
        print(f"    ✓ Annotated image saved to: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error processing image: {str(e)}")
        return False


def main():
    """Main function."""
    # Initialize model
    model = demo_basic_usage()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        print("\n" + "=" * 70)
        print("USAGE:")
        print("=" * 70)
        print(f"  python {sys.argv[0]} <image_path>")
        print("\nExample:")
        print(f"  python {sys.argv[0]} sample_images/example.jpg")
        print("\nOr use the model in your own code:")
        print("  from src.easy_ocr_model import EasyOCRModel")
        print("  model = EasyOCRModel(languages=['en'], gpu=False)")
        print("  results = model.read_image('path/to/image.jpg')")
        print("  text = model.get_full_text('path/to/image.jpg')")
        print("=" * 70)
        return
    
    # Process the image
    success = process_sample_image(model, image_path)
    
    if success:
        print("\n" + "=" * 70)
        print("✓ Demo completed successfully!")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("✗ Demo failed!")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
