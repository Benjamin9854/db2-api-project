from litestar.exceptions import HTTPException
from litestar import Controller, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData
from advanced_alchemy.exceptions import NotFoundError
from sqlalchemy import select

from app.dtos import (
    AuthorReadDTO,
    AuthorReadFullDTO,
    AuthorUpdateDTO,
    AuthorWriteDTO,
    BookReadDTO,
    BookGetDTO,
    BookUpdateDTO,
    BookWriteDTO,
    ClientReadDTO,
    ClientReadFullDTO,
    ClientUpdateDTO,
    ClientWriteDTO
)
from app.models import Author, Book, Client
from app.repositories import (
    AuthorRepository,
    BookRepository,
    ClientRepository,
    provide_authors_repo,
    provide_books_repo,
    provide_clients_repo,
)


class AuthorController(Controller):
    path = "/authors"
    tags = ["authors"]
    return_dto = AuthorReadDTO
    dependencies = {"authors_repo": Provide(provide_authors_repo)}

    @get()
    async def list_authors(self, authors_repo: AuthorRepository) -> list[Author]:
        return authors_repo.list()

    @post(dto=AuthorWriteDTO)
    async def create_author(self, data: Author, authors_repo: AuthorRepository) -> Author:
        return authors_repo.add(data)

    @get("/{author_id:int}", return_dto=AuthorReadFullDTO)
    async def get_author(self, author_id: int, authors_repo: AuthorRepository) -> Author:
        try:
            return authors_repo.get(author_id)
        except NotFoundError:
            raise HTTPException("El autor no existe", status_code=404)

    @patch("/{author_id:int}", dto=AuthorUpdateDTO)
    async def update_author(
        self, author_id: int, data: DTOData[Author], authors_repo: AuthorRepository
    ) -> Author:
        try:
            author = authors_repo.get(author_id)
            author = data.update_instance(author)
            return authors_repo.update(author)
        except NotFoundError:
            raise HTTPException("El autor no existe", status_code=404)


class BookController(Controller):
    path = "/books"
    tags = ["books"]
    return_dto = BookReadDTO
    dependencies = {"books_repo": Provide(provide_books_repo)}

    @get()
    async def list_books(self, books_repo: BookRepository) -> list[Book]:
        return books_repo.list()
    
    @get("/{book_id:int}", return_dto=BookGetDTO)
    async def get_book(self, book_id: int, books_repo: BookRepository) -> Book:
        try:
            return books_repo.get(book_id)
        except NotFoundError:
            raise HTTPException("El libro no existe", status_code=404)
        
    # @get("/{book_title:str}", return_dto=BookGetDTO)
    # async def get_book_title(self, book_title: str, books_repo: BookRepository) -> Book:
    #     try:
    #         return books_repo._filter_by_like(statement=lambda field: field.like(f'%{book_title}%'),field_name=Book.title,value=book_title,ignore_case=True)
    #     except NotFoundError:
    #         raise HTTPException("El libro no existe", status_code=404)
    

    @patch("/{book_id:int}", dto=BookUpdateDTO)
    async def update_book(
        self, book_id: int, data: DTOData[Book], books_repo: BookRepository
    ) -> Book:
        try:
            book = books_repo.get(book_id)
            book = data.update_instance(book)
            return books_repo.update(book)
        except NotFoundError:
            raise HTTPException("El libro no existe", status_code=404)

    @post(dto=BookWriteDTO)
    async def create_book(self, data: Book, books_repo: BookRepository) -> Book:
        return books_repo.add(data)
    




class ClientController(Controller):
    path = "/clients"
    tags = ["clients"]
    return_dto = ClientReadDTO
    dependencies = {"clients_repo": Provide(provide_clients_repo)}

    @get()
    async def list_clients(self, clients_repo: ClientRepository) -> list[Client]:
        return clients_repo.list()

    @post(dto=ClientWriteDTO)
    async def create_client(self, data: Client, clients_repo: ClientRepository) -> Client:
        return clients_repo.add(data)
