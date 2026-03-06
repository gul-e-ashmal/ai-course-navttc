from typing import Annotated

from fastapi import FastAPI, Path,Query,Body,Response,status,File, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel,Field,HttpUrl

app = FastAPI()

#Body - Multiple Parameters
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

#multiple parameters -- item and user
@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item |None =None,
    user: User |None=None,
    importance: Annotated[int |None, Body()]=None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    if user:
        results.update({"user":user,"importance":importance})
    return results

# item: Item = Body(embed=True),  item: Annotated[Item, Body(embed=True)] --accept parameter in this way { "item":{}}

#Body - Fields
class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None

#Body - Nested Models
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = [] #list
    tags: set[str] = set() #set
    image: Image | None = None #nested url
    images: list[Image] | None = None # list of nested model

#not understand this
# @app.post("/index-weights/")
# async def create_index_weights(weights: dict[int, float]):
#     return weights

#Declare Request Example Data
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results


#RESPONSE MODEL RETURN TYPE
# https://fastapi.tiangolo.com/tutorial/response-model/ -- for deep learning
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]

#response_model Parameter
# If you added the return type annotation, tools and editors would complain with a (correct) error telling you that your function is returning a type (e.g. a dict) that is different from what you declared (e.g. a Pydantic model).
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item

# can return dict or database object
@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]

# understand the concept -- respose model will get the priority
class UserIn(BaseModel):
    username: str
    password: str
    # email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    # email: EmailStr
    full_name: str | None = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user

# still need to use return type instaed of response model-- then inhereitance is used
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str


@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user

# return type annotation

@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})


@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}

# basemodel have default value and you wantt to remove default values, only return those that are included

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]
#  response from items[0] data
{
    "name": "Foo",
    "price": 50.2
}



#1 leanr it everything will be in commnets
@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]


#2There are some cases where you need or want to return some data that is not exactly what the type declares.
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]






# RESPONSDE STATUS
# https://fastapi.tiangolo.com/tutorial/response-status-code/
@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}

# using status object from fastapi
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}



#FORM DATA
# $ pip install python-multipart---To use forms, first install python-multipart.

from fastapi import FastAPI, Form


# async def login(username: str = Form(), password: str = Form()):
@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}


#FORM MODELS
# SAME AS WWWW.URLFORMENCODED
class FormData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}

@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data

#REQUEST FILES
#https://fastapi.tiangolo.com/tutorial/request-files/
# from typing import Annotated
# from fastapi import FastAPI, File, UploadFile
# File is a class that inherits directly from Form.
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}
# Upload file has more advantage than File()
# https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


# full code of form file with html
# from fastapi.responses import HTMLResponse
@app.post("/files/")
async def create_files(files: Annotated[list[bytes] |None, File(description="A file read as bytes")]=None):
    return {"file_sizes": [len(file) for file in files]}

# file: Annotated[UploadFile, File(description="A file read as UploadFile")],
@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

#REQUEST FORM AND FILES


# practice 1
@app.get("/products/{productid}")
async def get_products(productid,discount: Annotated[int | None,Query()]=None):
    return {"productid":productid,"discount":discount}

#practice 2

class User(BaseModel):
    name: str
    age: int
    email: str

@app.post("/users")
async def create_users(user:User|None):
    return user

#practice 3

@app.put("/user/{userid}")
async def update_users(userid:Annotated[int ,Path(gt="0",le="99")],user:User|None):
    return user

class Order(BaseModel):
    item_name: str
    price: float | None=None
    quantity: int

#practive 4
@app.post("/orders/{orderid}")
async def create_orders(orderid:int, priority:Annotated[bool ,Query()]=False,order:Order |None =None):
    return {"orderid":orderid,"priority":priority,"order":order}

#practice 5 
@app.get("/students/{studentid}")
async def get_products(studentid: Annotated[int,Path(gt="0")],garde: Annotated[int | None,Query(gt="0",le="100")]=None):
    return {"studentid":studentid,"garde":garde}

#practice 6
class Account(BaseModel):
    username: str
    balance:  float = Field(ge=0)

@app.patch("/accounts/{accountid}")
async def create_account(
    accountid:Annotated[int,Path(gt=100)],
    active:Annotated[bool ,Query()]=False,
    account:Account |None =None
    ):
    return {"accountid":accountid,"active":active,"account":account}
