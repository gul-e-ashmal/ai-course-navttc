from fastapi import FastAPI,Path,Query
from typing import Annotated
from pydantic import BaseModel,Field
from enum import Enum


app = FastAPI()

#practice 1: GET /products/{product_id}
# Requirements:
# product_id must be an integer
# Must be greater than 0
# Optional query parameter include_reviews (boolean)
# If include_reviews=True, include reviews in response
# Example request:/products/12?include_reviews=true

@app.get("/products/{product_id}")
async def get_product(product_id:Annotated[int, Path(gt=0)] , include_reviews: Annotated[bool | None, Query()]=None):
    return {"product_id":product_id,"include_reviews":include_reviews}


# parctice 2: Question 2 — Search Products
# Create endpoint:GET /products/search
# Requirements:Query parameters:
# Parameter	Rules
# q	string, min_length=3, max_length=50
# category	optional
# limit	default=10, max=100
# skip	default=0
# Example:
# /products/search?q=laptop&category=electronics&limit=20

@app.get("/products/search")
async def search_product(
    q: Annotated[str , Query(min_length=3,max_length=50)],
    limit: Annotated[int , Query(max_length=100)]=10,
    skip: Annotated[int , Query()]=0
    ):
    return {"q":q,"limit":limit,"skip":skip}


# Question 3 — Create Product
# Endpoint:
# POST /products
# Request body model:
# Product
# - name
# - description
# - price
# - tax
# - stock_quantity
# Rules:
# price > 0
# tax optional
# if tax exists → return price_with_tax

class Product(BaseModel):
    name: str
    description: str 
    price: Annotated[float , Field(gt=0)]
    tax: float | None =None
    stock_quantity: int
@app.post("/products")
async def search_product(
    product: Product
    ):
    if (product.tax):
        price_with_tax = product.price + product.tax
        return {"name":product.name,"description":product.description,"price":product.price,"tax":product.tax,"stock_quantity":product.stock_quantity,"price_with_tax":price_with_tax}
    return product


# Question 4 — Product Category Enum
# Create enum:
# electronics
# clothing
# books
# furniture
# Endpoint:GET /products/category/{category}
# Return products by category.

class Category(Enum):
    electronics = "electronics"
    clothing = "clothing"
    books = "books"
    furniture = "furniture"


@app.get("/products/category/{category}")
async def search_product(
    category:Category
    ):
    if category.value in Category:
        return {"category":category.value}
    return {"error":"category not found"}



# Question 5 — Get Current Logged-in User
# Endpoint:
# GET /users/me
# Return mock user:
# {
#   "user_id": "current_user",
#   "role": "admin"
# }
# This should appear before:
# /users/{user_id}
@app.get("/users/me")
async def me(
    ):
   return  { "user_id": "current_user","role": "admin"}


# Question 6 — Get User Profile
# Endpoint:
# GET /users/{user_id}
# Rules:
# user_id must be integer
# greater than 0
# query param include_orders (bool)



# Question 7 — Create User
# Endpoint:
# POST /users
# Request body:
# User
# - username
# - email
# - age
# - is_active
# Rules:
# username min_length=4
# email must be string
# age > 18






# Practice Set 1 — E-commerce Product API
# Question 1 — Get Product Details

# Create an endpoint:

# GET /products/{product_id}

# Requirements:

# product_id must be an integer

# Must be greater than 0

# Optional query parameter include_reviews (boolean)

# If include_reviews=True, include reviews in response

# Example request:

# /products/12?include_reviews=true
# Question 2 — Search Products

# Create endpoint:

# GET /products/search

# Requirements:

# Query parameters:

# Parameter	Rules
# q	string, min_length=3, max_length=50
# category	optional
# limit	default=10, max=100
# skip	default=0

# Example:

# /products/search?q=laptop&category=electronics&limit=20
# Question 3 — Create Product

# Endpoint:

# POST /products

# Request body model:

# Product
# - name
# - description
# - price
# - tax
# - stock_quantity

# Rules:

# price > 0

# tax optional

# if tax exists → return price_with_tax

# Question 4 — Product Category Enum

# Create enum:

# electronics
# clothing
# books
# furniture

# Endpoint:

# GET /products/category/{category}

# Return products by category.

# Practice Set 2 — User Management API
# Question 5 — Get Current Logged-in User

# Endpoint:

# GET /users/me

# Return mock user:

# {
#   "user_id": "current_user",
#   "role": "admin"
# }

# This should appear before:

# /users/{user_id}
# Question 6 — Get User Profile

# Endpoint:

# GET /users/{user_id}

# Rules:

# user_id must be integer

# greater than 0

# query param include_orders (bool)

# Question 7 — Create User

# Endpoint:

# POST /users

# Request body:

# User
# - username
# - email
# - age
# - is_active

# Rules:

# username min_length=4

# email must be string

# age > 18

# Practice Set 3 — Order System (Realistic Backend Scenario)
# Question 8 — Get Orders with Filters

# Endpoint:

# GET /orders

# Query parameters:

# name	rules
# status	enum
# limit	default 20
# skip	default 0
# min_price	gt 0
# max_price	lt 10000

# Order status enum:

# pending
# shipped
# delivered
# cancelled

# Example:

# /orders?status=shipped&min_price=100
# Question 9 — Get Order Items

# Endpoint:

# GET /orders/{order_id}/items

# Rules:

# order_id must be integer

# greater than 0

# query param short=true to remove description

# Practice Set 4 — Query List Practice
# Question 10 — Filter Products by Tags

# Endpoint:

# GET /products/filter

# Query parameter:

# tags: list[str]

# Example request:

# /products/filter?tags=electronics&tags=gaming

# Response:

# {
#   "tags": ["electronics", "gaming"]
# }
# Practice Set 5 — Header and Cookie Practice
# Question 11 — Track User Device

# Endpoint:

# GET /analytics/device

# Read header:

# User-Agent

# Return:

# {
#   "device": "<user-agent>"
# }
# Question 12 — Read Tracking Cookie

# Endpoint:

# GET /ads

# Cookie parameter:

# ads_id

# Return:

# {
#  "ads_tracking_id": "value"
# }
# Practice Set 6 — Advanced Validation (Industry style)
# Question 13 — Inventory Update

# Endpoint:

# PUT /inventory/{product_id}

# Path validation:

# product_id >= 1

# Query parameter:

# warehouse_id (alias="warehouse-id")

# Body:

# InventoryUpdate
# - quantity

# Rules:

# quantity >= 0
# Practice Set 7 — File Path API
# Question 14 — Get File

# Endpoint:

# GET /files/{file_path:path}

# Example:

# /files/shop/images/product1.png

# Return file path.

# Practice Set 8 — Professional Query Metadata
# Question 15 — Product Search API (Production Style)

# Endpoint:

# GET /search

# Query parameter:

# query

# Requirements:

# Use Query metadata:

# title
# description
# alias="product-query"
# min_length=3
# max_length=50
# deprecated=True
# pattern="^[a-zA-Z0-9 ]+$"
# Bonus Challenge (Very Realistic)
# Question 16 — Complete Product Review API

# Endpoints:

# POST /products/{product_id}/reviews
# GET  /products/{product_id}/reviews

# Review model:

# Review
# - user_id
# - rating (1–5)
# - comment

# Rules:

# product_id >= 1

# rating between 1 and 5