# tests/integration/test_calculation_db.py
from app.models import User, Calculation, CalculationType
from app.schemas import CalculationCreate
from app.security import hash_password
from app.calculation_factory import CalculationFactory


def test_calculation_persists_to_db(db_session):
    """
    Insert a calculation record and confirm the DB stores correct data.
    """
    calc_in = CalculationCreate(a=3.0, b=4.0, type=CalculationType.MULTIPLY)
    op = CalculationFactory.get_operation(calc_in.type)
    result = op.compute(calc_in.a, calc_in.b)

    calc = Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type,
        result=result,
        user_id=None,
    )
    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)

    assert calc.id is not None
    assert calc.result == 12.0

    fetched = db_session.query(Calculation).filter_by(id=calc.id).first()
    assert fetched is not None
    assert fetched.a == 3.0
    assert fetched.b == 4.0
    assert fetched.type == CalculationType.MULTIPLY
    assert fetched.result == 12.0


def test_calculation_with_user_fk(db_session):
    """
    Ensure Calculation.user_id FK works and relationship links to User.
    """
    user = User(
        username="calc-user",
        email="calc-user@example.com",
        password_hash=hash_password("secret123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    calc_in = CalculationCreate(a=10.0, b=2.0, type=CalculationType.DIVIDE)
    op = CalculationFactory.get_operation(calc_in.type)
    result = op.compute(calc_in.a, calc_in.b)

    calc = Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type,
        result=result,
        user_id=user.id,
    )
    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)

    assert calc.user_id == user.id
    # relationship should be available
    assert calc.user.username == "calc-user"
