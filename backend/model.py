from typing import List, Optional
from datetime import date, datetime
from typing import Annotated
from fastapi import Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import table
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship

class baseModel(SQLModel,table=False):
    id: int = Field(default=None, primary_key=True)
    status: str
    created_datetimestamp: Optional[datetime] = Field(default=None, nullable=False)
    updated_datetimestamp: Optional[datetime] = Field(default=None, nullable=False)

class UserModel(baseModel,table=True):
    username : str
    email : str
    password : str
    isActive : str
    isLoggedIn : bool
    recipes: List["Recipe"] = Relationship(back_populates="user")

class Category(baseModel, table=True):
    catrgoryName: str
    # One-to-Many relationship (Category to Recipe)
    recipes: List["Recipe"] = Relationship(back_populates="category")

class RecipeIngredientLink(baseModel, table=True):
    recipe_id: Optional[int] = Field(default=None, foreign_key="recipe.id", primary_key=True)
    ingredient_id: Optional[int] = Field(default=None, foreign_key="ingredient.id", primary_key=True)

class Ingredient(baseModel, table=True):
    name: str
    # Many-to-Many relationship (Ingredient to Recipe)
    recipes: List["Recipe"] = Relationship(back_populates="ingredients", link_model=RecipeIngredientLink)

class Recipe(baseModel, table=True):
    receipeName: str
    receipeMethod: str
    receipeImagePath: str
    # Foreign key to Category
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    # One-to-Many relationship
    category: Optional[Category] = Relationship(back_populates="recipes")
    # Many-to-Many relationship
    ingredients: List[Ingredient] = Relationship(back_populates="recipes", link_model=RecipeIngredientLink)
    user : int = Field(foreign_key="usermodel.id")



sqlite_file_name = "database1.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    print('in here------------------')
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

