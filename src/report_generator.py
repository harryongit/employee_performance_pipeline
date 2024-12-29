import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class ReportGenerator:
    def __init__(self, config):
        self.report_path = Path(config['paths']['reports'])
        self.report_path.mkdir(exist_ok=True)
        
    def generate_performance_report(self, df, stats_results):
        """Generate comprehensive performance report with visualizations."""
        plt.style.use('seaborn')
        
        # Create performance distribution plot
        self._create_performance_distribution(df)
        
        # Create department comparison plot
        self._create_department_comparison(df)
        
        # Generate summary report
        self._generate_summary_report(df, stats_results)
    
    def _create_performance_distribution(self, df):
        """Create distribution plot of performance scores."""
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x='performance_score', hue='department', multiple="stack")
        plt.title('Distribution of Performance Scores by Department')
        plt.savefig(self.report_path / 'performance_distribution.png')
        plt.close()
    
    def _create_department_comparison(self, df):
        """Create box plot comparing departments."""
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x='department', y='performance_score')
        plt.title('Performance Score Comparison by Department')
        plt.xticks(rotation=45)
        plt.savefig(self.report_path / 'department_comparison.png')
        plt.close()
    
    def _generate_summary_report(self, df, stats_results):
        """Generate text summary report."""
        with open(self.report_path / 'summary_report.txt', 'w') as f:
            f.write("Employee Performance Analysis Summary\n")
            f.write("====================================\n\n")
            
            f.write("Overall Statistics:\n")
            for metric, stats in stats_results.items():
                f.write(f"\n{metric.title()}:\n")
                f.write(f"Mean: {stats['mean']:.2f}\n")
                f.write(f"Median: {stats['median']:.2f}\n")
                f.write(f"Standard Deviation: {stats['std']:.2f}\n")
                f.write(f"ANOVA p-value: {stats['anova']['p_value']:.4f}\n")
