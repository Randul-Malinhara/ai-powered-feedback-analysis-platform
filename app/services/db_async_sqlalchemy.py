import logging
from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from config.config import config
from models.feedback import Feedback, Base

logger = logging.getLogger(__name__)

async_engine = create_async_engine(config.AZURE_SQL_CONN_STR, echo=True)
async_session_maker = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

async def init_db() -> None:
    """
    Create all tables asynchronously.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Async DB tables created.")

async def save_feedback(feedback_data: Dict[str, Any]) -> int:
    """
    Save a feedback record asynchronously.
    """
    async with async_session_maker() as session:
        async with session.begin():
            feedback = Feedback(**feedback_data)
            session.add(feedback)
        await session.commit()
        logger.info(f"Feedback saved with id: {feedback.id}")
        return feedback.id

async def get_all_feedbacks() -> List[Feedback]:
    """
    Retrieve all feedback records, ordered by creation date descending.
    """
    async with async_session_maker() as session:
        result = await session.execute(select(Feedback).order_by(Feedback.created_at.desc()))
        feedbacks = result.scalars().all()
        logger.info(f"Retrieved {len(feedbacks)} feedback records.")
        return feedbacks

async def update_feedback(feedback_id: int, update_data: Dict[str, Any]) -> int:
    """
    Update a feedback record asynchronously.
    """
    async with async_session_maker() as session:
        async with session.begin():
            stmt = sqlalchemy_update(Feedback).where(Feedback.id == feedback_id).values(**update_data)
            result = await session.execute(stmt)
        await session.commit()
        rows_affected = result.rowcount or 0
        logger.info(f"Feedback with id {feedback_id} updated; rows affected: {rows_affected}")
        return rows_affected

async def delete_feedback(feedback_id: int) -> int:
    """
    Delete a feedback record asynchronously.
    """
    async with async_session_maker() as session:
        async with session.begin():
            stmt = sqlalchemy_delete(Feedback).where(Feedback.id == feedback_id)
            result = await session.execute(stmt)
        await session.commit()
        rows_affected = result.rowcount or 0
        logger.info(f"Feedback with id {feedback_id} deleted; rows affected: {rows_affected}")
        return rows_affected

async def run_in_transaction(statements: List[Any]) -> None:
    """
    Execute multiple statements in a single transaction.
    """
    async with async_session_maker() as session:
        async with session.begin():
            for stmt in statements:
                await session.execute(stmt)
        await session.commit()
    logger.info("Transaction executed successfully.")
