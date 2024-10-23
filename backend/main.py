from typing import Annotated
from fastapi import Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from enum import Enum
from fastapi import FastAPI
from model import create_db_and_tables,get_session,SessionDep

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

    # getting path parameters
# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     return {"item_id": item_id}

# Path parameters with types
@app.get("/items1/{item_id}")
async def read_item1(item_id: int):
    return {"item_id": item_id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: bool):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: ModelName | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.on_event("startup")  
def on_startup():
    create_db_and_tables()

from model import Recipe

@app.post("/receipe/")
def create_receipe(receipe : Recipe, session: SessionDep):
    session.add(receipe)
    session.commit()
    session.refresh(receipe)
    return receipe

@app.get("/receipe/")
def read_receipes(session : SessionDep,offset: int = 0,
                 limit: Annotated[int, Query(le=100)] = 100,):
    receipes = session.exec(select(Recipe).offset(offset).limit(limit)).all()
    return receipes


@app.get("/receipe/{receipe_id}")
def read_receipe(receipt_id: int, session: SessionDep):
    receipe = session.get(Recipe, receipt_id)
    if not receipe:
        raise HTTPException(status_code=404, detail="Hero not found")
    return receipe
  

# @app.delete("/heroes/{hero_id}")
# def delete_hero(hero_id: int, session: SessionDep):
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     session.delete(hero)
#     session.commit()
#     return {"ok": True}