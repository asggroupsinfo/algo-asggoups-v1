"""
Error Codes and Constants

Centralized error code definitions for the trading bot.
Based on: Updates/telegram_updates/09_ERROR_HANDLING_GUIDE.md
"""

# ============================================================================
# ERROR CODE PREFIXES
# ============================================================================

ERROR_PREFIX_TELEGRAM = "TG"
ERROR_PREFIX_MT5 = "MT"
ERROR_PREFIX_DATABASE = "DB"
ERROR_PREFIX_PLUGIN = "PL"
ERROR_PREFIX_TRADING = "TE"
ERROR_PREFIX_NOTIFICATION = "NF"
ERROR_PREFIX_MENU = "MN"

# ============================================================================
# ERROR SEVERITY LEVELS
# ============================================================================

SEVERITY_CRITICAL = "CRITICAL"  # 🔴 Requires immediate action
SEVERITY_MAJOR = "MAJOR"        # 🟠 Needs attention soon
SEVERITY_MINOR = "MINOR"        # 🟡 Auto-recoverable
SEVERITY_INFO = "INFO"          # 🟢 Informational only

# ============================================================================
# TELEGRAM API ERROR CODES
# ============================================================================

TG_001_HTTP_409 = "TG-001"          # HTTP 409 Conflict - Multiple bot instances
TG_002_RATE_LIMIT = "TG-002"        # Rate limit exceeded
TG_003_INVALID_TOKEN = "TG-003"     # Invalid or revoked token
TG_004_CHAT_NOT_FOUND = "TG-004"    # Chat ID invalid or blocked
TG_005_MESSAGE_TOO_LONG = "TG-005"  # Message > 4096 chars
TG_006_CALLBACK_EXPIRED = "TG-006"  # Callback query too old

# ============================================================================
# MT5 ERROR CODES
# ============================================================================

MT_001_CONNECTION_FAILED = "MT-001"  # MT5 connection lost
MT_002_ORDER_FAILED = "MT-002"       # Order execution failed
MT_003_INVALID_SYMBOL = "MT-003"     # Symbol not available

# MT5 Native Error Code Mapping
MT5_ERROR_CODES = {
    10004: "Requote - price changed",
    10006: "Request rejected",
    10009: "Invalid request",
    10010: "Invalid price",
    10014: "Invalid volume",
    10015: "Invalid stops",
    10016: "Trade disabled",
    10017: "Market closed",
    10018: "Insufficient funds",
    10019: "Prices changed",
    10020: "No quotes",
    10021: "Invalid expiration",
    10022: "Order changed",
    10023: "Too many requests",
    10024: "No changes",
    10025: "Autotrading disabled by server",
    10026: "Autotrading disabled by client terminal",
    10027: "Request locked",
    10028: "Order or position frozen",
    10029: "Invalid order filling type",
    10030: "No connection to trade server",
    10031: "Operation not allowed in demo",
    10032: "Order limit exceeded",
    10033: "Margin requirement exceeded"
}

# ============================================================================
# DATABASE ERROR CODES
# ============================================================================

DB_001_CONNECTION_ERROR = "DB-001"     # Database connection lost (also stored as DB_001_CONNECTION_LOST for compatibility)
DB_001_CONNECTION_LOST = "DB-001"      # Alias for backward compatibility
DB_002_TABLE_MISSING = "DB-002"        # Required table missing (also stored as DB_002_TABLE_NOT_FOUND)
DB_002_TABLE_NOT_FOUND = "DB-002"      # Alias for backward compatibility
DB_003_CONSTRAINT_VIOLATION = "DB-003" # Data constraint violated (also stored as DB_003_INTEGRITY_ERROR)
DB_003_INTEGRITY_ERROR = "DB-003"      # Alias for backward compatibility

# ============================================================================
# PLUGIN SYSTEM ERROR CODES
# ============================================================================

PL_001_LOAD_FAILED = "PL-001"         # Plugin load failed
PL_002_PROCESS_ERROR = "PL-002"       # Plugin crashed during processing
PL_003_CONFIG_ERROR = "PL-003"        # Invalid plugin configuration

