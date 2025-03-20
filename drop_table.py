from app.database.database import Base
from sqlalchemy import create_engine
import importlib
import pkgutil
import os
import dotenv

dotenv.load_dotenv()


def import_all_models() -> None:
    """Import all models automatically."""
    # Import all models automatically
    models_pkg = importlib.import_module("app.models")
    for _, name, _ in pkgutil.iter_modules(models_pkg.__path__):
        importlib.import_module(f"app.models.{name}")


# Import all models automatically
import_all_models()

# Define your database URL

DATABASE_URL = (
    f"{os.getenv('DB_CONNECTION')}://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

# Create an engine
engine = create_engine(DATABASE_URL)

# Drop all tables - this will remove all tables and their data completely
Base.metadata.drop_all(engine)

print("All tables and their data have been completely removed.")  # noqa
