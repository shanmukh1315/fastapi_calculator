# Alembic Migration Guide

## Overview

This project uses Alembic for database schema migrations. This guide provides step-by-step instructions for common migration scenarios.

## Quick Reference

| Command                                        | Description                                            |
| ---------------------------------------------- | ------------------------------------------------------ |
| `alembic current`                              | Show current migration revision                        |
| `alembic history`                              | List all migrations                                    |
| `alembic upgrade head`                         | Apply all pending migrations                           |
| `alembic downgrade -1`                         | Rollback last migration                                |
| `alembic revision --autogenerate -m "message"` | Create new migration from model changes                |
| `alembic stamp head`                           | Mark database as up-to-date without running migrations |

## Common Scenarios

### Scenario 1: Fresh Database Setup

Starting with a brand new database:

```bash
# 1. Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Apply all migrations
alembic upgrade head

# 3. Verify migration status
alembic current
# Output: b01b1ad235d4 (head)

# 4. Start the application
uvicorn app.main:app --reload
```

### Scenario 2: Existing Database (Already Has Tables)

If you have an existing database with tables already created:

```bash
# Mark the database as being at the latest migration
alembic stamp head

# Verify
alembic current
```

### Scenario 3: Adding a New Model Field

Let's say you want to add a `phone_number` field to the User model:

1. **Modify the model** in `app/models.py`:

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    phone_number = Column(String(20), nullable=True)  # NEW FIELD
```

2. **Generate migration**:

```bash
alembic revision --autogenerate -m "Add phone_number to users"
```

3. **Review the generated migration** in `alembic/versions/`:

```python
def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone_number', sa.String(length=20), nullable=True))

def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('phone_number')
```

4. **Apply the migration**:

```bash
alembic upgrade head
```

### Scenario 4: Adding a New Enum Value

To add a new calculation type (e.g., `SQUARE_ROOT`):

1. **Update the enum** in `app/models.py`:

```python
class CalculationType(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    POWER = "power"
    MODULUS = "modulus"
    PERCENT_OF = "percent_of"
    NTH_ROOT = "nth_root"
    LOG_BASE = "log_base"
    SQUARE_ROOT = "square_root"  # NEW
```

2. **Create migration**:

```bash
alembic revision -m "Add SQUARE_ROOT calculation type"
```

3. **Manually edit the migration** (SQLite doesn't support enum changes via ALTER):

```python
def upgrade():
    # For SQLite, enum is stored as VARCHAR, so no schema change needed
    # The application code will handle the new enum value
    pass

def downgrade():
    pass
```

4. **Apply migration**:

```bash
alembic upgrade head
```

### Scenario 5: Rollback Changes

If you need to undo the last migration:

```bash
# Check current revision
alembic current

# View history
alembic history

# Rollback one migration
alembic downgrade -1

# Or rollback to a specific revision
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

### Scenario 6: Production Deployment

For deploying to production:

```bash
# 1. Backup your database first!
cp app.db app.db.backup

# 2. Pull latest code
git pull origin main

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Install/update dependencies
pip install -r requirements.txt

# 5. Apply migrations
alembic upgrade head

# 6. Restart the application
# (depends on your deployment method - systemd, docker, etc.)
```

## Best Practices

1. **Always Review Auto-Generated Migrations**

   - `--autogenerate` is helpful but not perfect
   - Always review and test migrations before applying

2. **Test Migrations Both Ways**

   ```bash
   alembic upgrade head    # Test upgrade
   alembic downgrade -1    # Test downgrade
   alembic upgrade head    # Upgrade again
   ```

3. **Never Edit Applied Migrations**

   - Once a migration is applied, don't modify it
   - Create a new migration to fix issues

4. **Commit Migrations to Git**

   ```bash
   git add alembic/versions/*.py
   git commit -m "Add migration for <feature>"
   ```

5. **Backup Before Production Migrations**
   - Always backup production databases before running migrations
   - Test migrations on staging environment first

## Troubleshooting

### Problem: "Target database is not up to date"

```bash
# Check current revision
alembic current

# View pending migrations
alembic history

# Apply pending migrations
alembic upgrade head
```

### Problem: "Can't locate revision identified by..."

This usually means the database thinks it's at a revision that doesn't exist.

```bash
# Reset to base and re-apply
alembic downgrade base
alembic upgrade head

# Or stamp to current head if schema is already correct
alembic stamp head
```

### Problem: SQLite ALTER TABLE errors

SQLite has limited ALTER TABLE support. Ensure `render_as_batch=True` is set in `alembic/env.py`:

```python
context.configure(
    connection=connection,
    target_metadata=target_metadata,
    render_as_batch=True  # Important for SQLite!
)
```

## Migration File Structure

```
alembic/
├── versions/
│   └── b01b1ad235d4_initial_schema.py
├── env.py           # Migration environment config
├── script.py.mako   # Template for new migrations
└── README           # Auto-generated Alembic README

alembic.ini          # Alembic configuration file
```

## Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
