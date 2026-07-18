import logging
import sys
from pathlib import Path
import uuid
import time
import structlog
from config import LOG_PATH as _LOG_PATH

LOG_PATH = Path(_LOG_PATH)
LOG_PATH.parent.mkdir(exist_ok=True)


def _configure() -> None:
    tutor_logger = logging.getLogger("tutor")
    tutor_logger.setLevel(logging.INFO)
    tutor_logger.propagate = False
    if not tutor_logger.handlers:
        fmt = logging.Formatter("%(message)s")
        for handler in (logging.FileHandler(LOG_PATH), logging.StreamHandler(sys.stdout)):
            handler.setFormatter(fmt)
            tutor_logger.addHandler(handler)

    for noisy in ("httpx", "httpcore", "urllib3", "huggingface_hub", "sentence_transformers"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


_configure()
_log = structlog.get_logger("tutor")


def new_conversation_id() -> str:
    return str(uuid.uuid4())


def log_turn(**fields) -> None:
    event = fields.pop("event", "turn")
    _log.info(event, **fields)


class timed:
    def __init__(self, sink: dict, key: str = "latency_ms"):
        self.sink, self.key = sink, key

    def __enter__(self):
        self._t = time.perf_counter()
        return self

    def __exit__(self, *exc):
        self.sink[self.key] = round((time.perf_counter() - self._t) * 1000, 2)
        return False