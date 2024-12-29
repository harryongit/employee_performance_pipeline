import pandas as pd
import yaml
import logging
from pathlib import Path

class DataExtractor:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def extract_data(self):
        """Extract data from source file."""
        try:
            file_path = Path(self.config['paths']['raw_data'])
            self.logger.info(f"Extracting data from {file_path}")
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            self.logger.error(f"Error extracting data: {str(e)}")
            raise
