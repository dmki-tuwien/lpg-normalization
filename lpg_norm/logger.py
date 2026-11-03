import logging

QUERY_LEVEL = 21
logging.addLevelName(QUERY_LEVEL, "QUERY")

class QueryLogger(logging.Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.setLevel(logging.INFO)
        self.propagate = False

    def query(self, msg, *args, **kwargs):
        if self.isEnabledFor(QUERY_LEVEL):
            self._log(QUERY_LEVEL, msg, args, **kwargs)