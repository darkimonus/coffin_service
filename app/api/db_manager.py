from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from app.api.db_model import Material, MaterialType, CoffinMaterial, Coffin
from app.api.model import *


async def get_all_material_types(db: AsyncSession):
    return (await db.execute(select(MaterialType))).all()


async def add_material_type(db: AsyncSession, material_type: MaterialTypeCreate, ):
    query = insert(MaterialType).values(name=material_type.name)
    return await db.execute(query)


async def add_material(db: AsyncSession, material: MaterialCreate, ):
    query = insert(Material).values(name=material.name, id_type=material.id_type)
    return await db.execute(query)


async def get_all_materials(db: AsyncSession):
    return (await db.execute(select(Material))).all()


async def add_coffin(db: AsyncSession, coffin_data: CoffinCreate):
    # Спочатку додаємо Coffin без матеріалів
    query = insert(Coffin).values(
        name=coffin_data.name,
        price=coffin_data.price,
        length=coffin_data.length,
        width=coffin_data.width,
        quantity=coffin_data.quantity
    )
    result = await db.execute(query)
    new_coffin = result.fetchone()

    # Потім додаємо матеріали до CoffinMaterial
    for material_id in coffin_data.materials:
        query = insert(CoffinMaterial).values(id_coffin=new_coffin.id_coffin, id_material=material_id)
        await db.execute(query)

    return new_coffin


async def get_coffin(db: AsyncSession, coffin_id: int):
    # Використовуємо SQLAlchemy для об'єднання таблиць та вибірки даних
    stmt = (
        select(Coffin)
        .filter(Coffin.id_coffin == coffin_id)
        .options(select(Material).join(Coffin.materials).load_only("name"))
    )

    result = await db.execute(stmt)
    coffin_with_materials = result.scalar()

    return coffin_with_materials
