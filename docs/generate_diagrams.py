"""
Generate visual diagrams for documentation
Creates architecture and workflow diagrams
"""

from PIL import Image, ImageDraw, ImageFont
import os

def get_font(size=20):
    """Get a font with fallback to default."""
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except (IOError, OSError):
        return ImageFont.load_default()

def draw_rounded_rectangle(draw, xy, radius=10, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill, outline=outline, width=width)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill, outline=outline, width=width)
    draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill, outline=outline)
    draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill, outline=outline)
    draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill, outline=outline)
    draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill, outline=outline)

def create_architecture_diagram():
    """Create system architecture diagram."""
    width, height = 1000, 700
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(28)
    header_font = get_font(20)
    text_font = get_font(16)
    
    # Title
    draw.text((width//2 - 200, 30), "EasyOCR Training System Architecture", 
              fill='black', font=title_font)
    
    # Colors
    ui_color = '#4A90E2'
    api_color = '#7ED321'
    model_color = '#E74C3C'
    data_color = '#F39C12'
    
    # Web UI Layer
    draw_rounded_rectangle(draw, [100, 100, 300, 180], radius=10, fill=ui_color, outline='black', width=2)
    draw.text((140, 125), "Web UI", fill='white', font=header_font)
    draw.text((120, 150), "HTML/CSS/JS", fill='white', font=text_font)
    
    # FastAPI Layer
    draw_rounded_rectangle(draw, [400, 100, 600, 250], radius=10, fill=api_color, outline='black', width=2)
    draw.text((440, 115), "FastAPI", fill='white', font=header_font)
    draw.text((420, 145), "REST API", fill='white', font=text_font)
    draw.text((420, 170), "Dataset Upload", fill='white', font=text_font)
    draw.text((420, 195), "Training Control", fill='white', font=text_font)
    draw.text((420, 220), "Status Tracking", fill='white', font=text_font)
    
    # EasyOCR Model Layer
    draw_rounded_rectangle(draw, [700, 100, 900, 220], radius=10, fill=model_color, outline='black', width=2)
    draw.text((730, 125), "EasyOCR", fill='white', font=header_font)
    draw.text((715, 150), "Text Detection", fill='white', font=text_font)
    draw.text((715, 175), "Recognition", fill='white', font=text_font)
    draw.text((715, 200), "Multi-language", fill='white', font=text_font)
    
    # Data Layer
    draw_rounded_rectangle(draw, [100, 320, 900, 600], radius=10, fill='#F5F5F5', outline='black', width=2)
    draw.text((420, 335), "Data Layer", fill='black', font=header_font)
    
    # Sample Dataset
    draw_rounded_rectangle(draw, [150, 380, 350, 550], radius=8, fill=data_color, outline='black', width=2)
    draw.text((180, 395), "Sample Dataset", fill='white', font=header_font)
    draw.text((160, 430), "• 15 sample images", fill='white', font=text_font)
    draw.text((160, 455), "• Various styles", fill='white', font=text_font)
    draw.text((160, 480), "• Different fonts", fill='white', font=text_font)
    draw.text((160, 505), "• labels.txt", fill='white', font=text_font)
    
    # Uploaded Datasets
    draw_rounded_rectangle(draw, [380, 380, 580, 550], radius=8, fill=data_color, outline='black', width=2)
    draw.text((410, 395), "User Uploads", fill='white', font=header_font)
    draw.text((390, 430), "• Custom images", fill='white', font=text_font)
    draw.text((390, 455), "• Custom labels", fill='white', font=text_font)
    draw.text((390, 480), "• Multiple datasets", fill='white', font=text_font)
    
    # Output/Results
    draw_rounded_rectangle(draw, [610, 380, 850, 550], radius=8, fill=data_color, outline='black', width=2)
    draw.text((660, 395), "Training Results", fill='white', font=header_font)
    draw.text((620, 430), "• Accuracy metrics", fill='white', font=text_font)
    draw.text((620, 455), "• Predictions", fill='white', font=text_font)
    draw.text((620, 480), "• Detailed analysis", fill='white', font=text_font)
    draw.text((620, 505), "• Progress tracking", fill='white', font=text_font)
    
    # Arrows
    # UI -> API
    draw.line([(300, 140), (400, 140)], fill='black', width=3)
    draw.polygon([(400, 140), (390, 135), (390, 145)], fill='black')
    
    # API -> Model
    draw.line([(600, 175), (700, 175)], fill='black', width=3)
    draw.polygon([(700, 175), (690, 170), (690, 180)], fill='black')
    
    # API -> Data
    draw.line([(500, 250), (500, 320)], fill='black', width=3)
    draw.polygon([(500, 320), (495, 310), (505, 310)], fill='black')
    
    # Model -> Data
    draw.line([(800, 220), (800, 320)], fill='black', width=3)
    draw.polygon([(800, 320), (795, 310), (805, 310)], fill='black')
    
    # Save
    output_path = os.path.join(os.path.dirname(__file__), 'images', 'architecture.png')
    img.save(output_path)
    print(f"Created: {output_path}")

def create_workflow_diagram():
    """Create workflow diagram."""
    width, height = 1000, 800
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(28)
    header_font = get_font(20)
    text_font = get_font(16)
    
    # Title
    draw.text((width//2 - 180, 30), "EasyOCR Training Workflow", 
              fill='black', font=title_font)
    
    # Define workflow steps
    steps = [
        ("1. Select Dataset", 100, "#4A90E2", "Choose sample or\nupload custom"),
        ("2. Configure", 220, "#7ED321", "Set languages\nand GPU options"),
        ("3. Start Training", 340, "#F39C12", "Click 'Start Training'\nbutton"),
        ("4. Processing", 460, "#E74C3C", "OCR runs on\neach image"),
        ("5. View Results", 580, "#9B59B6", "See accuracy and\ndetailed analysis"),
    ]
    
    for step_text, y_pos, color, details in steps:
        # Draw step box
        draw_rounded_rectangle(draw, [150, y_pos, 850, y_pos + 90], 
                             radius=10, fill=color, outline='black', width=2)
        draw.text((180, y_pos + 15), step_text, fill='white', font=header_font)
        
        # Draw details
        detail_lines = details.split('\n')
        for i, line in enumerate(detail_lines):
            draw.text((180, y_pos + 45 + i * 20), line, fill='white', font=text_font)
        
        # Draw arrow to next step (except for last step)
        if y_pos < 580:
            arrow_x = 500
            arrow_y1 = y_pos + 90
            arrow_y2 = y_pos + 130
            draw.line([(arrow_x, arrow_y1), (arrow_x, arrow_y2)], fill='black', width=3)
            draw.polygon([(arrow_x, arrow_y2), (arrow_x - 5, arrow_y2 - 10), 
                         (arrow_x + 5, arrow_y2 - 10)], fill='black')
    
    # Add note at bottom
    draw.text((200, 700), "Complete training cycle in minutes with real-time feedback!", 
              fill='#666', font=text_font)
    
    # Save
    output_path = os.path.join(os.path.dirname(__file__), 'images', 'workflow.png')
    img.save(output_path)
    print(f"Created: {output_path}")

def create_features_showcase():
    """Create features showcase image."""
    width, height = 1000, 600
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(28)
    header_font = get_font(20)
    text_font = get_font(16)
    emoji_font = get_font(40)
    
    # Title
    draw.text((width//2 - 150, 30), "Key Features", fill='black', font=title_font)
    
    # Features grid
    features = [
        ("🖼️", "Image OCR", "Extract text from\nimages accurately", 150, 120, "#4A90E2"),
        ("📊", "Web Dashboard", "User-friendly web UI\nfor training", 400, 120, "#7ED321"),
        ("🌍", "Multi-language", "Support 80+\nlanguages", 650, 120, "#F39C12"),
        ("⚡", "Fast Processing", "Quick training and\nvalidation", 150, 330, "#E74C3C"),
        ("📈", "Analytics", "Detailed metrics and\nresults", 400, 330, "#9B59B6"),
        ("🔧", "Easy Setup", "Simple pip install\nand run", 650, 330, "#27AE60"),
    ]
    
    for emoji, title, desc, x, y, color in features:
        # Box
        draw_rounded_rectangle(draw, [x, y, x + 200, y + 180], 
                             radius=10, fill=color, outline='black', width=2)
        # Emoji
        draw.text((x + 75, y + 15), emoji, fill='white', font=emoji_font)
        # Title
        draw.text((x + 30, y + 80), title, fill='white', font=header_font)
        # Description
        desc_lines = desc.split('\n')
        for i, line in enumerate(desc_lines):
            draw.text((x + 20, y + 110 + i * 22), line, fill='white', font=text_font)
    
    # Save
    output_path = os.path.join(os.path.dirname(__file__), 'images', 'features.png')
    img.save(output_path)
    print(f"Created: {output_path}")

def main():
    """Generate all diagrams."""
    print("Generating documentation diagrams...")
    create_architecture_diagram()
    create_workflow_diagram()
    create_features_showcase()
    print("\nAll diagrams created successfully!")

if __name__ == "__main__":
    main()
