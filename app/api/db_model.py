from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY, ForeignKey, DateTime, TIMESTAMP, PrimaryKeyConstraint)


from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
import asyncio

DATABASE_URL = "postgresql+asyncpg://myadmin:aboba@localhost:5432/coffins_db"
engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


class Material(Base):
    __tablename__ = "materials"
    id_material = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    id_type = Column(Integer, ForeignKey("material_types.id_type"))
    material_type = relationship("MaterialType", secondary="coffin_materials", back_populates="materials")


class MaterialType(Base):
    __tablename__ = "material_types"
    id_type = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    materials = relationship("Material", back_populates="material_types")


class Coffin(Base):
    __tablename__ = "coffins"
    id_coffin = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    length = Column(Integer)
    width = Column(Integer)
    quantity = Column(Integer)
    materials = relationship("Material", secondary="coffin_materials")


class CoffinMaterial(Base):
    __tablename__ = "coffin_materials"
    id_coffin = Column(Integer, ForeignKey("coffins.id_coffin"), primary_key=True)
    id_material = Column(Integer, ForeignKey("materials.id_material"), primary_key=True)
    coffin = relationship("Coffin", back_populates="coffin_materials")
    material = relationship("Material", back_populates="coffin_materials")
    PrimaryKeyConstraint("id_coffin", "id_material", name="pk_coffin_materials")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
# Викликати цю функцію для асинхронного створення таблиць


asyncio.run(create_tables())


database = Database(DATABASE_URL)