# ============================================================================
# TRADING ENGINE ERROR CODES
# ============================================================================

TE_001_INVALID_SIGNAL = "TE-001"      # Signal validation failed
TE_002_RISK_LIMIT = "TE-002"          # Risk limit exceeded
TE_003_DUPLICATE = "TE-003"           # Duplicate signal blocked

# ============================================================================
# NOTIFICATION ERROR CODES
# ============================================================================

NF_001_QUEUE_FULL = "NF-001"          # Notification queue full
NF_002_VOICE_FAILED = "NF-002"        # Voice alert failed

# ============================================================================
# MENU SYSTEM ERROR CODES
# ============================================================================

MN_001_HANDLER_NOT_FOUND = "MN-001"   # Callback handler not found
MN_002_BUILD_ERROR = "MN-002"         # Menu build failed

# ============================================================================
# ERROR MESSAGES
# ============================================================================

ERROR_MESSAGES = {
    # Telegram
    TG_001_HTTP_409: "HTTP 409 Conflict - Multiple bot instances running",
    TG_002_RATE_LIMIT: "Rate limit exceeded - Too many requests",
    TG_003_INVALID_TOKEN: "Invalid or revoked Telegram token",
    TG_004_CHAT_NOT_FOUND: "Chat not found - User may have blocked bot",
    TG_005_MESSAGE_TOO_LONG: "Message exceeds 4096 character limit",
    TG_006_CALLBACK_EXPIRED: "Callback query expired",
    
    # MT5
    MT_001_CONNECTION_FAILED: "MT5 connection failed",
    MT_002_ORDER_FAILED: "Order execution failed",
    MT_003_INVALID_SYMBOL: "Symbol not available in MT5",
    
    # Database
    DB_001_CONNECTION_LOST: "Database connection lost",
    DB_002_TABLE_NOT_FOUND: "Required database table missing",
    DB_003_INTEGRITY_ERROR: "Data integrity constraint violated",
    
    # Plugin
    PL_001_LOAD_FAILED: "Plugin load failed",
    PL_002_PROCESS_ERROR: "Plugin crashed during signal processing",
    PL_003_CONFIG_ERROR: "Invalid plugin configuration",
    
    # Trading Engine
    TE_001_INVALID_SIGNAL: "Signal validation failed",
    TE_002_RISK_LIMIT: "Risk limit exceeded",
    TE_003_DUPLICATE: "Duplicate signal blocked",
    
    # Notification
    NF_001_QUEUE_FULL: "Notification queue full",
    NF_002_VOICE_FAILED: "Voice alert generation failed",
    
    # Menu
    MN_001_HANDLER_NOT_FOUND: "Callback handler not found",
    MN_002_BUILD_ERROR: "Menu build failed"
}

# ============================================================================
# AUTO-RECOVERY CONFIGURATION
# ============================================================================

AUTO_RECOVERY_ENABLED = {
    TG_001_HTTP_409: True,           # Restart polling
    TG_002_RATE_LIMIT: True,         # Wait and retry
    TG_003_INVALID_TOKEN: False,     # Manual fix required
    TG_004_CHAT_NOT_FOUND: True,     # Remove from list
    TG_005_MESSAGE_TOO_LONG: True,   # Split message
    TG_006_CALLBACK_EXPIRED: True,   # Send fresh menu
    
    MT_001_CONNECTION_FAILED: True,  # Auto reconnect
    MT_002_ORDER_FAILED: True,       # Retry with backoff (partial)
    MT_003_INVALID_SYMBOL: False,    # Manual fix required
    
    DB_001_CONNECTION_LOST: True,    # Reconnect
    DB_002_TABLE_NOT_FOUND: True,    # Create tables
    DB_003_INTEGRITY_ERROR: True,    # Use INSERT OR REPLACE
    
    PL_001_LOAD_FAILED: False,       # Manual fix required
    PL_002_PROCESS_ERROR: True,      # Isolate and continue
    PL_003_CONFIG_ERROR: True,       # Use defaults
    
    TE_001_INVALID_SIGNAL: True,     # Reject and notify
    TE_002_RISK_LIMIT: False,        # Wait for reset
    TE_003_DUPLICATE: True,          # Block silently
    
    NF_001_QUEUE_FULL: True,         # Drop oldest
    NF_002_VOICE_FAILED: True,       # Fallback to text
    
    MN_001_HANDLER_NOT_FOUND: True,  # Show warning
    MN_002_BUILD_ERROR: True         # Fallback menu
}

