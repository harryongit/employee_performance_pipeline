import pandas as pd
import numpy as np
from scipy import stats

class PerformanceAnalyzer:
    def __init__(self, config):
        self.metrics = config['analysis']['metrics']
        self.grouping = config['analysis']['grouping']
    
    def calculate_department_metrics(self, df):
        """Calculate key metrics by department."""
        dept_metrics = df.groupby('department')[self.metrics].agg([
            'mean', 'median', 'std'
        ]).round(2)
        return dept_metrics
    
    def identify_top_performers(self, df, threshold=90):
        """Identify top performers based on performance score."""
        top_performers = df[df['performance_score'] >= threshold]
        return top_performers
    
    def perform_statistical_analysis(self, df):
        """Perform statistical analysis on performance metrics."""
        stats_results = {}
        
        for metric in self.metrics:
            # Calculate basic statistics
            stats_results[metric] = {
                'mean': df[metric].mean(),
                'median': df[metric].median(),
                'std': df[metric].std(),
                'skew': df[metric].skew(),
                'kurtosis': df[metric].kurtosis()
            }
            
            # Perform one-way ANOVA for departments
            departments = df['department'].unique()
            dept_groups = [df[df['department'] == dept][metric] for dept in departments]
            f_stat, p_value = stats.f_oneway(*dept_groups)
            
            stats_results[metric]['anova'] = {
                'f_statistic': f_stat,
                'p_value': p_value
            }
        
        return stats_results
