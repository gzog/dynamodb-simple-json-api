import json
import logging
from app.settings import settings
from logging import Formatter, LogRecord


class JsonFormatter(Formatter):
    def __init__(self) -> None:
        super(JsonFormatter, self).__init__()

    def format(self, record: LogRecord) -> str:
        json_record = {}
        json_record["message"] = record.getMessage()
        if "req" in record.__dict__:
            json_record["req"] = record.__dict__["req"]
        if "res" in record.__dict__:
            json_record["res"] = record.__dict__["res"]
        if record.levelno == logging.ERROR and record.exc_info:
            json_record["err"] = self.formatException(record.exc_info)
        return json.dumps(json_record)


for name, logger in logging.root.manager.loggerDict.items():
    logger.disabled = settings.disable_existing_loggers  # type: ignore


logger = logging.root
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.handlers = [handler]
logger.setLevel(settings.log_level)
