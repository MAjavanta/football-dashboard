LOGGING_CONFIG_DEV = {
    "version": 1,
    "formatters": {
        "detailed": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
        "standard": {"format": "%(asctime)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "detailed",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "ingest": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "__main__": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {"level": "ERROR", "handlers": ["console", "file"]},
}
