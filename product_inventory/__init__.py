import json

from loguru import logger


def serialize(record):
    subset = {
        "timestamp": record["time"].timestamp(),
        "file.name": record["file"].path,
        "func": record["function"],
        "line.number": record["line"],
        "log.level": record["level"].name,
        "message": record["message"],
        "exception": record["exception"],
        **record["extra"],
    }
    return json.dumps(subset, default=str)


def sink(message):
    serialized = serialize(message.record)
    print(serialized)


def formatter(record):
    # Note this function returns the string to be formatted, not the actual message to be logged
    # return "{time:YYYY-MM-DD HH:mm:ss} [application_name] [{extra[correlationId]}] [{level}] - {name}:{function}:{line} - {message}\n"
    return (
        "{time} | {level: <8} | {name: ^15} | {function: ^15} | {line: >3} | {message}"
    )


logger.remove()
logger.add(sink, format=formatter)
logger.level("EXCEPTION", no=38, color="<red>")