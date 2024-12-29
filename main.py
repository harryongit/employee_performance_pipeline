# main.py
import yaml
from pathlib import Path
from src.extractor import DataExtractor
from src.transformer import DataTransformer
from src.loader import DataLoader
from src.analyzer import PerformanceAnalyzer
from src.report_generator import ReportGenerator

def main():
    # Load configuration
    with open('config/pipeline_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    # Initialize components
    extractor = DataExtractor('config/pipeline_config.yaml')
    transformer = DataTransformer()
    loader = DataLoader(config['database'])
    analyzer = PerformanceAnalyzer(config)
    report_gen = ReportGenerator(config)
    
    # Execute pipeline
    try:
        # Extract
        raw_data = extractor.extract_data()
        
        # Transform
        transformed_data = transformer.transform_data(raw_data)
        
        # Load
        loader.load_to_database(transformed_data, 'employee_performance')
        loader.load_to_csv(
            transformed_data, 
            Path(config['paths']['processed_data']) / 'processed_employee_data.csv'
        )
        
        # Analyze
        dept_metrics = analyzer.calculate_department_metrics(transformed_data)
        top_performers = analyzer.identify_top_performers(transformed_data)
        stats_results = analyzer.perform_statistical_analysis(transformed_data)
        
        # Generate reports
        report_gen.generate_performance_report(transformed_data, stats_results)
        
        print("Pipeline executed successfully!")
        
    except Exception as e:
        print(f"Error executing pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main()
