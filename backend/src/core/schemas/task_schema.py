from pydantic import BaseModel


class TaskSchema(BaseModel):    
    description : str
    