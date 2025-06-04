from typing import List,Optional
from sqlalchemy import ForeignKey,String,Text,Integer
from sqlalchemy.orm import DeclarativeBase,Mapped,relationship,mapped_column



class BaseModel(DeclarativeBase):
    pass

#FIX double check spelling
class CategoryModel(BaseModel):
    # def __init__(self,id: int=None,name: String=None):
    #     self.name=name
    #     super().__init__(id=id)

    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    search_items: Mapped[List["SearchQueryModel"]] = relationship(
        back_populates="name", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r}, search_items={self.search_items!r}"

class SearchQueryModel(BaseModel):
    __tablename__ = "search_query"

    id: Mapped[int] = mapped_column(primary_key=True)
    # str may be wrong -- FIX
    name: Mapped[str] = mapped_column(Text())
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["CategoryModel"] = relationship(back_populates="name")

    def __repr__(self) -> str:
        return f"SearchQueryModel(id={self.id!r}, name={self.name!r}, category_id={self.category_id!r}, category={self.category!r})"


class ResponseModel(BaseModel):
    __tablename__ = "response"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_list: Mapped[List["SiteModel"]] = relationship(
        back_populates="site", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"ResponseModel(id={self.id!r}, site_list={self.site_list!r})"

class SiteModel(BaseModel):
    __tablename__ = "site"

    id: Mapped[int] = mapped_column(primary_key=True)
    snippet: Mapped[str] = mapped_column(Text())
    rank: Mapped[int] = mapped_column(Integer)
    response_id: Mapped[int] = mapped_column(ForeignKey("response.id"))
    site: Mapped["ResponseModel"] = relationship(back_populates="site_list")

    ## Everything below this comment is derived from pagemap data - including the optional and TBD
    formatted_url: Mapped[str] = mapped_column(String(200))
    title: Mapped[str] = mapped_column(String(200))


    # maybe add -- FIX
    # webpage: Mapped[Optional[List[str]]]
    # derived from meta-tags
    # a small number of items do not have metatags
    og_description: Mapped[Optional[str]] = mapped_column(Text())
    og_title: Mapped[Optional[str]] = mapped_column(Text())


    def __repr__(self) -> str:
        return f"SiteModel(id={self.id!r},snippet={self.snippet!r}, rank={self.rank!r},formatted_url={self.formatted_url!r}, title={self.title!r}, og_description={self.og_description!r},og_title={self.og_title!r})"
