from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi_users.password import PasswordHelper

from app.models.user import User
from app.models.task_option import TaskOption
from app.db.database import engine
from app.config import SECRET_KEY
from app.auth.manager import get_user_manager
from wtforms import SelectField


from wtforms import Form, StringField, SelectMultipleField
from wtforms.validators import DataRequired
from sqlalchemy import select
from app.models.task import Task, TaskType
from app.db.database import async_session_maker



templates = Jinja2Templates(directory="app/templates")


class AdminAuth(AuthenticationBackend):
    def __init__(self):
        super().__init__(secret_key=SECRET_KEY)

    async def authenticate(self, request: Request) -> bool:
        user_id = request.session.get("user")
        if not user_id:
            return False
        try:
            manager = await anext(get_user_manager())
            user = await manager.get(user_id)
            return user.is_admin
        except Exception:
            return False

    async def login(self, request: Request) -> HTMLResponse:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        manager = await anext(get_user_manager())
        user = await manager.get_by_email(email)
        password_helper = PasswordHelper()
        verified = password_helper.verify_and_update(password, user.hashed_password)
        if not verified or not user.is_admin:
            raise Exception("Invalid credentials or not admin")

        response = RedirectResponse(url="/admin", status_code=302)
        request.session["user"] = str(user.id)
        return response

    async def logout(self, request: Request) -> RedirectResponse:
        response = RedirectResponse(url="/admin/login", status_code=302)
        self.forget(response)
        return response


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.is_admin]
    form_columns = ["email", "is_admin"]
    column_searchable_list = [User.email]
    can_create = False


class TaskOptionAdmin(ModelView, model=TaskOption):
    column_list = [TaskOption.id, TaskOption.text, TaskOption.tasks]

    @staticmethod
    def make_task_option_form(tasks_choices):
        class _TaskOptionForm(Form):
            text = StringField("Вариант ответа", validators=[DataRequired()])
            tasks = SelectMultipleField(
                "Применимо к заданиям",
                coerce=str,
                choices=tasks_choices
            )
        return _TaskOptionForm

    async def scaffold_form(self, request):
        async with async_session_maker() as session:
            result = await session.execute(
                select(Task).where(Task.task_type != TaskType.text)
            )
            tasks = result.scalars().all()

            choices = [(str(task.id), task.title) for task in tasks]
            return self.make_task_option_form(choices)

class TaskAdmin(ModelView, model=Task):
    # TODO: Add i18n
    form_columns = [
        "title",
        "description",
        "task_type",
        "is_global",
        "assigned_user"
    ]
    form_overrides = {
        "task_type": SelectField
    }

    form_args = {
        "task_type": {
            "choices": [
                ("single_choice", "Один вариант ответа"),
                ("multiple_choice", "Несколько вариантов ответа"),
                ("text", "Свой вариат ответа")
            ]
        }
    }
    column_labels = {
    Task.title: "Название",
    Task.description: "Описание",
    Task.task_type: "Тип задания",
    Task.is_global: "Общее задание (для всех пользователей",
    Task.assigned_user: "Назначено на",
    }


def setup_admin(app):
    admin = Admin(app, engine, authentication_backend=AdminAuth())
    admin.add_view(UserAdmin)
    admin.add_view(TaskAdmin)
    admin.add_view(TaskOptionAdmin)
