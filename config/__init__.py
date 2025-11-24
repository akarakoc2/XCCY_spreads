"""
Configuration manager for XCCY Spreads application.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """
    Configuration manager that loads and provides access to application settings.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to configuration JSON file
        """
        if config_path is None:
            # Default to config/config.json in project root
            project_root = Path(__file__).parent.parent
            config_path = project_root / 'config' / 'config.json'
        
        self.config_path = Path(config_path)
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            print(f"Warning: Config file not found at {self.config_path}, using defaults")
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "application": {
                "name": "XCCY Spreads Analyzer",
                "version": "1.0.0"
            },
            "data": {
                "output_directory": "output"
            },
            "oas_analysis": {
                "max_oas_filter": 150,
                "min_duration_filter": 1
            },
            "visualization": {
                "figure_size": [12, 7],
                "dpi": 300
            }
        }
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Path to config value (e.g., 'data.output_directory')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self._config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.
        
        Args:
            section: Section name (e.g., 'oas_analysis')
            
        Returns:
            Dictionary of section configuration
        """
        return self._config.get(section, {})
    
    @property
    def all(self) -> Dict[str, Any]:
        """Get entire configuration."""
        return self._config


# Global config instance
_config_instance = None


def get_config(config_path: Optional[str] = None) -> Config:
    """
    Get global configuration instance.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        Config instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance
