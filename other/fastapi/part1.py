from pydantic import BaseModel
from enum import Enum
from fastapi import FastAPI,Query,Path,Cookie, Header
from typing import Annotated # validation

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


# PATH PARAMETERS 
#1order matters in declaring same type of url
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

#2 creating and using enum in path parameters
class ModelName(str, Enum):
    alexnet = "alexne"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

# http://127.0.0.1:8000/models/alexnet
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # model_name is a value not a variable name
    # while ModelName is a class-- object
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

#3 Path parameters containing paths
# thsi has to written in same way {file_path:path} to get path in url
# http://127.0.0.1:8000/files//shop/category/productid
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# QUERY PARAMETERS
#1 Optional parameters
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# http://127.0.0.1:8000/items/?skip=0&limit=10
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

#2 Optional parameters and type conversion and multiple query parameters
# http://127.0.0.1:8000/user/1/items/foo?short=on || yes || true || True
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# REQUEST BODY
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

async def create_item(item: Item):
    # model_dump--- convert json in to python dict for manilution
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

#  **item.model_dump() -- deconstruct it, open it

# Query Parameters and String Validation
#1its length doesn't exceed 50 characters.
#  Annotated[str | None]=None --- is equal to --- q:str|None =None
# FastAPI will now: Validate the data
# previous version of fast api -> async def read_items(q: str | None = Query(default=None, max_length=50)):
# q: Annotated[str, Query()] = "rick"--> default value othe than None
# async def read_items(q: Annotated[str | None, Query(min_length=3) -> This would force clients to send a value, even if the value is None.
# async def read_items(q: Annotated[str, Query(min_length=3) -> make query required
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(min_length=3,max_length=50, pattern="^fixedquery$")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# 2http://localhost:8000/items/?q=foo&q=bar
# , you need to explicitly use Query, otherwise it would be interpreted as a request body.
# async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]): -- default value
# async def read_items(q: Annotated[list, Query()] = []):
# async def read_items(q: Annotated[list, Query()] = []):
@app.get("/items/")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items


#3http://127.0.0.1:8000/items/?item-query=foobaritems  --item-query is due to alias
@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
#4 There could be cases where you need to do some custom validation that can't be done with the parameters shown above.-- using pydantic library's AfterValidator function

#5 id, item = random.choice(list(data.items())) --- select random data from dict of key,value pair

#Path Parameters and Numeric Validations
#1 you can declare the same type of validations and metadata for path parameters with Path.
# from fastapi import FastAPI, Path, Query -- using Path function form FastApi
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# 2Python will complain if you put a value with a "default" before a value that doesn't have a "default".But you can re-order them, and have the value without a default (the query parameter q) first.
@app.get("/items/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
# But keep in mind that if you use Annotated, you won't have this problem, it won't matter as you're not using the function parameter default values for Query() or Path().
@app.get("/items/{item_id}")
async def read_items(
    q: str, item_id: Annotated[int, Path(title="The ID of the item to get")]
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

#3 Pass *, as the first parameter of the function.

# Python won't do anything with that *, but it will know that all the following parameters should be called as keyword arguments (key-value pairs), also known as kwargs. Even if they don't have a default value.
@app.get("/items/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# 4. number validation
@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str,
    size: Annotated[float, Query(gt=0, lt=10.5)],
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results

#Cookie Parameters
# Have in mind that, as browsers handle cookies in special ways and behind the scenes, they don't easily allow JavaScript to touch them.
# If you go to the API docs UI at /docs you will be able to see the documentation for cookies for your path operations.
# But even if you fill the data and click "Execute", because the docs UI works with JavaScript, the cookies won't be sent, and you will see an error message as if you didn't write any values.

# same parameters as as Path adn Query function have

# from fastapi import Cookie, FastAPI
@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}


# Header Parameters

# from fastapi import FastAPI, Header -- same as Cookie,Path and Query
# https://fastapi.tiangolo.com/tutorial/header-params/
# by default, Header will convert the parameter names characters from underscore (_) to hyphen (-) to extract and document the headers.
@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}