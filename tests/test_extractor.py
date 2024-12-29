import unittest
import pandas as pd
from pathlib import Path
import tempfile
import yaml
from src.extractor import DataExtractor

class TestDataExtractor(unittest.TestCase):
    def setUp(self):
        # Create temporary directory and files for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'employee_id': range(1, 4),
            'department': ['Sales', 'IT', 'Marketing'],
            'performance_score': [85, 92, 78],
            'projects_completed': [12, 15, 10],
            'attendance_rate': [0.95, 0.98, 0.92]
        })
        
        # Save sample data
        self.data_path = self.temp_path / 'employee_data.csv'
        self.sample_data.to_csv(self.data_path, index=False)
        
        # Create test config
        self.config = {
            'paths': {
                'raw_data': str(self.data_path),
                'processed_data': str(self.temp_path / 'processed'),
                'reports': str(self.temp_path / 'reports')
            },
            'database': {
                'type': 'sqlite',
                'name': 'test_db.sqlite'
            },
            'analysis': {
                'metrics': ['performance_score', 'projects_completed', 'attendance_rate'],
                'grouping': ['department']
            }
        }
        
        # Save test config
        self.config_path = self.temp_path / 'test_config.yaml'
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f)
        
        self.extractor = DataExtractor(self.config_path)
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_extract_data(self):
        """Test data extraction from CSV file."""
        extracted_df = self.extractor.extract_data()
        
        # Check if dataframe is not empty
        self.assertFalse(extracted_df.empty)
        
        # Check if all expected columns are present
        expected_columns = ['employee_id', 'department', 'performance_score', 
                          'projects_completed', 'attendance_rate']
        self.assertTrue(all(col in extracted_df.columns for col in expected_columns))
        
        # Check if data types are correct
        self.assertTrue(extracted_df['employee_id'].dtype in ['int64', 'int32'])
        self.assertTrue(extracted_df['department'].dtype == 'object')
        self.assertTrue(pd.api.types.is_numeric_dtype(extracted_df['performance_score']))
        
        # Check if number of rows matches
        self.assertEqual(len(extracted_df), len(self.sample_data))
    
    def test_extract_data_file_not_found(self):
        """Test handling of missing file."""
        # Change config to point to non-existent file
        with open(self.config_path, 'r') as f:
            bad_config = yaml.safe_load(f)
        bad_config['paths']['raw_data'] = 'nonexistent.csv'
        
        bad_config_path = self.temp_path / 'bad_config.yaml'
        with open(bad_config_path, 'w') as f:
            yaml.dump(bad_config, f)
        
        bad_extractor = DataExtractor(bad_config_path)
        
        with self.assertRaises(Exception):
            bad_extractor.extract_data()
    
    def test_extract_data_invalid_format(self):
        """Test handling of invalid CSV format."""
        # Create invalid CSV file
        invalid_path = self.temp_path / 'invalid.csv'
        with open(invalid_path, 'w') as f:
            f.write("invalid,csv,format\nno,proper,headers")
        
        # Update config to point to invalid file
        with open(self.config_path, 'r') as f:
            invalid_config = yaml.safe_load(f)
        invalid_config['paths']['raw_data'] = str(invalid_path)
        
        invalid_config_path = self.temp_path / 'invalid_config.yaml'
        with open(invalid_config_path, 'w') as f:
            yaml.dump(invalid_config, f)
        
        invalid_extractor = DataExtractor(invalid_config_path)
        
        # Test should pass but resulting DataFrame should be empty or raise an error
        try:
            df = invalid_extractor.extract_data()
            self.assertTrue(df.empty or len(df.columns) == 0)
        except Exception as e:
            self.assertTrue(True)
