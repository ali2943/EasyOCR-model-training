"""
Script to generate sample OCR training dataset
Creates simple text images with corresponding labels
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_image(text, filename, size=(300, 100), bg_color='white', text_color='black', 
                       font_size=24, font_style='regular', add_border=False):
    """Create a simple image with text with various styling options."""
    # Create background
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use different fonts based on style
    font = None
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    ]
    
    try:
        if font_style == 'bold':
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        elif font_style == 'italic':
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", font_size)
        elif font_style == 'mono':
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", font_size)
        else:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    except (IOError, OSError):
        font = ImageFont.load_default()
    
    # Calculate text position (centered)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    
    # Add border if requested
    if add_border:
        draw.rectangle([5, 5, size[0]-5, size[1]-5], outline=text_color, width=2)
    
    # Draw text
    draw.text(position, text, fill=text_color, font=font)
    
    # Save image
    img.save(filename)
    print(f"Created: {filename}")

def main():
    """Generate sample dataset."""
    # Sample texts for OCR training with various styles
    # Format: (text, filename, size, bg_color, text_color, font_size, font_style, add_border)
    samples = [
        ("Hello World", "image_001.jpg", (300, 100), 'white', 'black', 24, 'regular', False),
        ("Machine Learning", "image_002.jpg", (300, 100), 'white', 'black', 24, 'regular', False),
        ("Optical Character Recognition", "image_003.jpg", (400, 100), 'white', 'black', 24, 'regular', False),
        ("Deep Learning OCR", "image_004.jpg", (300, 100), 'white', 'black', 24, 'regular', False),
        ("Training Dataset", "image_005.jpg", (300, 100), 'white', 'black', 24, 'regular', False),
        ("Sample Text 123", "image_006.jpg", (300, 100), 'white', 'black', 24, 'regular', False),
        ("Python FastAPI", "image_007.jpg", (300, 100), 'white', 'black', 24, 'regular', False),
        ("EasyOCR Model", "image_008.jpg", (300, 100), 'white', 'black', 24, 'regular', False),
        # New diverse samples
        ("BOLD TEXT EXAMPLE", "image_009.jpg", (350, 100), 'white', 'black', 28, 'bold', False),
        ("Italic Style Text", "image_010.jpg", (300, 100), 'white', 'black', 24, 'italic', False),
        ("Numbers: 1234567890", "image_011.jpg", (350, 100), 'white', 'black', 24, 'mono', False),
        ("Special @#$%&* Chars", "image_012.jpg", (350, 100), 'white', 'black', 24, 'regular', False),
        ("Light Background", "image_013.jpg", (300, 100), '#f0f0f0', '#333333', 24, 'regular', True),
        ("Email: test@example.com", "image_014.jpg", (400, 100), 'white', 'black', 22, 'mono', False),
        ("Website: www.example.org", "image_015.jpg", (400, 100), 'white', 'black', 22, 'regular', False),
    ]
    
    # Create images directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create labels file
    labels_path = os.path.join(script_dir, 'labels.txt')
    with open(labels_path, 'w') as f:
        for sample_data in samples:
            text, filename = sample_data[0], sample_data[1]
            # Create image with styling
            image_path = os.path.join(script_dir, filename)
            create_sample_image(*sample_data)
            
            # Write label (format: filename<TAB>text)
            f.write(f"{filename}\t{text}\n")
    
    print(f"\nCreated labels file: {labels_path}")
    print(f"Dataset created with {len(samples)} samples")

if __name__ == "__main__":
    main()
