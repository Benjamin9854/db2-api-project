from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import Author, Book


class AuthorReadDTO(SQLAlchemyDTO[Author]):
    config = SQLAlchemyDTOConfig(exclude={"books"})


class AuthorReadFullDTO(SQLAlchemyDTO[Author]):
    pass


class AuthorWriteDTO(SQLAlchemyDTO[Author]):
    config = SQLAlchemyDTOConfig(exclude={"id", "books"})


class AuthorUpdateDTO(SQLAlchemyDTO[Author]):
    config = SQLAlchemyDTOConfig(exclude={"id", "books"}, partial=True)




class BookReadDTO(SQLAlchemyDTO[Book]):
    pass

class BookGetDTO(SQLAlchemyDTO[Book]):
    config = SQLAlchemyDTOConfig(exclude={"id", "author_id", "author.id", "author.biography", "author.date_of_birth"})

class BookUpdateDTO(SQLAlchemyDTO[Book]):
    config = SQLAlchemyDTOConfig(exclude={"id", "author_id", "author", "categories"})


class BookWriteDTO(SQLAlchemyDTO[Book]):
    config = SQLAlchemyDTOConfig(exclude={"id", "author"})
