import logging
from logging.handlers import RotatingFileHandler


class Logger:
    """
    Output information up to the debug level to the terminal,
    and output information up to the warning level to a file.
    """

    def __init__(self, logger_name: str) -> None:
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # Streamハンドラクラスをインスタンス化
        st_handler = logging.StreamHandler()
        st_handler.setLevel(logging.DEBUG)

        # Fileハンドラクラスをインスタンス化
        fl_handler = RotatingFileHandler(
            filename="template.log",
            encoding="utf-8",
            maxBytes=100 * 1024,  # 100KB
            backupCount=5,
        )
        fl_handler.setLevel(logging.WARNING)

        self.logger.addHandler(st_handler)
        self.logger.addHandler(fl_handler)
