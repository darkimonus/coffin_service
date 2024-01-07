from fastapi import APIRouter, Header, HTTPException, Depends, FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse


from app.api.db_model import AsyncSessionLocal
from app.api.db_manager import *
from app.api.model import (MaterialType_, Material_, MaterialTypeCreate, MaterialCreate, CoffinCreate, CoffinShow,
                           CoffinMaterial)

from app.api import db_manager
from app.api import db_model
app = FastAPI()


async def get_db():
    async_db = AsyncSessionLocal()
    try:
        yield async_db
    finally:
        await async_db.close()



@app.get('/material_types', response_model=list[MaterialType_])
async def get_all_(db: AsyncSession = Depends(get_db)):
    return await db_manager.get_all_material_types(db)


@app.post('/material_types')
async def add(material_type: MaterialTypeCreate, db: AsyncSession = Depends(get_db)):
    db_per = db_model.Table()
    await db_manager.add_material_type(db, material_type)
    await db.commit()
    for instance in db:
        await db.refresh(instance)

    return {'message': "material type add"}


@app.get('/materials', response_model=list[Material_])
async def get_all_(db: AsyncSession = Depends(get_db)):
    return await db_manager.get_all_materials(db)


@app.post('/materials')
async def add(materials: MaterialCreate, db: AsyncSession = Depends(get_db)):
    db_per = db_model.Table()
    await db_manager.add_material(db, materials)
    await db.commit()
    for instance in db:
        await db.refresh(instance)

    return {'message': "material add"}




