from typing import List,Optional
from sqlalchemy import ForeignKey,String,Text,Integer
from sqlalchemy.orm import DeclarativeBase,Mapped,relationship,mapped_column



class BaseModel(DeclarativeBase):
    pass

#FIX double check spelling
class Category(BaseModel):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    search_items: Mapped[List["SearchQuery"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r}"

class SearchQuery(BaseModel):
    __tablename__ = "search_query"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(back_populates="search_items")
    site_list: Mapped[List["Site"]] = relationship(
        back_populates="search_query", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"SearchQueryModel(id={self.id!r}, name={self.name!r}, category_id={self.category_id!r})"


class Site(BaseModel):
    __tablename__ = "site"

    id: Mapped[int] = mapped_column(primary_key=True)
    snippet: Mapped[str] = mapped_column(Text())
    rank: Mapped[int] = mapped_column(Integer)
    search_query_id: Mapped[int] = mapped_column(ForeignKey("search_query.id"))
    search_query: Mapped["SearchQuery"] = relationship(back_populates="site_list")

    ## Everything below this comment is derived from pagemap data - including the optional and TBD
    formatted_url: Mapped[str] = mapped_column(String(200))
    title: Mapped[str] = mapped_column(String(200))

    # a small number of items do not have one or more of these
    description: Mapped[Optional[str]] = mapped_column(Text())
    alt_title: Mapped[Optional[str]] = mapped_column(Text())


    def __repr__(self) -> str:
        return f"SiteModel(id={self.id!r},snippet={self.snippet!r}, rank={self.rank!r},formatted_url={self.formatted_url!r}, title={self.title!r},search_query_id={self.search_query_id!r},description={self.description!r},alt_title={self.alt_title!r})"
