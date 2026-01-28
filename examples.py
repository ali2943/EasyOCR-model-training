"""
Quick Examples for EasyOCR Model

This file contains simple code examples for using the EasyOCR model.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from easy_ocr_model import EasyOCRModel


def example1_basic_ocr():
    """Example 1: Basic OCR - Extract text from an image"""
    print("Example 1: Basic OCR")
    print("-" * 50)
    
    # Initialize the model
    model = EasyOCRModel(languages=['en'], gpu=False)
    
    # Read text from image
    image_path = 'sample_images/sample_text.jpg'
    results = model.read_image(image_path)
    
    # Print results
    for bbox, text, confidence in results:
        print(f"Text: {text}")
        print(f"Confidence: {confidence:.2%}\n")


def example2_extract_text_only():
    """Example 2: Extract only text (no bounding boxes or confidence)"""
    print("\nExample 2: Extract Text Only")
    print("-" * 50)
    
    model = EasyOCRModel(languages=['en'], gpu=False)
    
    image_path = 'sample_images/sample_text.jpg'
    text_list = model.extract_text_only(image_path)
    
    print("Extracted text:")
    for text in text_list:
        print(f"  - {text}")


def example3_get_full_text():
    """Example 3: Get all text as a single string"""
    print("\nExample 3: Get Full Text")
    print("-" * 50)
    
    model = EasyOCRModel(languages=['en'], gpu=False)
    
    image_path = 'sample_images/sample_text.jpg'
    full_text = model.get_full_text(image_path)
    
    print(f"Full text:\n{full_text}")


def example4_confidence_threshold():
    """Example 4: Filter results by confidence threshold"""
    print("\nExample 4: Filter by Confidence")
    print("-" * 50)
    
    model = EasyOCRModel(languages=['en'], gpu=False)
    
    image_path = 'sample_images/sample_text.jpg'
    results = model.get_text_with_confidence(image_path)
    
    # Filter by confidence threshold
    threshold = 0.8
    high_confidence_text = [text for text, conf in results if conf >= threshold]
    
    print(f"Text with confidence >= {threshold:.0%}:")
    for text in high_confidence_text:
        print(f"  - {text}")


def example5_draw_bounding_boxes():
    """Example 5: Draw bounding boxes on the image"""
    print("\nExample 5: Draw Bounding Boxes")
    print("-" * 50)
    
    model = EasyOCRModel(languages=['en'], gpu=False)
    
    image_path = 'sample_images/sample_text.jpg'
    output_path = 'output/example_annotated.jpg'
    
    # Create output directory if it doesn't exist
    import os
    os.makedirs('output', exist_ok=True)
    
    model.draw_bounding_boxes(image_path, output_path)
    print(f"Annotated image saved to: {output_path}")


def example6_multilingual():
    """Example 6: Multi-language OCR"""
    print("\nExample 6: Multi-language OCR")
    print("-" * 50)
    
    # Initialize model with multiple languages
    model = EasyOCRModel(languages=['en', 'es', 'fr'], gpu=False)
    
    print("Model initialized with languages: English, Spanish, French")
    print("You can now process images containing text in multiple languages!")


def main():
    """Run all examples."""
    import os
    
    # Check if sample image exists
    if not os.path.exists('sample_images/sample_text.jpg'):
        print("Sample image not found!")
        print("Please run: python generate_sample_image.py")
        return
    
    print("=" * 70)
    print("EasyOCR Model - Code Examples")
    print("=" * 70)
    
    example1_basic_ocr()
    example2_extract_text_only()
    example3_get_full_text()
    example4_confidence_threshold()
    example5_draw_bounding_boxes()
    example6_multilingual()
    
    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
