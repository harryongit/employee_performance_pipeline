import pandas as pd
import numpy as np
from datetime import datetime

class DataTransformer:
    def __init__(self):
        self.transformations = {
            'performance_score': self._normalize_performance_score,
            'attendance_rate': self._calculate_attendance_rate,
            'projects_completed': self._validate_projects
        }
    
    def transform_data(self, df):
        """Apply all transformations to the dataset."""
        transformed_df = df.copy()
        
        for column, transformation in self.transformations.items():
            if column in transformed_df.columns:
                transformed_df[column] = transformation(transformed_df[column])
        
        transformed_df['processed_date'] = datetime.now()
        return transformed_df
    
    def _normalize_performance_score(self, series):
        """Normalize performance scores to 0-100 scale."""
        return ((series - series.min()) / (series.max() - series.min()) * 100).round(2)
    
    def _calculate_attendance_rate(self, series):
        """Calculate attendance rate as percentage."""
        return (series * 100).round(2)
    
    def _validate_projects(self, series):
        """Validate and clean projects completed data."""
        return series.clip(lower=0)
