import os
import time
import logging
from datetime import datetime
from threading import Thread

# Log directory
LOG_DIR = "root_app/root_app/public/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Function to configure logging
def configure_logging(log_file):
    """Configures the logging module to use the specified log file."""
    # Clear existing handlers (to avoid duplicate log entries)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Set up new handlers
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),  # File logging
            logging.StreamHandler()        # Console logging
        ]
    )
    logging.info(f"Logging configured to use file: {log_file}")

# Function to validate log file
def validate_log_file():
    """Checks and creates the log file for the current date."""
    # Ensure the log directory exists
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Determine the current log file based on the date
    current_date = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(LOG_DIR, f"{current_date}.log")

    # Create the log file if it doesn't exist
    if not os.path.exists(log_file):
        with open(log_file, 'a') as f:
            f.write(f"Log initialized for {current_date}\n")
    
    return log_file

# Periodic log check in a background thread
def periodic_log_check():
    """Periodically validates and updates log files."""
    while True:
        try:
            log_file = validate_log_file()  # Get the current log file path
            configure_logging(log_file)    # Update logging configuration
        except Exception as e:
            logging.error(f"Error during log validation: {e}")
        time.sleep(3600)  # Check every hour

# Start the log checking thread
def start_background_tasks():
    """Start background tasks, like periodic log checks."""
    log_file = validate_log_file()  # Initial log file setup
    configure_logging(log_file)    # Configure logging initially
    log_check_thread = Thread(target=periodic_log_check, daemon=True)
    log_check_thread.start()
