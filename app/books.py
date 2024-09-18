from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title":"Title One", "author":"Author 1", "category":"Fiction"},
    {"title":"Title Two", "author":"Author 2", "category":"Science"},
    {"title":"Title Three", "author":"Author 3", "category":"Science"},
    {"title":"Title Four", "author":"Author 4", "category":"Health Care"}
]

@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param):
    return {'dynamic':dynamic_param}

@app.get("/books/param/{book_title}")
async def read_book(book_title:str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

@app.get("/books/qparam/")
async def read_book(category:str):
    books_to_return=[]
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return