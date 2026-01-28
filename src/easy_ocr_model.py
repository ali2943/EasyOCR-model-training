"""
EasyOCR Image-to-Text Model
This module implements an OCR model using EasyOCR to convert images to text.
"""

import easyocr
import cv2
import numpy as np
import logging
from typing import List, Tuple, Optional, Union
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)


class EasyOCRModel:
    """
    A wrapper class for EasyOCR that provides easy-to-use methods
    for extracting text from images.
    """
    
    def __init__(self, languages: List[str] = ['en'], gpu: bool = False):
        """
        Initialize the EasyOCR model.
        
        Args:
            languages: List of language codes to use for OCR (default: ['en'])
            gpu: Whether to use GPU for processing (default: False)
        """
        self.languages = languages
        self.gpu = gpu
        self.reader = None
        self._initialize_reader()
    
    def _initialize_reader(self):
        """Initialize the EasyOCR reader."""
        try:
            self.reader = easyocr.Reader(self.languages, gpu=self.gpu)
            logger.info(f"EasyOCR reader initialized with languages: {self.languages}")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize EasyOCR reader: {str(e)}")
    
    def read_image(self, image_path: Union[str, Path]) -> List[Tuple[List, str, float]]:
        """
        Read text from an image file.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of tuples containing (bounding_box, text, confidence)
        """
        if not self.reader:
            raise RuntimeError("EasyOCR reader not initialized")
        
        image_path = str(image_path)
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        try:
            results = self.reader.readtext(image_path)
            return results
        except Exception as e:
            raise RuntimeError(f"Failed to read image: {str(e)}")
    
    def read_image_array(self, image_array: np.ndarray) -> List[Tuple[List, str, float]]:
        """
        Read text from a numpy array (image).
        
        Args:
            image_array: Image as numpy array (BGR or RGB format)
            
        Returns:
            List of tuples containing (bounding_box, text, confidence)
        """
        if not self.reader:
            raise RuntimeError("EasyOCR reader not initialized")
        
        try:
            results = self.reader.readtext(image_array)
            return results
        except Exception as e:
            raise RuntimeError(f"Failed to read image array: {str(e)}")
    
    def extract_text_only(self, image_path: Union[str, Path]) -> List[str]:
        """
        Extract only the text content from an image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of extracted text strings
        """
        results = self.read_image(image_path)
        return [text for (_, text, _) in results]
    
    def get_text_with_confidence(self, image_path: Union[str, Path]) -> List[Tuple[str, float]]:
        """
        Extract text with confidence scores from an image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of tuples containing (text, confidence)
        """
        results = self.read_image(image_path)
        return [(text, confidence) for (_, text, confidence) in results]
    
    def get_full_text(self, image_path: Union[str, Path], separator: str = ' ') -> str:
        """
        Extract all text from an image as a single string.
        
        Args:
            image_path: Path to the image file
            separator: String to join text fragments (default: ' ')
            
        Returns:
            Concatenated text string
        """
        text_list = self.extract_text_only(image_path)
        return separator.join(text_list)
    
    def draw_bounding_boxes(self, image_path: Union[str, Path], 
                          output_path: Optional[Union[str, Path]] = None) -> np.ndarray:
        """
        Draw bounding boxes on the image with detected text.
        
        Args:
            image_path: Path to the input image file
            output_path: Path to save the output image (optional)
            
        Returns:
            Image array with bounding boxes drawn
        """
        # Read the image
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")
        
        # Get OCR results
        results = self.read_image(image_path)
        
        # Draw bounding boxes and text
        for (bbox, text, confidence) in results:
            # Convert bbox to integer coordinates
            bbox = [[int(x), int(y)] for x, y in bbox]
            
            # Draw the bounding box
            pts = np.array(bbox, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(image, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
            
            # Put text and confidence
            cv2.putText(image, f"{text} ({confidence:.2f})", 
                       tuple(bbox[0]), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (0, 0, 255), 1)
        
        # Save if output path is provided
        if output_path:
            cv2.imwrite(str(output_path), image)
            logger.info(f"Output saved to: {output_path}")
        
        return image


def main():
    """
    Main function demonstrating the usage of EasyOCRModel.
    """
    print("EasyOCR Image-to-Text Model")
    print("=" * 50)
    
    # Example usage
    # Initialize the model
    model = EasyOCRModel(languages=['en'], gpu=False)
    
    # Example: Read text from an image
    # image_path = "path/to/your/image.jpg"
    # results = model.read_image(image_path)
    # 
    # print("\nFull OCR Results:")
    # for bbox, text, confidence in results:
    #     print(f"Text: {text}, Confidence: {confidence:.2f}")
    # 
    # print("\nExtracted Text Only:")
    # text_list = model.extract_text_only(image_path)
    # for text in text_list:
    #     print(text)
    # 
    # print("\nFull Text:")
    # full_text = model.get_full_text(image_path)
    # print(full_text)
    
    print("\nModel initialized successfully!")
    print("Use the EasyOCRModel class to process your images.")


if __name__ == "__main__":
    main()
