from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    isbn: Mapped[str] = mapped_column(index=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str]
    year: Mapped[int]
    language: Mapped[str]
    copies: Mapped[int]
    fine: Mapped[int]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    # relationships
    author: "Mapped[Author]" = relationship(back_populates="books")
    categories: "Mapped[list[Category]]" = relationship(
        back_populates="books", secondary="books_categories"
    )


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    biography: Mapped[Optional[str]]
    date_of_birth: Mapped[Optional[date]]

    # relationships
    books: "Mapped[list[Book]]" = relationship(back_populates="author")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    # relationships
    books: "Mapped[list[Book]]" = relationship(
        back_populates="categories", secondary="books_categories"
    )


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    # relationships
    loans: "Mapped[list[Loan]]" = relationship(back_populates="client")


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_book: Mapped[int]
    date_loan: Mapped[date]
    fine: Mapped[int]
    state: Mapped[bool]
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))

    # relationships
    client: "Mapped[Client]" = relationship(back_populates="loans")


class BookCategory(Base):
    __tablename__ = "books_categories"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), primary_key=True
    )
