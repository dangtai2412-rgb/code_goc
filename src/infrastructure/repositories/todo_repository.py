from domain.models.itodo_repository import ITodoRepository
from domain.models.todo import Todo
from typing import List, Optional
from dotenv import load_dotenv
from infrastructure.models.todo_model import TodoModel
from infrastructure.databases.mssql import session
from sqlalchemy.orm import Session

load_dotenv()

class TodoRepository(ITodoRepository):
    def __init__(self, session: Session = session):
        self.session = session

    def add(self, todo: Todo) -> TodoModel:
        """Thêm mới Todo vào Database"""
        try:
            # 1. Chuyển đổi từ Domain (Todo) -> Database Model (TodoModel)
            new_todo_model = TodoModel(
                title=todo.title,
                description=todo.description,
                status=todo.status,
                created_at=todo.created_at,
                updated_at=todo.updated_at
            )
            
            # 2. Lưu vào DB
            self.session.add(new_todo_model)
            self.session.commit()
            self.session.refresh(new_todo_model)
            
            return new_todo_model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Lỗi khi thêm Todo: {str(e)}')
        finally:
            self.session.close()

    def get_by_id(self, todo_id: int) -> Optional[TodoModel]:
        """Lấy 1 Todo theo ID"""
        return self.session.query(TodoModel).filter_by(id=todo_id).first()

    def list(self) -> List[TodoModel]:
        """Lấy danh sách tất cả Todo"""
        # select * from todos
        return self.session.query(TodoModel).all()

    def update(self, todo: Todo) -> TodoModel:
        """Cập nhật Todo"""
        try:
            # 1. Tìm bản ghi cũ trong Database bằng ID
            todo_model = self.session.query(TodoModel).filter_by(id=todo.id).first()
            
            if not todo_model:
                raise ValueError('Todo not found')

            # 2. Cập nhật dữ liệu mới vào bản ghi cũ
            todo_model.title = todo.title
            todo_model.description = todo.description
            todo_model.status = todo.status
            todo_model.updated_at = todo.updated_at
            
            # 3. Lưu thay đổi
            self.session.commit()
            return todo_model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Lỗi khi cập nhật Todo: {str(e)}')
        finally:
            self.session.close()

    def delete(self, todo_id: int) -> None:
        """Xóa Todo"""
        try:
            todo_model = self.session.query(TodoModel).filter_by(id=todo_id).first()
            if todo_model:
                self.session.delete(todo_model)
                self.session.commit()
            else:
                raise ValueError('Todo not found')
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Lỗi khi xóa Todo: {str(e)}')
        finally:
            self.session.close()