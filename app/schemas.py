from fastapi import Path

# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.NamingRulesDataTypes.html
KeyPath = Path(min_length=1, max_length=255, pattern="[a-z0-9_\.\-]+")
