from fastapi import APIRouter, Depends
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.auth.routes import current_user
from app.db.session import get_async_session
from app.models.task import Task, TaskType
from app.models.user import User
from fastapi import HTTPException, Body
from app.models.task_answer import TaskAnswer
from typing import List

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
                Task.is_global == True,
                Task.assigned_user_id == user.id
            )
        )
    )
    return result.unique().scalars().all()

@router.post("/answers")
async def submit_answers(
    body: List[dict] | dict = Body(...),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    created = []
    if isinstance(body, dict):
        body = [body]
    for answer in body:
        try:
            task_id = int(answer["task_id"])
        except (KeyError, ValueError):
            raise HTTPException(status_code=422, detail="Некорректный или отсутствующий task_id")

        selected_option_ids = answer.get("selected_option_ids")
        text_answer = answer.get("text_answer")
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()

        # TODO: Refactor exception handling
        if not selected_option_ids and not text_answer:
            raise HTTPException(status_code=400, detail="Нужно выбрать хотя бы один вариант или ввести текст")

        if task.task_type == TaskType.text:
            if selected_option_ids:
                raise HTTPException(status_code=400, detail="Нельзя выбрать варианты для текстового задания")
            if not text_answer:
                raise HTTPException(status_code=400, detail="Нужен текстовый ответ")
        if task.task_type == TaskType.single_choice:
            if not selected_option_ids:
                raise HTTPException(status_code=400, detail="Нужно выбрать вариант ответа")
            if len(selected_option_ids) > 1 or text_answer:
                raise HTTPException(status_code=400, detail="Нужно выбрать один вариант ответа")
        if task.task_type == TaskType.multiple_choice:
            if text_answer:
                raise HTTPException(status_code=400, detail="Нельзя писать текстовый ответ для этого задания")
            if not selected_option_ids:
                raise HTTPException(status_code=400, detail="Нужно выбрать хотя бы один вариант ответа")


        answer = TaskAnswer(
            user_id=user.id,
            task_id=task_id,
            selected_option_ids=selected_option_ids,
            text_answer=text_answer
        )

        session.add(answer)
        created.append(answer)

    await session.commit()
    for obj in created:
        await session.refresh(obj)

    return created
