import logging
from logging import LogRecord
from typing import Iterable, TypeVar
import time

T = TypeVar('T')

class ProgressFormatter(logging.Formatter):
    def format(self, record: LogRecord) -> str:
        if hasattr(record, 'progress'):
            return f"Progress: {record.progress:.2f}% - {record.msg}"
        return record.msg

class LoggingManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggingManager, cls).__new__(cls)
            cls._instance._logger = None
        return cls._instance

    def setup_logging(self) -> None:
        if self._logger is None:
            self._logger = logging.getLogger(__name__)
            self._logger.setLevel(logging.INFO)
            
            formatter = ProgressFormatter()
            
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)

    def get_logger(self) -> logging.Logger:
        if self._logger is None:
            self.setup_logging()
        return self._logger

    def log(self, message: str) -> None:
        self.get_logger().info(message)

    def get_progress_logger(self, iterable: Iterable[T], total: int, log_interval: int = 1) -> Iterable[T]:
        logger = self.get_logger()
        start_time = time.time()
        last_print_time = start_time
        last_print_index = 0

        for i, item in enumerate(iterable, 1):
            yield item
            
            if i % log_interval == 0 or i == total:
                current_time = time.time()
                elapsed_time = current_time - start_time
                items_per_second = i / elapsed_time if elapsed_time > 0 else 0
                
                if items_per_second > 0:
                    estimated_total_time = total / items_per_second
                    estimated_remaining_time = estimated_total_time - elapsed_time
                else:
                    estimated_remaining_time = float('inf')
                
                if current_time - last_print_time >= 1 or i == total:  # Print at most once per second
                    progress = (i / total) * 100
                    if estimated_remaining_time != float('inf'):
                        time_string = self.format_time(estimated_remaining_time)
                        message = f"Processing item {i} of {total} (ETA: {time_string})"
                    else:
                        message = f"Processing item {i} of {total}"
                    
                    logger.info(message, extra={'progress': progress})
                    last_print_time = current_time
                    last_print_index = i

    @staticmethod
    def format_time(seconds: float) -> str:
        """Format time in a human-readable format."""
        if seconds == float('inf'):
            return "unknown"
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"

# Global instance
logging_manager = LoggingManager()