from sqlalchemy import Column, JSON, String, Integer, ForeignKey, Table, create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
class Base(DeclarativeBase):
    pass

drop_tag_association = Table(
    "drop_tag_association",
    Base.metadata,
    Column("drop_id", ForeignKey("drop.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tag"
    id:Mapped[int] = mapped_column(primary_key = True)
    name:Mapped[str] = mapped_column(String(128)) 

class Drop(Base):
    __tablename__ = "drop"
    id:Mapped[int] = mapped_column(primary_key = True)
    drop_data:Mapped[dict] = mapped_column(JSON)
    meta_data:Mapped[dict] = mapped_column(JSON) # Make the metadata format flexible, so that changing it doesn't require redoing the entire database.
    gt_user_uid:Mapped[str] = mapped_column(String(10))
    tags:Mapped[list["Tag"]] = relationship(secondary = drop_tag_association)
    
    def to_json(self):
        return {"drop":self.drop_data, "dropInfo":self.meta_data, "tags":[tag.name for tag in self.tags]}

engine = create_engine("sqlite:///db.sqlite")
Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()

def pick_random_drop():
    return session.query(Drop).order_by(func.random()).first()

def create_drop(drop_data, meta_data, gt_user_uid, tags):
    drop = Drop(drop_data= drop_data, meta_data = meta_data, gt_user_uid=gt_user_uid, tags=tags)
    session.add(drop)
    session.commit()

def create_tag(name):
    tag = Tag(name=name)
    session.add(tag)
    session.commit()

