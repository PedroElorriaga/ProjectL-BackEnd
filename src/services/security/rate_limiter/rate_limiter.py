from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta
from typing import Dict, List


class RateLimiter:
    """
    Rate limiter service that enforces request limits per IP address to prevent brute force attacks.
    In-memory IP-based rate limiter for Flask routes using a time window.
     - max_requests: Maximum number of requests allowed within the time window.
     - window_seconds: Time window in seconds for counting requests."""

    def __init__(self):
        self._requests: Dict[str, List[datetime]] = {}

    def _get_client_ip(self) -> str:
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        return request.remote_addr or 'unknown'

    def _cleanup_old_requests(self, ip: str, window_seconds: int):
        if ip in self._requests:
            cutoff_time = datetime.now() - timedelta(seconds=window_seconds)
            self._requests[ip] = [
                timestamp for timestamp in self._requests[ip]
                if timestamp > cutoff_time
            ]

    def limit(self, max_requests: int, window_seconds: int = 60):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                ip = self._get_client_ip()
                self._cleanup_old_requests(ip, window_seconds)
                if ip not in self._requests:
                    self._requests[ip] = []
                if len(self._requests[ip]) >= max_requests:
                    return jsonify({
                        'message': f'Muitas tentativas. Tente novamente em {window_seconds} segundos.',
                        'sucess': False
                    }), 429
                self._requests[ip].append(datetime.now())
                return f(*args, **kwargs)

            return decorated_function
        return decorator


rate_limiter = RateLimiter()
