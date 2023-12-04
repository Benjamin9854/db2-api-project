from datetime import datetime, timedelta
from litestar.exceptions import HTTPException
from litestar import Controller, get, patch, post, delete
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
    CategoryReadDTO,
    CategoryReadFullDTO,
    CategoryUpdateDTO,
    CategoryWriteDTO,
    ClientReadDTO,
    ClientReadFullDTO,
    ClientUpdateDTO,
    ClientWriteDTO,
    LoanReadDTO,
    LoanReadFullDTO,
    LoanWriteDTO,
)
from app.models import Author, Book, Category, Client, Loan
from app.repositories import (
    AuthorRepository,
    BookRepository,
    CategoryRepository,
    ClientRepository,
    LoanRepository,
    provide_authors_repo,
    provide_books_repo,
    provide_categories_repo,
    provide_clients_repo,
    provide_loans_repo,
)


class AuthorController(Controller):
    path = "/authors"
    tags = ["authors"]
    return_dto = AuthorReadDTO
    dependencies = {"authors_repo": Provide(provide_authors_repo)}

    @get()
    async def list_authors(self, authors_repo: AuthorRepository) -> list[Author]:
        return authors_repo.list()

    @get("/{author_id:int}", return_dto=AuthorReadFullDTO)
    async def get_author(
        self, author_id: int, authors_repo: AuthorRepository
    ) -> Author:
        try:
            return authors_repo.get(author_id)
        except NotFoundError:
            raise HTTPException("El autor no existe", status_code=404)

    @post(dto=AuthorWriteDTO)
    async def create_author(
        self, data: Author, authors_repo: AuthorRepository
    ) -> Author:
        return authors_repo.add(data)

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


class CategoryController(Controller):
    path = "/categories"
    tags = ["categories"]
    return_dto = CategoryReadDTO
    dependencies = {"categories_repo": Provide(provide_categories_repo)}

    @get()
    async def list_categories(
        self, categories_repo: CategoryRepository
    ) -> list[Category]:
        return categories_repo.list()

    @post(dto=CategoryWriteDTO)
    async def create_category(
        self, data: Category, categories_repo: CategoryRepository
    ) -> Category:
        return categories_repo.add(data)

    @patch("/{category_id:int}", dto=CategoryUpdateDTO)
    async def update_category(
        self,
        category_id: int,
        data: DTOData[Category],
        categories_repo: CategoryRepository,
    ) -> Category:
        try:
            category = categories_repo.get(category_id)
            category = data.update_instance(category)
            return categories_repo.update(category)
        except NotFoundError:
            raise HTTPException("La categoria no existe", status_code=404)


class ClientController(Controller):
    path = "/clients"
    tags = ["clients"]
    return_dto = ClientReadDTO
    dependencies = {"clients_repo": Provide(provide_clients_repo)}

    @get()
    async def list_clients(self, clients_repo: ClientRepository) -> list[Client]:
        return clients_repo.list()

    @post(dto=ClientWriteDTO)
    async def create_client(
        self, data: Client, clients_repo: ClientRepository
    ) -> Client:
        return clients_repo.add(data)

    @get("/{client_id:int}", return_dto=ClientReadFullDTO)
    async def get_client(
        self, client_id: int, clients_repo: ClientRepository
    ) -> Client:
        try:
            return clients_repo.get(client_id)
        except NotFoundError:
            raise HTTPException("El cliente no existe", status_code=404)

    @patch("/{client_id:int}", dto=ClientUpdateDTO)
    async def update_client(
        self, client_id: int, data: DTOData[Client], clients_repo: ClientRepository
    ) -> Client:
        try:
            client = clients_repo.get(client_id)
            client = data.update_instance(client)
            return clients_repo.update(client)
        except NotFoundError:
            raise HTTPException("El cliente no existe", status_code=404)


class LoanController(Controller):
    path = "/loans"
    tags = ["loans"]
    return_dto = LoanReadDTO
    dependencies = {
        "loans_repo": Provide(provide_loans_repo),
        "books_repo": Provide(provide_books_repo),
        "clients_repo": Provide(provide_clients_repo),
    }

    @get()
    async def list_loans(self, loans_repo: LoanRepository) -> list[Loan]:
        return loans_repo.list()

    @post(dto=LoanWriteDTO, return_dto=LoanReadFullDTO)
    async def create_loan(
        self,
        data: Loan,
        loans_repo: LoanRepository,
        books_repo: BookRepository,
        clients_repo: ClientRepository,
    ) -> Loan:
        data.date_loan = datetime.now().date() + timedelta(days=7)
        data.state = False
        data.fine = 0

        # verifica si existe el libro o el cliente
        try:
            book = books_repo.get(data.id_book)
        except NotFoundError:
            raise HTTPException("El libro no existe", status_code=404)

        try:
            client = clients_repo.get(data.client_id)
        except NotFoundError:
            raise HTTPException("El cliente no existe", status_code=404)

        # Verificar si hay copias disponibles para prestar
        if book.copies <= 0:
            raise HTTPException(
                "No hay copias disponibles para prestar", status_code=400
            )

        # Actualizar el número de copias del libro
        book.copies -= 1
        books_repo.update(book)

        # Crear el préstamo
        return loans_repo.add(data)

    @post("/{loan_id:int}", return_dto=LoanReadFullDTO)
    async def return_loan(
        self, loan_id: int, loans_repo: LoanRepository, books_repo: BookRepository
    ) -> Loan:
        try:
            loan = loans_repo.get(loan_id)
            book = books_repo.get(loan.id_book)
            if loan.state == True:
                raise HTTPException("El prestamo ya fue devuelto", status_code=404)
            if loan.date_loan < datetime.now().date():
                loan.fine = book.fine
            loan.state = True
            book.copies += 1
            books_repo.update(book)
            return loans_repo.update(loan)
        except NotFoundError:
            raise HTTPException("El prestamo no existe", status_code=404)
