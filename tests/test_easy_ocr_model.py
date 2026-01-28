"""
Unit tests for EasyOCR Model
"""

import unittest
import sys
import os
from pathlib import Path
import numpy as np

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from easy_ocr_model import EasyOCRModel


class TestEasyOCRModel(unittest.TestCase):
    """Test cases for EasyOCRModel class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.model = EasyOCRModel(languages=['en'], gpu=False)
        cls.test_image_path = Path(__file__).parent.parent / 'sample_images' / 'sample_text.jpg'
    
    def test_model_initialization(self):
        """Test that the model initializes correctly."""
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.model.reader)
        self.assertEqual(self.model.languages, ['en'])
        self.assertFalse(self.model.gpu)
    
    def test_read_image(self):
        """Test reading text from an image."""
        if not self.test_image_path.exists():
            self.skipTest(f"Test image not found: {self.test_image_path}")
        
        results = self.model.read_image(self.test_image_path)
        
        # Check that results are returned
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # Check format of results
        for bbox, text, confidence in results:
            self.assertIsInstance(text, str)
            self.assertIsInstance(confidence, float)
            self.assertGreater(len(text), 0)
            self.assertGreaterEqual(confidence, 0.0)
            self.assertLessEqual(confidence, 1.0)
    
    def test_extract_text_only(self):
        """Test extracting only text content."""
        if not self.test_image_path.exists():
            self.skipTest(f"Test image not found: {self.test_image_path}")
        
        text_list = self.model.extract_text_only(self.test_image_path)
        
        self.assertIsInstance(text_list, list)
        self.assertGreater(len(text_list), 0)
        
        for text in text_list:
            self.assertIsInstance(text, str)
            self.assertGreater(len(text), 0)
    
    def test_get_full_text(self):
        """Test getting concatenated full text."""
        if not self.test_image_path.exists():
            self.skipTest(f"Test image not found: {self.test_image_path}")
        
        full_text = self.model.get_full_text(self.test_image_path)
        
        self.assertIsInstance(full_text, str)
        self.assertGreater(len(full_text), 0)
    
    def test_get_text_with_confidence(self):
        """Test getting text with confidence scores."""
        if not self.test_image_path.exists():
            self.skipTest(f"Test image not found: {self.test_image_path}")
        
        results = self.model.get_text_with_confidence(self.test_image_path)
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        for text, confidence in results:
            self.assertIsInstance(text, str)
            self.assertIsInstance(confidence, float)
            self.assertGreater(len(text), 0)
            self.assertGreaterEqual(confidence, 0.0)
            self.assertLessEqual(confidence, 1.0)
    
    def test_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent files."""
        with self.assertRaises(FileNotFoundError):
            self.model.read_image('nonexistent_file.jpg')
    
    def test_draw_bounding_boxes(self):
        """Test drawing bounding boxes on images."""
        if not self.test_image_path.exists():
            self.skipTest(f"Test image not found: {self.test_image_path}")
        
        # Test without saving
        result_image = self.model.draw_bounding_boxes(self.test_image_path)
        self.assertIsInstance(result_image, np.ndarray)
        self.assertEqual(len(result_image.shape), 3)  # Should be a color image
        
        # Test with saving
        output_path = Path('/tmp/test_output.jpg')
        result_image = self.model.draw_bounding_boxes(self.test_image_path, output_path)
        self.assertTrue(output_path.exists())
        
        # Clean up
        if output_path.exists():
            output_path.unlink()


def run_tests():
    """Run all tests."""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEasyOCRModel)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
