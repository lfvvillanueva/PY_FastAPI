from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import Session, create_engine, SQLModel
from pathlib import Path

# 1) Raíz del proyecto = un nivel ARRIBA de este archivo (DB/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 2) Asegura carpeta DB y arma la ruta absoluta del archivo
DB_PATH = PROJECT_ROOT / "DB" / "database.sqlite3"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# 3) URL de conexión (absoluta)
sqlite_url = f"sqlite:///{DB_PATH}"

engine = create_engine(sqlite_url)

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]