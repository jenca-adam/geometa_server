from sqlalchemy import Column, JSON, String, Integer, ForeignKey, Table, create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, scoped_session
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
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    parent_id: Mapped[int] = mapped_column(ForeignKey("tag.id"), nullable=True)
    children: Mapped[list["Tag"]] = relationship(back_populates="parent", cascade="all")
    parent: Mapped["Tag"] = relationship(remote_side=[id], back_populates="children")
    metas: Mapped[list["Meta"]] = relationship(
        secondary=meta_tag_association, back_populates="tags"
    )

    def get_name(self):
        names = []
        tag = self
        while tag:
            names.append(tag.name)
            tag = tag.parent
        return " > ".join(reversed(names))

    def to_json(self):
        return {
            "id": self.name,
            "name": self.get_name(),
            "parent": self.parent.to_json() if self.parent else None,
        }


class Meta(Base):
    __tablename__ = "meta"
    id: Mapped[int] = mapped_column(primary_key=True)
    meta_data: Mapped[dict] = mapped_column(
        JSON
    )  # Make the metadata format flexible, so that changing it doesn't require redoing the entire database.
    gt_user_uid: Mapped[str] = mapped_column(String(16))
    tags: Mapped[list["Tag"]] = relationship(
        secondary=meta_tag_association, back_populates="metas"
    )
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    country: Mapped["Country"] = relationship(back_populates="metas")
    drops: Mapped[list["Drop"]] = relationship(back_populates="meta")

    def to_mma(self):
        return f"{self.id} {self.meta_data.get('title', '?')}"

    def to_json(self):
        return {
            **self.meta_data,
            "tags": [tag.to_json() for tag in self.tags],
            "country": self.country.to_json() if self.country else None,
        }


class Drop(Base):
    __tablename__ = "drop"
    id: Mapped[int] = mapped_column(primary_key=True)
    drop_data: Mapped[dict] = mapped_column(JSON)
    meta_id: Mapped[int] = mapped_column(ForeignKey("meta.id"))
    meta: Mapped["Meta"] = relationship(back_populates="drops")

    def to_json(self):
        return {"drop": self.drop_data, "dropInfo": self.meta.to_json()}

    def to_mma(self):
        return {
            "lat": self.drop_data.get("lat", 0),
            "lng": self.drop_data.get("lng", 0),
            "heading": self.drop_data.get("heading", 0),
            "pitch": self.drop_data.get("pitch", 0),
            "zoom": self.drop_data.get("zoom", 0),
            "panoId": self.drop_data.get("panoId"),
            "countryCode": self.drop_data.get("code", self.meta.country.iso2),
            "stateCode": self.drop_data.get("subCode"),
            "extra": {
                "panoId": self.drop_data.get("panoId"),
                "tags": [self.meta.to_mma()],
            },
        }


class Country(Base):
    __tablename__ = "country"
    id: Mapped[int] = mapped_column(primary_key=True)
    iso2: Mapped[str] = mapped_column(String(2))
    name: Mapped[str] = mapped_column(String(32))
    metas: Mapped[list["Meta"]] = relationship(back_populates="country")

    def to_json(self):
        return {"iso2": self.iso2, "name": self.name}


engine = create_engine("sqlite:///db/db.sqlite")
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()


def pick_random_drop():
    return session.query(Drop).order_by(func.random()).first()


def create_drop(drop_data, meta):
    drop = Drop(drop_data=drop_data, meta=meta)
    session.add(drop)
    session.commit()
    return drop


def create_meta(meta_data, gt_user_uid, tags, country):
    meta = Meta(
        meta_data=meta_data, gt_user_uid=gt_user_uid, tags=tags, country=country
    )
    session.add(meta)
    session.commit()
    return meta


def create_tag(name, parent=None):
    tag = Tag(name=name, parent=parent)
    session.add(tag)
    session.commit()
    return tag


def create_country(iso2, name):
    country = Country(iso2=iso2, name=name)
    session.add(country)
    session.commit()
    return country


def get_tag(name):
    return session.query(Tag).filter(Tag.name == name).first()
