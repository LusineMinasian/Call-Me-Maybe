from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class ParameterType(BaseModel):
    type: str


class FunctionDefinition(BaseModel):
    name: str = Field(min_length=1)
    description: str
    parameters: dict[str, ParameterType]
    returns: ParameterType


class PromptItem(BaseModel):
    prompt: str


class FunctionCall(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt: str
    name: str
    parameters: dict[str, Any]
