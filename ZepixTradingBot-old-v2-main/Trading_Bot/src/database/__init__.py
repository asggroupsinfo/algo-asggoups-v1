"""
Database module
Handles all database operations
"""

__version__ = "2.0.0"

# Import TradeDatabase from parent module (src/database.py)
import importlib.util
import os

# Get the parent src directory
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
database_py_path = os.path.join(src_dir, 'database.py')

# Load database.py directly
spec = importlib.util.spec_from_file_location("database_module", database_py_path)
database_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(database_module)

# Export TradeDatabase
TradeDatabase = database_module.TradeDatabase
__all__ = ['TradeDatabase']
