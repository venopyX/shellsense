"""
Logging Manager for ShellSense

This module provides a centralized logging configuration system that can be used across the application.
It supports different environments (development, production) and allows for flexible logging setup.

Features:
- Environment-based configuration
- Multiple handlers (console, file)
- Custom log formatting
- Log level control
- Singleton pattern to ensure consistent logging across the application

Usage:
    ```python
    from shellsense.utils.logging_manager import get_logger, log_function_call

    # Get a logger instance
    logger = get_logger(__name__)

    # Use the decorator for development-only logging
    @log_function_call
    def your_function():
        logger.info("This is an info message")
        logger.debug("This debug message will only appear in development")
    
    # No decorator for production logging_manager
    def your_function2():
        logger.info("This is an info message")
        logger.debug("This debug message will appear in production")
    ```

TODO:
- Add support for remote logging services
- Implement log rotation
- Add support for structured logging
- Add performance metrics logging
"""

import os
import sys
import logging
import logging.handlers
from typing import Optional, Dict, Any
from functools import wraps
from pathlib import Path

class LoggingManager:
    """
    A singleton class that manages logging configuration across the application.
    
    Attributes:
        _instance (LoggingManager): Singleton instance
        _initialized (bool): Flag to track initialization
        logger (logging.Logger): Main logger instance
        log_level (int): Current log level
        environment (str): Current environment (development/production)
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls) -> 'LoggingManager':
        if cls._instance is None:
            cls._instance = super(LoggingManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not self._initialized:
            self._initialized = True
            self.logger = logging.getLogger('shellsense')
            self.environment = os.environ.get('ENVIRONMENT', 'production')
            self._configure_logging()
    
    def _configure_logging(self) -> None:
        """Configure logging based on the environment."""
        # Set base configuration
        self.logger.setLevel(logging.DEBUG if self.environment == 'development' else logging.INFO)
        
        # Create logs directory if it doesn't exist
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        simple_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Configure handlers based on environment
        if self.environment == 'development':
            # Console handler (stdout) for development
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(detailed_formatter)
            console_handler.setLevel(logging.DEBUG)
            self.logger.addHandler(console_handler)
            
            # File handler for development
            file_handler = logging.FileHandler(log_dir / 'development.log')
            file_handler.setFormatter(detailed_formatter)
            file_handler.setLevel(logging.DEBUG)
            self.logger.addHandler(file_handler)
        else:
            # File handler for production (only critical and errors)
            file_handler = logging.FileHandler(log_dir / 'production.log')
            file_handler.setFormatter(simple_formatter)
            file_handler.setLevel(logging.ERROR)
            self.logger.addHandler(file_handler)
    
    @property
    def log_level(self) -> int:
        """Get current log level."""
        return self.logger.getEffectiveLevel()
    
    @log_level.setter
    def log_level(self, level: int) -> None:
        """Set log level for all handlers."""
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
    
    def get_logger(self, name: str = None) -> logging.Logger:
        """
        Get a logger instance.
        
        Args:
            name (str, optional): Logger name. Defaults to None.
        
        Returns:
            logging.Logger: Logger instance
        """
        if name:
            return self.logger.getChild(name)
        return self.logger

def get_logger(name: str = None) -> logging.Logger:
    """
    Convenience function to get a logger instance.
    
    Args:
        name (str, optional): Logger name. Defaults to None.
    
    Returns:
        logging.Logger: Logger instance
    """
    return LoggingManager().get_logger(name)

def log_function_call(func):
    """
    Decorator to log function calls if in development environment.
    
    Args:
        func: Function to be decorated
    
    Returns:
        wrapper: Decorated function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        # Only log in development environment
        if LoggingManager().environment == 'development':
            logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"{func.__name__} completed successfully")
                return result
            except Exception as e:
                logger.exception(f"Error in {func.__name__}: {str(e)}")
                raise
        else:
            return func(*args, **kwargs)
    
    return wrapper
