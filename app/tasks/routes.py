from fastapi import APIRouter, Depends
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.auth.routes import current_user
from app.db.session import get_async_session
from app.models.task import Task
from app.models.user import User
from fastapi import HTTPException, Body
from app.models.task_answer import TaskAnswer

router = APIRouter()

# TODO: Add response model
@router.get("/me")
async def get_my_tasks(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    result = await session.execute(
        select(Task)
        .options(joinedload(Task.options))
        .where(
            or_(
                Task.is_global is True,
                Task.assigned_user_id == user.id
            )
        )
    )
    return result.unique().scalars().all()

@router.post("/answer")
async def submit_answer(
    body: dict = Body(...),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):

    try:
        task_id = body["task_id"]
    except (KeyError, ValueError):
        raise HTTPException(status_code=422, detail="Некорректный или отсутствующий task_id")

    selected_option_ids = body.get("selected_option_ids")
    text_answer = body.get("text_answer")

    if not selected_option_ids and not text_answer:
        raise HTTPException(status_code=400, detail="Нужно выбрать хотя бы один вариант или ввести текст")

    answer = TaskAnswer(
        user_id=user.id,
        task_id=int(task_id),
        selected_option_ids=selected_option_ids,
        text_answer=text_answer
    )

    session.add(answer)
    await session.commit()
    await session.refresh(answer)
    return {
        "id": answer.id,
        "task_id": str(answer.task_id),
        "user_id": str(answer.user_id),
        "selected_option_ids": selected_option_ids,
        "text_answer": text_answer
    }
