from pydantic import BaseModel

# Pydantic-моделі
class MaterialTypeBase(BaseModel):
    name: str


class MaterialTypeCreate(MaterialTypeBase):
    name: str


class MaterialType_(MaterialTypeBase):
    id_type: int

    class Config:
        orm_mode = True


class MaterialBase(BaseModel):
    name: str
    id_type: int


class Material_(MaterialBase):
    id_material: int

    class Config:
        orm_mode = True


class MaterialCreate(MaterialBase):
    name: str
    id_type: int


class CoffinBase(BaseModel):
    name: str
    price: int  # Змінено на int відповідно до вашого коду SQLAlchemy
    length: int
    width: int
    quantity: int


class CoffinCreate(CoffinBase):
    name: str
    price: int
    length: int
    width: int
    quantity: int


class CoffinShow(CoffinBase):
    id_coffin: int

    class Config:
        orm_mode = True


class CoffinMaterialBase(BaseModel):
    id_coffin: int
    id_material: int


class CoffinMaterial(CoffinMaterialBase):
    pass

    class Config:
        orm_mode = True

