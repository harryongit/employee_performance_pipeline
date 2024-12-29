import unittest
import pandas as pd
import numpy as np
from src.transformer import DataTransformer

class TestDataTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = DataTransformer()
        self.sample_data = pd.DataFrame({
            'employee_id': range(1, 4),
            'performance_score': [3, 4, 5],
            'attendance_rate': [0.95, 0.87, 0.92],
            'projects_completed': [10, -1, 15]
        })
    
    def test_normalize_performance_score(self):
        result = self.transformer._normalize_performance_score(self.sample_data['performance_score'])
        self.assertTrue(all(result >= 0) and all(result <= 100))
    
    def test_validate_projects(self):
        result = self.transformer._validate_projects(self.sample_data['projects_completed'])
        self.assertTrue(all(result >= 0))

if __name__ == '__main__':
    unittest.main()
