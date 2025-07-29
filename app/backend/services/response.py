from app.backend.services.ollama import ask_llama_response

message_response = {
    "type": "response",
    'original': str,
    'content': str,
}

class ResponseMessageService():
    MAX_LENGTH = 1000

    def __init__(self, message: str):
        self.message = message

    async def respond(self):
        self.message = self.message.strip()
        if not self.message:
            return {"error": "Empty message"}
        if len(self.message) > self.MAX_LENGTH:
            return {"error": f"Message too long, must be less than {self.MAX_LENGTH} characters"}
        try:
            response = await ask_llama_response(self.message)
        except Exception as e:
            return {"error": f"An error occurred while processing the message: {str(e)}"}
        return {
            "type": "response",
            "original": self.message,
            "content": response
        }