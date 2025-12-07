from fastapi import FastAPI, HTTPException, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, Token
from app.security import hash_password, verify_password, create_access_token
from app.operations import add, subtract, multiply, divide
from app.logger_config import configure_logger
from app.users import router as users_router
from app.calculations import router as calculations_router
from app.db import Base, engine

logger = configure_logger()

app = FastAPI(
    title="FastAPI Calculator",
    version="0.2.0",
    description="Simple calculator API with secure user model for Module 10",
)

# Serve simple frontend pages for Module 13
app.mount("/static", StaticFiles(directory="static"), name="static")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI Calculator",
        version="0.2.0",
        description="Simple calculator API with secure user model for Module 10",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token from /api/users/login",
        }
    }
    # Mark calculation endpoints as requiring Bearer auth
    for path, path_item in openapi_schema["paths"].items():
        if "/api/calculations" in path:
            for method in path_item:
                if isinstance(path_item[method], dict):
                    if "security" not in path_item[method]:
                        path_item[method]["security"] = [{"Bearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.on_event("startup")
def on_startup():
    """
    Create database tables on application startup.
    This will be tested directly to get full coverage.
    """
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")


@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to the FastAPI Calculator!"}


@app.get("/add", summary="Add Route")
def add_route(a: float, b: float):
    result = add(a, b)
    logger.info(f"ADD {a} + {b} = {result}")
    return {"result": result}


@app.get("/subtract", summary="Subtract Route")
def subtract_route(a: float, b: float):
    result = subtract(a, b)
    logger.info(f"SUBTRACT {a} - {b} = {result}")
    return {"result": result}


@app.get("/multiply", summary="Multiply Route")
def multiply_route(a: float, b: float):
    result = multiply(a, b)
    logger.info(f"MULTIPLY {a} * {b} = {result}")
    return {"result": result}


@app.get("/divide", summary="Divide Route")
def divide_route(a: float, b: float):
    try:
        result = divide(a, b)
        logger.info(f"DIVIDE {a} / {b} = {result}")
        return {"result": result}
    except ValueError as exc:
        logger.error(f"DIVIDE error: {exc}")
        raise HTTPException(status_code=400, detail=str(exc))


# 🔐 Secure user endpoints
app.include_router(users_router, prefix="/api", tags=["users"])
app.include_router(calculations_router, prefix="/api", tags=["calculations"])


# Simple frontend endpoints
@app.get("/register", include_in_schema=False)
def register_page():
    return FileResponse("static/register.html")


@app.get("/login", include_in_schema=False)
def login_page():
    return FileResponse("static/login.html")


@app.get("/calculations", include_in_schema=False)
def calculations_page():
    return FileResponse("static/calculations.html")


# Expose API-compatible routes at top-level for simple frontend posting
@app.post("/register", response_model=UserCreate)
def register_api(payload: UserCreate, db: Session = Depends(get_db)):
    # Mirror logic from app/users.py create_user
    existing_username = db.query(User).filter(User.username == payload.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    existing_email = db.query(User).filter(User.email == payload.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return payload


@app.post("/login", response_model=Token)
def login_api(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token)
