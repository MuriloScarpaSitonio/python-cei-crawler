class CeiCrawlerUnableToLoginException(Exception):
    pass


class CeiCrawlerBlankCredentialsException(Exception):
    DEFAULT_MESSAGE = "Username ou password não podem estar em branco!"

    def __init__(self, *args: object) -> None:
        if args:
            super().__init__(*args)
        else:
            super().__init__(self.DEFAULT_MESSAGE)
