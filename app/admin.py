import enum
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi_users.password import PasswordHelper

from app.models.user import User
from app.models.task import Task
from app.db.database import engine
from app.config import SECRET_KEY
from app.auth.manager import get_user_manager
from wtforms import SelectField



templates = Jinja2Templates(directory="app/templates")


# 🔐 Кастомная авторизация
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


class TaskAdmin(ModelView, model=Task):
    # TODO: Add i18n
    # column_list = [
    #     Task.id,
    #     Task.title,
    #     Task.task_type,
    #     Task.is_global,
    #     Task.assigned_user
    # ]
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