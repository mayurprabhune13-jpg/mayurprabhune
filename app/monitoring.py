import logging
import time
from functools import wraps
from flask import request, current_app
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

class Monitoring:
    def __init__(self, app=None):
        self.app = app
        self.request_start_times = {}
        self.slow_request_threshold = 1.0  # seconds
        
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Ensure logs directory exists
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Set up application logger
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        
        # File handler for errors
        error_file_handler = RotatingFileHandler(
            'logs/errors.log',
            maxBytes=10240000,
            backupCount=10
        )
        error_file_handler.setFormatter(formatter)
        error_file_handler.setLevel(logging.ERROR)
        
        # File handler for general logs
        file_handler = RotatingFileHandler(
            'logs/application.log',
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # Configure app logger
        app.logger.addHandler(file_handler)
        app.logger.addHandler(error_file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application monitoring started')

        # Register monitoring endpoints
        @app.before_request
        def before_request():
            self.request_start_times[request.url] = time.time()

        @app.after_request
        def after_request(response):
            if request.url in self.request_start_times:
                elapsed_time = time.time() - self.request_start_times[request.url]
                
                # Log slow requests
                if elapsed_time > self.slow_request_threshold:
                    app.logger.warning(
                        f'Slow request: {request.method} {request.url} '
                        f'took {elapsed_time:.2f} seconds'
                    )
                
                # Log basic request info
                app.logger.info(
                    f'Request: {request.method} {request.url} '
                    f'Status: {response.status_code} '
                    f'Duration: {elapsed_time:.2f}s'
                )
                
                del self.request_start_times[request.url]
            
            return response

        @app.errorhandler(Exception)
        def handle_error(error):
            app.logger.error(f'Unhandled error: {str(error)}', exc_info=True)
            return 'Internal Server Error', 500

def log_function_call(func):
    """Decorator to log function calls with timing"""
    @wraps(func)
    def wrapped(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            current_app.logger.info(
                f'Function {func.__name__} completed in {elapsed_time:.2f}s'
            )
            return result
        except Exception as e:
            elapsed_time = time.time() - start_time
            current_app.logger.error(
                f'Function {func.__name__} failed after {elapsed_time:.2f}s: {str(e)}',
                exc_info=True
            )
            raise
    return wrapped

def log_db_query(query_func):
    """Decorator to log database queries with timing"""
    @wraps(query_func)
    def wrapped(*args, **kwargs):
        start_time = time.time()
        try:
            result = query_func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            if elapsed_time > 0.1:  # Log slow queries (>100ms)
                current_app.logger.warning(
                    f'Slow DB Query in {query_func.__name__}: {elapsed_time:.2f}s'
                )
            return result
        except Exception as e:
            current_app.logger.error(
                f'DB Query Error in {query_func.__name__}: {str(e)}',
                exc_info=True
            )
            raise
    return wrapped