# ============================================================================
# SEVERITY EMOJI MAPPING
# ============================================================================

SEVERITY_EMOJI = {
    SEVERITY_CRITICAL: "🔴",
    SEVERITY_MAJOR: "🟠",
    SEVERITY_MINOR: "🟡",
    SEVERITY_INFO: "🟢"
}

# ============================================================================
# ERROR CATEGORY MAPPING
# ============================================================================

ERROR_SEVERITY = {
    # CRITICAL errors
    TG_001_HTTP_409: SEVERITY_CRITICAL,
    TG_003_INVALID_TOKEN: SEVERITY_CRITICAL,
    MT_001_CONNECTION_FAILED: SEVERITY_CRITICAL,
    
    # MAJOR errors
    TG_004_CHAT_NOT_FOUND: SEVERITY_MAJOR,
    TG_002_RATE_LIMIT: SEVERITY_MAJOR,
    MT_002_ORDER_FAILED: SEVERITY_MAJOR,
    MT_003_INVALID_SYMBOL: SEVERITY_MAJOR,
    DB_001_CONNECTION_LOST: SEVERITY_MAJOR,
    DB_002_TABLE_NOT_FOUND: SEVERITY_MAJOR,
    PL_001_LOAD_FAILED: SEVERITY_MAJOR,
    PL_002_PROCESS_ERROR: SEVERITY_MAJOR,
    
    # MINOR errors
    TG_005_MESSAGE_TOO_LONG: SEVERITY_MINOR,
    TG_006_CALLBACK_EXPIRED: SEVERITY_MINOR,
    DB_003_INTEGRITY_ERROR: SEVERITY_MINOR,
    PL_003_CONFIG_ERROR: SEVERITY_MINOR,
    TE_001_INVALID_SIGNAL: SEVERITY_MINOR,
    TE_002_RISK_LIMIT: SEVERITY_MINOR,
    TE_003_DUPLICATE: SEVERITY_MINOR,
    NF_001_QUEUE_FULL: SEVERITY_MINOR,
    NF_002_VOICE_FAILED: SEVERITY_MINOR,
    MN_001_HANDLER_NOT_FOUND: SEVERITY_MINOR,
    MN_002_BUILD_ERROR: SEVERITY_MINOR
}

# ============================================================================
# REQUIRED SIGNAL FIELDS
# ============================================================================

REQUIRED_SIGNAL_FIELDS = [
    'symbol',      # e.g., "XAUUSD"
    'direction',   # "BUY" or "SELL"
    'entry',       # Entry price
]

OPTIONAL_SIGNAL_FIELDS = [
    'sl',          # Stop loss price
    'tp',          # Take profit price
    'logic',       # Logic route (LOGIC1/2/3)
    'timeframe',   # Timeframe (1M/5M/15M/etc)
    'plugin_id',   # Plugin identifier
    'timestamp',   # Signal timestamp
]

# ============================================================================
# CONSTANTS
# ============================================================================

# Telegram limits
MAX_MESSAGE_LENGTH = 4096
MAX_CALLBACK_DATA_LENGTH = 64
MAX_BUTTON_TEXT_LENGTH = 64

# Queue limits
MAX_NOTIFICATION_QUEUE_SIZE = 100

# Retry limits
MAX_MT5_RECONNECT_ATTEMPTS = 5
MAX_DB_RECONNECT_ATTEMPTS = 3

# Timeouts
PLUGIN_PROCESS_TIMEOUT = 30.0  # seconds
MT5_RECONNECT_DELAY = 10  # seconds
DB_RECONNECT_DELAY = 5  # seconds

# Logging
LOG_FILE_BOT = 'logs/bot.log'
LOG_FILE_ERRORS = 'logs/errors.log'
LOG_FORMAT = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
