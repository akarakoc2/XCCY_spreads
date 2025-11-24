"""
Data processing and transformation utilities.
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict
from datetime import datetime


class DataProcessor:
    """
    Handles data cleaning, transformation, and preprocessing.
    """
    
    @staticmethod
    def clean_data(
        df: pd.DataFrame,
        drop_na: bool = True,
        fill_method: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Clean the input data by handling missing values.
        
        Args:
            df: Input DataFrame
            drop_na: Whether to drop rows with NA values
            fill_method: Method to fill NA values ('ffill', 'bfill', 'mean', etc.)
            
        Returns:
            Cleaned DataFrame
        """
        df_clean = df.copy()
        
        if drop_na:
            df_clean = df_clean.dropna()
        elif fill_method:
            if fill_method in ['ffill', 'bfill']:
                df_clean = df_clean.fillna(method=fill_method)
            elif fill_method == 'mean':
                df_clean = df_clean.fillna(df_clean.mean())
            elif fill_method == 'zero':
                df_clean = df_clean.fillna(0)
        
        return df_clean
    
    @staticmethod
    def resample_timeseries(
        df: pd.DataFrame,
        date_column: str,
        frequency: str = 'D',
        aggregation: str = 'mean'
    ) -> pd.DataFrame:
        """
        Resample time series data to a different frequency.
        
        Args:
            df: Input DataFrame
            date_column: Name of the date column
            frequency: Target frequency ('D', 'W', 'M', etc.)
            aggregation: Aggregation method ('mean', 'sum', 'last', etc.)
            
        Returns:
            Resampled DataFrame
        """
        df_resampled = df.copy()
        df_resampled[date_column] = pd.to_datetime(df_resampled[date_column])
        df_resampled = df_resampled.set_index(date_column)
        
        if aggregation == 'mean':
            df_resampled = df_resampled.resample(frequency).mean()
        elif aggregation == 'sum':
            df_resampled = df_resampled.resample(frequency).sum()
        elif aggregation == 'last':
            df_resampled = df_resampled.resample(frequency).last()
        
        return df_resampled.reset_index()
    
    @staticmethod
    def calculate_moving_average(
        df: pd.DataFrame,
        column: str,
        window: int = 7
    ) -> pd.Series:
        """
        Calculate moving average for a specific column.
        
        Args:
            df: Input DataFrame
            column: Column name to calculate MA for
            window: Window size for moving average
            
        Returns:
            Series containing the moving average
        """
        return df[column].rolling(window=window).mean()
    
    @staticmethod
    def calculate_percentage_change(
        df: pd.DataFrame,
        column: str
    ) -> pd.Series:
        """
        Calculate percentage change for a specific column.
        
        Args:
            df: Input DataFrame
            column: Column name to calculate change for
            
        Returns:
            Series containing percentage changes
        """
        return df[column].pct_change() * 100
    
    @staticmethod
    def filter_by_date_range(
        df: pd.DataFrame,
        date_column: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Filter DataFrame by date range.
        
        Args:
            df: Input DataFrame
            date_column: Name of the date column
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            Filtered DataFrame
        """
        df_filtered = df.copy()
        df_filtered[date_column] = pd.to_datetime(df_filtered[date_column])
        
        if start_date:
            df_filtered = df_filtered[
                df_filtered[date_column] >= pd.to_datetime(start_date)
            ]
        
        if end_date:
            df_filtered = df_filtered[
                df_filtered[date_column] <= pd.to_datetime(end_date)
            ]
        
        return df_filtered
    
    @staticmethod
    def normalize_data(
        df: pd.DataFrame,
        columns: List[str],
        method: str = 'zscore'
    ) -> pd.DataFrame:
        """
        Normalize data using specified method.
        
        Args:
            df: Input DataFrame
            columns: List of columns to normalize
            method: Normalization method ('zscore', 'minmax')
            
        Returns:
            DataFrame with normalized columns
        """
        df_normalized = df.copy()
        
        for col in columns:
            if method == 'zscore':
                mean = df[col].mean()
                std = df[col].std()
                df_normalized[col] = (df[col] - mean) / std
            elif method == 'minmax':
                min_val = df[col].min()
                max_val = df[col].max()
                df_normalized[col] = (df[col] - min_val) / (max_val - min_val)
        
        return df_normalized
