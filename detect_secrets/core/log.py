import logging
import sys
from functools import partial
from typing import cast
from typing import Optional


def get_logger(name: Optional[str] = None, format_string: Optional[str] = None) -> 'CustomLogger':
    """
    :param name: used for declaring log channels.
    :param format_string: for custom formatting
    """
    logging.captureWarnings(True)
    log = logging.getLogger(name)

    # Bind custom method to instance.
    # Source: https://stackoverflow.com/a/2982
    log.set_debug_level = partial(CustomLogger.set_debug_level, log)    # type: ignore
    cast(CustomLogger, log).set_debug_level(0)

    # Setting up log formats
    log.handlers = []
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter(
            format_string
            or
            '[%(module)s]\t%(levelname)s\t%(message)s',
        ),
    )
    log.addHandler(handler)

    return cast(CustomLogger, log)


def _set_debug_level(self: logging.Logger, debug_level: int) -> None:
    """
    :param debug_level: between 0-2, configure verbosity of log
    """
    mapping = {
        0: logging.ERROR,
        1: logging.INFO,
        2: logging.DEBUG,
    }

    self.setLevel(
        mapping[min(debug_level, 2)],
    )


class CustomLogger(logging.Logger):
    def set_debug_level(self, debug_level: int) -> None:
        """
        :param debug_level: between 0-2, configure verbosity of log
        """
        mapping = {
            0: logging.ERROR,
            1: logging.INFO,
            2: logging.DEBUG,
        }

        self.setLevel(
            mapping[min(debug_level, 2)],
        )


log = get_logger('detect-secrets')
