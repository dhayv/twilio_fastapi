import uuid


class AIResponse:
    def __init__(self) -> None:
        self.responses = {}

    def generate_id(self):
        return str(uuid.uuid4())

    def store_response(self, request_id, response):
        self.responses[request_id] = response

    def get_response(self, request_id):
        return self.responses.get(request_id)
