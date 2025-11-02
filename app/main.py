from fastapi import FastAPI, HTTPException
from app.operations import add, subtract, multiply, divide
from app.logger_config import configure_logger

logger = configure_logger()

app = FastAPI(
    title="FastAPI Calculator",
    version="0.1.0",
    description="Simple calculator API built for Module 8",
)


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
