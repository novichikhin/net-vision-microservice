class BaseAppException(Exception):

    @property
    def message(self) -> str:
        return "Base app exception"
