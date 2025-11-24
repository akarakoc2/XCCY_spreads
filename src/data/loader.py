"""
Data loading utilities for various file formats.
"""

import pandas as pd
from typing import Optional, Dict, List
from pathlib import Path
import json
import csv


class DataLoader:
    """
    Handles loading data from various sources and formats.
    
    Supports CSV, Excel, JSON, and can be extended for API data.
    """
    
    @staticmethod
    def load_csv(
        file_path: str,
        date_column: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load data from a CSV file.
        
        Args:
            file_path: Path to the CSV file
            date_column: Name of the date column to parse
            **kwargs: Additional arguments for pd.read_csv
            
        Returns:
            DataFrame containing the loaded data
        """
        parse_dates = [date_column] if date_column else None
        
        df = pd.read_csv(
            file_path,
            parse_dates=parse_dates,
            **kwargs
        )
        
        return df
    
    @staticmethod
    def load_excel(
        file_path: str,
        sheet_name: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load data from an Excel file.
        
        Args:
            file_path: Path to the Excel file
            sheet_name: Name of the sheet to load (default: first sheet)
            **kwargs: Additional arguments for pd.read_excel
            
        Returns:
            DataFrame containing the loaded data
        """
        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name or 0,
            **kwargs
        )
        
        return df
    
    @staticmethod
    def load_json(file_path: str) -> Dict:
        """
        Load data from a JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Dictionary containing the loaded data
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return data
    
    @staticmethod
    def load_from_dict(data: Dict) -> pd.DataFrame:
        """
        Load data from a dictionary into a DataFrame.
        
        Args:
            data: Dictionary containing the data
            
        Returns:
            DataFrame containing the data
        """
        return pd.DataFrame(data)
    
    def validate_data(
        self,
        df: pd.DataFrame,
        required_columns: List[str]
    ) -> bool:
        """
        Validate that required columns exist in the DataFrame.
        
        Args:
            df: DataFrame to validate
            required_columns: List of required column names
            
        Returns:
            True if all required columns exist, False otherwise
        """
        missing_columns = set(required_columns) - set(df.columns)
        
        if missing_columns:
            raise ValueError(
                f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        return True
