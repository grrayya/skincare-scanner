import unittest
import numpy as np

# Import the specific math functions from your cv_engine
from cv_engine import calculate_redness, calculate_texture, calculate_oiliness

class TestCVMathEngine(unittest.TestCase):
    def setUp(self):
        """Set up mock image data before each test runs."""
        # Create a pure black 100x100 RGB image matrix
        self.black_image = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Create a pure white 100x100 RGB image matrix
        self.white_image = np.ones((100, 100, 3), dtype=np.uint8) * 255

    def test_redness_bounds(self):
        """Test that redness scores stay safely clamped between 0.0 and 1.0."""
        black_score = calculate_redness(self.black_image)
        white_score = calculate_redness(self.white_image)
        
        self.assertTrue(0.0 <= black_score <= 1.0)
        self.assertTrue(0.0 <= white_score <= 1.0)

    def test_texture_flat_surface(self):
        """Test that a perfectly flat image (no edges) returns 0 variance."""
        texture_score = calculate_texture(self.black_image)
        self.assertEqual(texture_score, 0.0)

    def test_oiliness_glare(self):
        """Test that a purely white image registers as maximum glare/oiliness."""
        oiliness_score = calculate_oiliness(self.white_image)
        self.assertEqual(oiliness_score, 1.0)

if __name__ == '__main__':
    unittest.main()
