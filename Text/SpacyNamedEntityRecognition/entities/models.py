# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Schema


class SkillProperty(str, Enum):
    id = "id"
    name = "standardizedName"


class RecordDataRequest(BaseModel):
    text: str
    languageCode: str


class RecordRequest(BaseModel):
    recordId: str
    data: RecordDataRequest


class RecordsRequest(BaseModel):
    values: List[RecordRequest]

class Entity(BaseModel):
    text: str
    type_: str
    start: int
    end: int

class RecordDataResponse(BaseModel):
    entities: List[Entity]

class ResponseMessage(BaseModel):
    message: str

class RecordResponse(BaseModel):
    recordId: str
    data: RecordDataResponse
    errors: Optional[List[ResponseMessage]]
    warnings: Optional[List[ResponseMessage]]


class RecordsResponse(BaseModel):
    values: List[RecordResponse]