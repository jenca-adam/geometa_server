from sqlalchemy import Column, JSON, String, Integer, ForeignKey, Table, create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
class Base(DeclarativeBase):
    pass

meta_tag_association = Table(
    "meta_tag_association",
    Base.metadata,
    Column("meta_id", ForeignKey("meta.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tag"
    id:Mapped[int] = mapped_column(primary_key = True)
    name:Mapped[str] = mapped_column(String(128)) 
    parent_id: Mapped[int] = mapped_column(ForeignKey("tag.id"), nullable=True)
    children: Mapped[list["Tag"]] = relationship(back_populates = "parent",  cascade="all")
    parent: Mapped["Tag"] = relationship(remote_side=[id], back_populates = "children")
    metas: Mapped[list["Meta"]] = relationship(secondary = meta_tag_association, back_populates="tags")

class Meta(Base):
    __tablename__ = "meta"
    id:Mapped[int] = mapped_column(primary_key = True)
    meta_data:Mapped[dict] = mapped_column(JSON) # Make the metadata format flexible, so that changing it doesn't require redoing the entire database.
    gt_user_uid:Mapped[str] = mapped_column(String(10))
    tags:Mapped[list["Tag"]] = relationship(secondary = meta_tag_association, back_populates="metas")
    drops: Mapped[list["Drop"]] = relationship(back_populates="meta")
    
class Drop(Base):
    __tablename__ = "drop"
    id:Mapped[int] = mapped_column(primary_key = True)
    drop_data:Mapped[dict] = mapped_column(JSON)
    meta_id:Mapped[int] = mapped_column(ForeignKey("meta.id"))
    meta:Mapped["Meta"] = relationship(back_populates = "drops")
    def to_json(self):
        return {"drop":self.drop_data, "dropInfo":self.meta_data, "tags":[tag.name for tag in self.tags]}

engine = create_engine("sqlite:///db.sqlite")
Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()

def pick_random_drop():
    return session.query(Drop).order_by(func.random()).first()

def create_drop(drop_data, meta):
    drop = Drop(drop_data= drop_data, meta=meta)
    session.add(drop)
    session.commit()
    return drop
def create_meta(meta_data, gt_user_uid, tags):
    meta = Meta(meta_data = meta_data, gt_user_uid=gt_user_uid, tags=tags)
    session.add(meta)
    session.commit()
    return meta
def create_tag(name, parent=None):
    tag = Tag(name=name, parent=parent)
    session.add(tag)
    session.commit()
    return tag
def get_tag(name):
    return session.query(Tag).filter(Tag.name==name).first()

