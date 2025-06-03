from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import *

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    search_items: Mapped[List["SearchQuery"]] = relationship(
        back_populates="name", cascade="all, delete-orphan"
    )


    def __repr__(self):
        return f"Category(id={self.id!r}, name={self.name!r}, search_items={self.search_items!r}"

class SearchQuery(Base):
    __tablename__ = "search_query"

    id: Mapped[int] = mapped_column(primary_key=True)
    # str may be wrong -- FIX
    name: Mapped[str] = mapped_column(Text())
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(back_populates="name")

    def __repr__(self):
        return f"SearchQuery(id={self.id!r}, name={self.name!r}, category_id={self.category_id!r}, category={self.category!r})"


class Response(Base):
    __tablename__ = "response"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_list: Mapped[List["Site"]] = relationship(
        back_populates="pagemap", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Response(id={self.id!r}, snippet={self.snippet!r}, pagemap={self.pagemap!r})"

class Site(Base):
    __tablename__ = "pagemap"

    id: Mapped[int] = mapped_column(primary_key=True)
    snippet: Mapped[str] = mapped_column(Text())
    rank: Mapped[int] = mapped_column(int)
    ## Everything below this comment is derived from pagemap data - including the optional and TBD
    formattedUrl: Mapped[str] = mapped_column(String(200))
    title: Mapped[str] = mapped_column(String(200))

    # maybe add -- FIX
    # webpage: Mapped[Optional[List[str]]]
    # derived from meta-tags
    # a small number of items do not have metatags
    og_description: Mapped[Optional[str]] = mapped_column(Text())
    og_title: Mapped[Optional[str]] = mapped_column(Text())
    def __repr__(self):
        return f"Pagemap(id={self.id!r}, snippet={self.snippet!r}, pagemap={self.pagemap!r})"
