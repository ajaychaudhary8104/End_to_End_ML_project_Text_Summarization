"""
DVC Tracking Module
This module provides utilities for tracking data, models, and metrics with DVC
"""

import json
import os
from pathlib import Path
from textSummarizer.logging import logger


class DVCTracker:
    """
    A utility class for tracking artifacts with DVC
    """
    
    def __init__(self, metrics_dir: str = "artifacts"):
        """
        Initialize DVC Tracker
        
        Args:
            metrics_dir: Root directory for storing metrics
        """
        self.metrics_dir = metrics_dir
        Path(metrics_dir).mkdir(parents=True, exist_ok=True)
    
    def log_metrics(self, stage_name: str, metrics: dict):
        """
        Log metrics for a specific stage
        
        Args:
            stage_name: Name of the pipeline stage
            metrics: Dictionary of metrics to log
        """
        try:
            metrics_file = os.path.join(
                self.metrics_dir, 
                stage_name, 
                ".metrics.json"
            )
            
            # Create directory if it doesn't exist
            Path(metrics_file).parent.mkdir(parents=True, exist_ok=True)
            
            # Write metrics to JSON file
            with open(metrics_file, 'w') as f:
                json.dump(metrics, f, indent=4)
            
            logger.info(f"Metrics logged for {stage_name} at {metrics_file}")
            
        except Exception as e:
            logger.exception(f"Error logging metrics for {stage_name}: {str(e)}")
            raise e
    
    def log_data(self, stage_name: str, data_path: str, description: str = ""):
        """
        Log data artifacts path for DVC tracking
        
        Args:
            stage_name: Name of the pipeline stage
            data_path: Path to the data artifact
            description: Optional description of the data
        """
        try:
            logger.info(f"Data tracked for {stage_name}: {data_path}")
            if description:
                logger.info(f"Description: {description}")
        except Exception as e:
            logger.exception(f"Error logging data for {stage_name}: {str(e)}")
            raise e
    
    def log_model(self, stage_name: str, model_path: str, model_type: str = ""):
        """
        Log model artifacts path for DVC tracking
        
        Args:
            stage_name: Name of the pipeline stage
            model_path: Path to the model artifact
            model_type: Type of model (e.g., 'transformer', 'neural_net')
        """
        try:
            logger.info(f"Model tracked for {stage_name}: {model_path}")
            if model_type:
                logger.info(f"Model Type: {model_type}")
        except Exception as e:
            logger.exception(f"Error logging model for {stage_name}: {str(e)}")
            raise e
    
    def log_params(self, params_file: str = "params.yaml"):
        """
        Log parameters file for DVC tracking
        
        Args:
            params_file: Path to the parameters file
        """
        try:
            logger.info(f"Parameters tracked from: {params_file}")
        except Exception as e:
            logger.exception(f"Error logging params: {str(e)}")
            raise e


# Global DVC Tracker instance
dvc_tracker = DVCTracker()


def get_dvc_tracker() -> DVCTracker:
    """Get the global DVC tracker instance"""
    return dvc_tracker
