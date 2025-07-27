from pydantic import BaseModel

class promtRequest(BaseModel):
    prompt: str

class promtResponse(BaseModel):
    response :str