class BasePriceException(Exception):
    def __init__(self, message: str, status_code: int) -> None:
        self.message = message
        self.status_code = status_code


class PriceStatusError(BasePriceException):
    pass


class PriceRequestError(BasePriceException):
    pass
