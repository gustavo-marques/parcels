import logging

__all__ = ('logger')

warning_once_level = 25


class DuplicateFilter(object):
    def __init__(self):
        self.msgs = set()

    def filter(self, record):
        rv = record.msg not in self.msgs
        if record.levelno == warning_once_level:
            self.msgs.add(record.msg)
        return rv


def warning_once(self, message, *args, **kws):
    if self.isEnabledFor(warning_once_level):
        self._log(warning_once_level, message, args, **kws)


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt="%(levelname)s: %(message)s"))
logger.addHandler(handler)

logging.addLevelName(warning_once_level, "WARNING")
logging.Logger.warning_once = warning_once

dup_filter = DuplicateFilter()
logger.addFilter(dup_filter)
logger.setLevel(10)