from sqlalchemy import create_engine
import pandas as pd

class DataLoader:
    def __init__(self, db_config):
        self.engine = create_engine(f"{db_config['type']}:///{db_config['name']}")
    
    def load_to_database(self, df, table_name, if_exists='replace'):
        """Load transformed data to database."""
        df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
    
    def load_to_csv(self, df, output_path):
        """Save transformed data to CSV."""
        df.to_csv(output_path, index=False)
