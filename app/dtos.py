from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import Author, Book, Category, Client, Loan


class AuthorReadDTO(SQLAlchemyDTO[Author]):
    config = SQLAlchemyDTOConfig(exclude={"books"})


class AuthorReadFullDTO(SQLAlchemyDTO[Author]):
    pass


class AuthorWriteDTO(SQLAlchemyDTO[Author]):
    config = SQLAlchemyDTOConfig(exclude={"id", "books"})


class AuthorUpdateDTO(SQLAlchemyDTO[Author]):
    config = SQLAlchemyDTOConfig(exclude={"id", "books"}, partial=True)


















class ClientReadDTO(SQLAlchemyDTO[Client]):
    pass


class ClientReadFullDTO(SQLAlchemyDTO[Client]):
    pass


class ClientWriteDTO(SQLAlchemyDTO[Client]):
    config = SQLAlchemyDTOConfig(exclude={"id", "loans"})


class ClientUpdateDTO(SQLAlchemyDTO[Client]):
    config = SQLAlchemyDTOConfig(exclude={"id", "loans"}, partial=True)

















class BookReadDTO(SQLAlchemyDTO[Book]):
    pass


class BookGetDTO(SQLAlchemyDTO[Book]):
    config = SQLAlchemyDTOConfig(
        exclude={
            "id",
            "author_id",
            "author.id",
            "author.biography",
            "author.date_of_birth",
            "categories",
        }
    )


class BookUpdateDTO(SQLAlchemyDTO[Book]):
    config = SQLAlchemyDTOConfig(exclude={"id", "author_id", "author", "categories"})


class BookWriteDTO(SQLAlchemyDTO[Book]):
    config = SQLAlchemyDTOConfig(exclude={"id", "author"})













class CategoryReadDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"books"})


class CategoryReadFullDTO(SQLAlchemyDTO[Category]):
    pass


class CategoryWriteDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"id", "books"})


class CategoryUpdateDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"id", "books"}, partial=True)













class LoanReadFullDTO(SQLAlchemyDTO[Loan]):
    pass


class LoanWriteDTO(SQLAlchemyDTO[Loan]):
    config = SQLAlchemyDTOConfig(exclude={"id", "date_loan", "fine", "state", "client"})


class LoanUpdateDTO(SQLAlchemyDTO[Loan]):
    config = SQLAlchemyDTOConfig(exclude={"id", "id_book", "date_loan", "client_id"})