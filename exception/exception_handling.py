import sys
from typing import Optional

class CustomException(Exception):
    """
    Custom exception class for the AI Trip Planner application.
    Captures detailed error information including file name, line number, and error message.
    """
    
    def __init__(self, error_message: Exception, error_detail: sys):
        super().__init__(error_message)
        self.error_message = self._get_detailed_error_message(error_message, error_detail)
    
    @staticmethod
    def _get_detailed_error_message(error: Exception, error_detail: sys) -> str:
        """
        Extract detailed error information from the exception.
        
        Args:
            error: The exception object
            error_detail: System module to extract traceback information
            
        Returns:
            Formatted error message with file name, line number, and error details
        """
        _, _, exc_tb = error_detail.exc_info()
        
        if exc_tb is not None:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
            error_message = f"Error occurred in script: [{file_name}] at line number [{line_number}]: {str(error)}"
        else:
            error_message = f"Error: {str(error)}"
        
        return error_message
    
    def __str__(self):
        return self.error_message
    
    def __repr__(self):
        return f"CustomException({self.error_message})"