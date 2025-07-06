from pydantic import BaseModel

class RewriteRequest(BaseModel):
    prompt: str

class SummarizeRequest(BaseModel):
    prompt: str
