from app.backend.services.ollama import ask_llama_fix

# diseño del mensaje
fix_message = {
    "type": "fix",
    'original' : str,
    'content' : str,
}


class FixMessageService():
    MAX_LENGTH = 1000

    def __init__(self, message: str):
        self.message = message

    async def fix_message(self):
        self.message = self.message.strip()
        if not self.message:
            return {"error": "Empty message"}

        if len(self.message) > self.MAX_LENGTH:
            return {"error": f"Message too long, must be less than {self.MAX_LENGTH} characters"}

        try:
            fixed = await ask_llama_fix(self.message)
        except Exception as e:
            return {"error": f"An error occurred while processing the message: {str(e)}"}
        return {
            "type": "fix",
            "original": self.message, 
            "content": fixed
        }
    
