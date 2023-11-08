import datetime
import uuid
from enum import Enum
from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()


def _generate_int_id() -> int:
    return uuid.uuid4().int


class InvalidKeyException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class DogType(str, Enum):
    """An enumeration."""
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int = Field(default_factory=_generate_int_id) # By documentaion it's not required ???
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.exception_handler(InvalidKeyException)
async def invalid_key_handler(request: Request, exc: InvalidKeyException) -> JSONResponse:
    return JSONResponse(
        status_code=418,
        content={"message": exc.msg},
    )


@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse(content="Hello")


@app.post("/post")
def get_post() -> Timestamp:
    obj_id = _generate_int_id()
    obj_ts = int(datetime.datetime.now().timestamp())
    new_ts = Timestamp(id=obj_id, timestamp=obj_ts)
    post_db.append(new_ts)
    return new_ts


@app.get("/dog")
def get_dogs(kind: DogType = None) -> List[Dog]:
    current_dogs = list(dogs_db.values())
    if kind:
        current_dogs = list(filter(lambda x: x.kind == kind, current_dogs))
    return current_dogs


@app.post("/dog")
def create_dog(dog: Dog) -> Dog:
    if dog.pk in dogs_db:
        raise InvalidKeyException(msg=f"Key {dog.pk} already exists")
    dogs_db[dog.pk] = dog
    return dog


@app.get("/dog/{pk}")
def get_dog_by_pk(pk: int) -> Dog:
    dog = dogs_db.get(pk)
    if not dog:
        raise InvalidKeyException(msg=f"No dog found for key {pk}")
    return dog


@app.patch("/dog/{pk}")
def update_dog(pk: int, dog: Dog) -> Dog:
    if pk != dog.pk:
        raise InvalidKeyException(msg=f"Passed pk is {pk}, but dog pk is {dog.pk}")
    dogs_db[pk] = dog
    return dog
