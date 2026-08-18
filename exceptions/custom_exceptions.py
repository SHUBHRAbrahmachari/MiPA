class ApiKeyNotFoundException(RuntimeError):
    def __init__(self, message):
        super().__init__(message)
        

class ChatModelDoesNotExistException(RuntimeError):
    def __init__(self, message: str):
        super().__init__(message)
        

class SummaryGenerationModelDoesNotExistException(RuntimeError):
    def __init__(self, message: str):
        super().__init__(message)


class ModelProviderNotSupportedException(RuntimeError):
    def __init__(self, message: str):
        super().__init__(message)
