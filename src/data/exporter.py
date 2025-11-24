"""
Data export utilities for saving results.
"""

import pandas as pd
import json
from typing import Dict, List, Optional
from pathlib import Path


class DataExporter:
    """
    Handles exporting data to various formats.
    """
    
    @staticmethod
    def export_to_csv(
        df: pd.DataFrame,
        file_path: str,
        index: bool = False,
        **kwargs
    ) -> None:
        """
        Export DataFrame to CSV file.
        
        Args:
            df: DataFrame to export
            file_path: Output file path
            index: Whether to include index in output
            **kwargs: Additional arguments for to_csv
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path, index=index, **kwargs)
        print(f"Data exported to {file_path}")
    
    @staticmethod
    def export_to_excel(
        df: pd.DataFrame,
        file_path: str,
        sheet_name: str = 'Sheet1',
        index: bool = False,
        **kwargs
    ) -> None:
        """
        Export DataFrame to Excel file.
        
        Args:
            df: DataFrame to export
            file_path: Output file path
            sheet_name: Name of the Excel sheet
            index: Whether to include index in output
            **kwargs: Additional arguments for to_excel
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(file_path, sheet_name=sheet_name, index=index, **kwargs)
        print(f"Data exported to {file_path}")
    
    @staticmethod
    def export_to_json(
        data: Dict,
        file_path: str,
        indent: int = 2
    ) -> None:
        """
        Export data to JSON file.
        
        Args:
            data: Dictionary to export
            file_path: Output file path
            indent: JSON indentation level
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=indent, default=str)
        
        print(f"Data exported to {file_path}")
    
    @staticmethod
    def export_multiple_sheets(
        dataframes: Dict[str, pd.DataFrame],
        file_path: str,
        **kwargs
    ) -> None:
        """
        Export multiple DataFrames to different sheets in one Excel file.
        
        Args:
            dataframes: Dictionary of sheet_name -> DataFrame mappings
            file_path: Output file path
            **kwargs: Additional arguments for ExcelWriter
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with pd.ExcelWriter(file_path, **kwargs) as writer:
            for sheet_name, df in dataframes.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"Data exported to {file_path} with {len(dataframes)} sheets")
