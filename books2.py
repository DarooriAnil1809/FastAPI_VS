from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional
from starlette.responses import JSONResponse

#OVERVIEW
# class BOOKS(BaseModel):
#     id: UUID
#     title:str = Field(min_length=1)
#     author:str = Field(min_length=1, max_length=200)
#     description: Optional[str] = Field(title = "Description of the Title",
#                                         min_length=1,
#                                         max_length=100
#     )
#     rating:int= Field(gt=-1, lt=101)

app = FastAPI()


class Book(BaseModel):
    id:UUID
    title:str = Field(min_length=1, max_length=500)
    author:str
    description:str
    rating:int

#BASEMODEL CONFIGURATION
#DEFAULT VALUES

class config:
    schema_extra = {
        "example": {
            "ID": "558a5121-8bf5-4236-859f-0c7b0b527803",
            "title" : "AVATAR",
            "author": "JAMES CAMERON",
            "description": "ANIMATION MOVIE",
            "rating": "100"
        }
    }

BOOKS = []




#POST METHOD REQUEST from BASEMODEL
#OWN STATUS CODE
@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book:Book):
    BOOKS.append(book)
    return book


#create book objects

def create_books_no_api():
    book_1 = Book(id="558a5121-8bf5-4236-859f-0c7b0b527803",
                  title = "GAME OF THRONES",
                  author ="DAVID",
                  description = "HORROR",
                  rating = 100
    )
    book_2 = Book(id="658a5121-8bf5-4236-859f-0c7b0b527803",
                  title = "LORD OF THE RINGS",
                  author ="PETER JACKSON",
                  description = "FANTASY",
                  rating = 100
    )
    book_3 = Book(id="758a5121-8bf5-4236-859f-0c7b0b527803",
                  title = "BAHUBALI",
                  author ="RAJAMOULI",
                  description = "WAR",
                  rating = 99
    )
    book_4 = Book(id="858a5121-8bf5-4236-859f-0c7b0b527803",
                  title = "PUSHPA",
                  author ="SUKUMAR",
                  description = "CRIME",
                  rating = 99
    )
    book_5 = Book(id="958a5121-8bf5-4236-859f-0c7b0b527803",
                  title = "RRR",
                  author ="Rajamouli",
                  description = "ACTION",
                  rating = 100
    )

    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
    BOOKS.append(book_5)

# @app.get("/")
# async def read_all_books():
#     if len(BOOKS) < 1:
#         create_books_no_api()
#     return BOOKS

#GET REQUEST (ENHANCEMENT)
#HOW MANY BOOKS ARE WRITTEN WHICH SPECIFY IN API
@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

    if len(BOOKS) < 1:
        create_books_no_api()
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books =[]
        while i <= books_to_return:
            new_books.append(BOOKS[i-1])
            i+=1
        return new_books
    return BOOKS

#GET DATA BASED ON UUID
@app.get("/book{book_id}")
async def readbook(book_id:UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x

#PUT REQUEST METHOD
@app.put("/{book_id}")
async def update_book(book_id:UUID, book:Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]

#DELETE REQUEST METHOD
@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'ID:{book_id} deleted'
    raise raise_item_be_found_exception()        


#EXCEPTION HANDLING - RAISE HTTP EXCEPTION
#Call this function in delete_book - add similarly in all methods
def raise_item_be_found_exception():
    return HTTPException(status_code=404,
                         detail = "Book not Found",
                         headers={"X_Header_Error": "NOTHING TO SEEN UUID"}
    )

#CUSTOM HTTP EXCEPTION
#Negative Number Exception
class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request:Request,
                                            exception:NegativeNumberException
):
    return JSONResponse (
        status_code=418,
        content={"message": f"Hey why do you want{exception.books_to_return}"
                            f"books? you need read more!"}

)


#RESPONSE MODEL - TO REMOVE ELEMENT
#RATING REMOVE FROM LIST

class BookNoRating(BaseModel):
    id:UUID
    title:str = Field(min_length=1)
    author:str
    description: Optional[str] = Field(None, title="Description of Book", min_length=1, max_length=100)


#NEW API
@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id:UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_be_found_exception()

#FORM FIELDS
@app.post("/books/login")
async def book_login(username:str = Form(...),
                    password:str = Form(...)
):
    return {"username": username,
            "password" : password
    }


#Headers - addt requirements
@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header" : random_header}


