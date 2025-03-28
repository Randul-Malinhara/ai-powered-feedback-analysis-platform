# app/services/db_async.py
import asyncio
import logging
import sqlalchemy
import databases
from typing import Any, Dict, List, Callable, Awaitable, TypeVar
from config import AZURE_SQL_CONN_STR
from app.models.feedback import metadata, Feedback

# Set up type variable for the retry decorator
T = TypeVar("T")

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Set up the asynchronous database and engine
database = databases.Database(AZURE_SQL_CONN_STR)
engine = sqlalchemy.create_engine(AZURE_SQL_CONN_STR)
metadata.create_all(engine)

def async_retry(retries: int = 3, delay: float = 1.0) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]:
    """
    A decorator to retry an async function if it raises an exception.
    """
    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        async def wrapper(*args, **kwargs) -> T:
            attempt = 0
            while attempt < retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    logger.error(f"Error in {func.__name__}, attempt {attempt}/{retries}: {e}")
                    if attempt < retries:
                        await asyncio.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator

async def connect_db() -> None:
    """Ensure the database connection is established."""
    if not database.is_connected:
        await database.connect()
        logger.info("Database connected.")

async def disconnect_db() -> None:
    """Disconnect the database if connected."""
    if database.is_connected:
        await database.disconnect()
        logger.info("Database disconnected.")

@async_retry(retries=3, delay=1.0)
async def save_feedback_async(feedback: Dict[str, Any]) -> int:
    """
    Save a feedback record asynchronously.
    Returns the inserted record's ID.
    """
    query = Feedback.__table__.insert().values(**feedback)
    try:
        record_id = await database.execute(query)
        logger.info(f"Feedback saved with id: {record_id}")
        return record_id
    except Exception as e:
        logger.error(f"Error saving feedback: {e}")
        raise

@async_retry(retries=3, delay=1.0)
async def get_all_feedbacks_async() -> List[Dict[str, Any]]:
    """
    Retrieve all feedback records asynchronously, ordered by creation date descending.
    Returns a list of records.
    """
    query = Feedback.__table__.select().order_by(Feedback.created_at.desc())
    try:
        results = await database.fetch_all(query)
        logger.info(f"Retrieved {len(results)} feedback records.")
        return results
    except Exception as e:
        logger.error(f"Error retrieving feedback records: {e}")
        raise

@async_retry(retries=3, delay=1.0)
async def update_feedback_async(feedback_id: int, update_data: Dict[str, Any]) -> int:
    """
    Update a feedback record asynchronously.
    Returns the number of rows affected.
    """
    query = Feedback.__table__.update().where(Feedback.id == feedback_id).values(**update_data)
    try:
        rows_affected = await database.execute(query)
        logger.info(f"Feedback with id {feedback_id} updated; rows affected: {rows_affected}")
        return rows_affected
    except Exception as e:
        logger.error(f"Error updating feedback with id {feedback_id}: {e}")
        raise

@async_retry(retries=3, delay=1.0)
async def delete_feedback_async(feedback_id: int) -> int:
    """
    Delete a feedback record asynchronously.
    Returns the number of rows affected.
    """
    query = Feedback.__table__.delete().where(Feedback.id == feedback_id)
    try:
        rows_affected = await database.execute(query)
        logger.info(f"Feedback with id {feedback_id} deleted; rows affected: {rows_affected}")
        return rows_affected
    except Exception as e:
        logger.error(f"Error deleting feedback with id {feedback_id}: {e}")
        raise

async def run_in_transaction(queries: List[sqlalchemy.sql.expression.ClauseElement]) -> None:
    """
    Execute multiple queries within a single transaction.
    All queries must succeed; otherwise, the transaction is rolled back.
    """
    async with database.transaction():
        for query in queries:
            await database.execute(query)
        logger.info("Transaction executed successfully.")
