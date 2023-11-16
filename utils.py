import hashlib
import re


def hash_url(url):
    return hashlib.md5(url.encode()).hexdigest()

def sanitize_filename(url):
    # Remove protocol (http://, https://)
    sanitized = re.sub(r'^https?:\/\/', '', url)
    # Replace illegal characters with underscores
    sanitized = re.sub(r'[\.<>:"/\\|?*]', '_', sanitized)
    return sanitized

def create_safe_filename(url, max_length=255):
    hash_part = hash_url(url)
    sanitized_part = sanitize_filename(url)

    # Truncate sanitized part if necessary
    max_sanitized_length = max_length - len(hash_part) - 1  # accounting for the underscore
    sanitized_part = sanitized_part[:max_sanitized_length]

    return f"{sanitized_part}_{hash_part}"

