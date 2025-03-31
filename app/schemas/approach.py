from pydantic import BaseModel, ConfigDict

class ApproachBase(BaseModel):
    name: str

class ApproachCreate(ApproachBase):
    pass

class ApproachResponse(ApproachBase):
    approach_id: int

    model_config = ConfigDict(from_attributes=True)