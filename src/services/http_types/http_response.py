class HttpResponse:
    def __init__(self, body: dict = None, status: int = None):
        self.body = body
        self.status = status
