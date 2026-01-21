"""
Centralized Logging Configuration for Zepix Trading Bot v2.0
Provides LogLevel enum and LoggingConfig class for intelligent logging control

Enhanced with error-specific logging based on:
Updates/telegram_updates/09_ERROR_HANDLING_GUIDE.md
"""

import logging
import logging.handlers
import os
from enum import Enum
from datetime import datetime
from pathlib import Path


class LogLevel(Enum):
    """Log level enumeration for filtering messages"""
    DEBUG = 1
    INFO = 2  
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


class LoggingConfig:
    """
    Centralized logging configuration with trading debug mode support.
    
    Features:
    - Configurable log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - Console and file logging control
    - Trading debug mode for detailed trend-signal analysis
    - Log rotation with size limits
    """
    
    def __init__(self):
        # Core logging settings
        self.current_level = LogLevel.INFO
        self.enable_console_logs = True
        self.enable_file_logs = True
        
        # File logging configuration
        self.log_file = "logs/bot_activity.log"
        self.max_file_size = 10 * 1024 * 1024  # 10MB max file size
        self.backup_count = 5  # Keep 5 backup files
        
        # TRADING DEBUG MODE - For detailed trend-signal analysis
        # When enabled, logs all trading decisions with full context
        self.trading_debug = True
        
        # Create logs directory if not exists
        os.makedirs("logs", exist_ok=True)
        
        # Load saved log level from config (PERSISTENCE across restarts)
        self._load_log_level_from_config()
        
    def set_level(self, level: LogLevel):
        """Change the current logging level"""
        self.current_level = level
        
    def should_log(self, message_level: LogLevel) -> bool:
        """Check if a message with given level should be logged"""
        return message_level.value >= self.current_level.value
    
    def enable_trading_debug(self):
        """Enable detailed trading debug logging"""
        self.trading_debug = True
        
    def disable_trading_debug(self):
        """Disable trading debug logging"""
        self.trading_debug = False
    
    def _load_log_level_from_config(self):
        """Load saved log level from config file (if exists)"""
        try:
            import json
            config_file = "config/logging_settings.json"
            
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    settings = json.load(f)
                    level_name = settings.get("log_level", "INFO")
                    
                    # Map string to LogLevel enum
                    level_map = {
                        "DEBUG": LogLevel.DEBUG,
                        "INFO": LogLevel.INFO,
                        "WARNING": LogLevel.WARNING,
                        "ERROR": LogLevel.ERROR,
                        "CRITICAL": LogLevel.CRITICAL
                    }
                    
                    if level_name in level_map:
                        self.current_level = level_map[level_name]
                        print(f"[LOGGING CONFIG] Loaded saved log level: {level_name}")
                        # Load trading_debug setting
                        trading_debug = settings.get("trading_debug", False)
                        self.trading_debug = trading_debug
                        print(f"[LOGGING CONFIG] Loaded trading_debug: {trading_debug}")
                    else:
                        print(f"[LOGGING CONFIG] Invalid saved level '{level_name}', using default INFO")
            else:
                print("[LOGGING CONFIG] No saved log level, using default INFO")
        except Exception as e:
            print(f"[LOGGING CONFIG] Could not load log level from config: {e}, using default INFO")


def setup_error_logging(log_dir: str = "logs"):
    """
    Setup enhanced error logging with separate error log file.
    Based on: Updates/telegram_updates/09_ERROR_HANDLING_GUIDE.md
    
    Creates:
    - logs/bot.log: All logs (INFO and above)
    - logs/errors.log: Error logs only (ERROR and above)
    
    Args:
        log_dir: Directory for log files
    """
    try:
        # Create log directory
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        # Define log format - matches document specification
        log_format = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        
        # Create formatter
        formatter = logging.Formatter(log_format, datefmt=date_format)
        
        # Setup root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # 1. Console handler (INFO and above)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # 2. Main log file handler (INFO and above)
        bot_log_file = os.path.join(log_dir, 'bot.log')
        file_handler = logging.handlers.RotatingFileHandler(
            bot_log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        
        # 3. Error log file handler (ERROR and above only)
        error_log_file = os.path.join(log_dir, 'errors.log')
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        root_logger.addHandler(error_handler)
        
        logging.info("✅ Enhanced error logging configured")
        logging.info(f"   - Main log: {bot_log_file}")
        logging.info(f"   - Error log: {error_log_file}")
        
    except Exception as e:
        print(f"Error setting up error logging: {e}")


def get_error_logger(name: str = None):
    """
    Get logger instance for error handling
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name or __name__)



# Global logging configuration instance
logging_config = LoggingConfig()
