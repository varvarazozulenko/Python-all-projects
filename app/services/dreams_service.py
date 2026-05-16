import sqlite3
from collections.abc import Sequence

from sqlalchemy import Select, select, func
from sqlalchemy.orm import Session, joinedload

from app import schema
from app.database import models, exceptions


def get_by_id(session: Session, id: int) -> models.Dream | None:
	"""
	:session: сессия sqlalchemy
	:id: идентификатор сна

	Возвращает информацию обо сне, подгружая
	данные об авторе из связанной таблицы 
	(например, используя метод joined_load).
	"""
	query = (
		select(models.Dream)
		.options(
			joinedload(models.Dream.author)
		)
		.filter(models.Dream.id == id)
	)
	return session.execute(query).unique().scalar_one_or_none()


	#raise NotImplementedError


def get_list(
	*,
	session: Session,
	limit: int,
	offset: int,
	author_username: str | None = None,
    search: str | None = None,
    favorited: str | None = None,
) -> tuple[Sequence[models.Dream], int]:
	"""
	:session: сессия sqlalchemy
	:limit: лимит ответа после фильтрации
	:offset: отступ ответа после фильтрации
	:author: фильтр по юзернейму автора

	Получает сны, подгружая данные об авторе
	и лайках (favorited_by) из связанных таблиц
	(например, используя метод joined_load).

	Опционально, фильтрует по автору
		Dream.author.has(User.username.ilike(f'%{author}%')),

	Подсчитывает количество снов после всех наложенных фильтров.
	Наконец, возвращает это число вместе с пагинированным результатом.
	"""
	query = select(models.Dream).options(joinedload(models.Dream.author))

	if author_username:
		query = query.filter(models.Dream.author_id == author_username)

	# Считаем общее кол-во
	count_query = select(func.count()).select_from(query.subquery())
	total_count = session.execute(count_query).scalar() or 0

	query = query.order_by(desc(models.Dream.created_at)).limit(limit).offset(offset)
	result = session.execute(query).unique().scalars().all()

	return result, total_count


#raise NotImplementedError


def create(
	*, session: Session, new_dream: schema.NewDream, author: schema.UserProfile
) -> models.Dream:
	"""
	:session: сессия sqlalchemy
	:new_dream: данные сна для добавления
	:author: данные об авторе

	Добавляет новый сон, включая информацию об авторе, в базу данных.
	В случае, если такой сон уже добавлен, выбрасывает DuplicateDatabaseException.
	Иначе - возвращает ORM-объект с новым сном.
	"""

	try:
		db_dream = models.Dream(
			description=new_dream.description,
			author_id=author.username
		)
		session.add(db_dream)
		session.commit()
		session.refresh(db_dream)
		return db_dream
	except Exception:
		session.rollback()
		raise exceptions.DuplicateDatabaseException("Вы уже создавали такой сон")


#raise NotImplementedError


def delete(*, session: Session, dream_id: int) -> None:
	"""
	:session: сессия sqlalchemy
	:dream_id: идентификатор сна для удаления

	Удаляет сон из базы данных.
	"""
	dream = session.get(models.Dream, dream_id)
	if dream:
		session.delete(dream)
		session.commit()

	#raise NotImplementedError
