import datetime as dt
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from fastapi import Depends, FastAPI
from loguru import logger

#uvicorn app:app --reload --port 8899
app = FastAPI()

class User(BaseModel):
    name: str
    surname: str
    age: int
    registration_date: dt.date

    class Config:
        orm_mode = True

def get_db():
    conn = psycopg2.connect(
        "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml",
        cursor_factory=RealDictCursor)
    return conn


@app.get("/stri")
def print_str_hello():
    return ("hello, world")


@app.get("/")
def sum_two_num(a: int, b: int) -> int:
    return a+b


@app.get("/sum_date")
def sum_day_and_num(current_date: dt.date, offset: int):
    result = current_date + dt.timedelta(offset)
    return result


@app.post("/user/validate")
def add_json_inf(user: User):
    return f"Will add user: {user.name} {user.surname} with age {user.age}"


@app.get("/user/{id}")
def get_id(id: int, db = Depends(get_db)):
    query = f"""
                    SELECT gender, age, city
                    FROM "user"
                    WHERE id = {id}
                """
    with db.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()

    if not result:
        raise HTTPException(404, "user not found")

    return result

class PostResponse(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True

@app.get("/post/{id}", response_model=PostResponse)
def return_info_posts(id: int, db = Depends(get_db)) -> PostResponse:
    query = """
                    SELECT id, text, topic
                    FROM post
                    WHERE id = %s
                """
    with db.cursor() as cursor:
        cursor.execute(query, (id,))
        result = cursor.fetchone()

    if not result:
        raise HTTPException(404, "post not found")

    return PostResponse(**result)
#Когда вы пишете PostResponse(**result), Python создает объект PostResponse,
#передавая поля id, text, и topic из словаря result в качестве аргументов для инициализации объекта.


