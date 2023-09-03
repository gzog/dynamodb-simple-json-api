from fastapi import Path

KeyPath = Path(min_length=1, max_length=255, pattern="^[a-z0-9-]+$")
