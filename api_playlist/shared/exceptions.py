class NotFound(Exception):
    """creating a NotFound exception class to validate my routers"""

    def __init__(self, name: str):
        self.name = name
