from sqlalchemy import func, select
from sqlalchemy import update


class SqlAlchemyRepository:
    class Config:
        model = None

    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._base_query = select(self.Config.model)

    def get_one_or_none(self, **kwargs):
        stmt = select(self.Config.model).filter_by(**kwargs)
        result = self.session_factory.execute(stmt)
        return result.scalar_one_or_none()

    def create_one(self, **kwargs):
        instance = self.Config.model(**kwargs)
        self.session_factory.add(instance)
        self.session_factory.commit()
        return instance

    def get_or_create(self, default, **kwargs):
        instance = self.get_one_or_none(**kwargs)
        if instance is None:
            return (self.create_one(**(kwargs | default)), True)
        else:
            return (instance, False)

    def update_one(self, attrs: dict, **kwargs):
        stmt = (
            update(self.Config.model)
            .filter_by(**kwargs)
            .values(**attrs)
            .returning(self.Config.model)
        )
        result = self.session_factory.execute(stmt)
        self.session_factory.commit()
        return result.scalar_one_or_none()

    def delete_one(self, **kwargs):
        instance = self.get_one_or_none(**kwargs)
        if instance is None:
            return None
        self.session_factory.delete(instance)
        self.session_factory.commit()
        return instance

    def filter(self, **kwargs):
        self._base_query = self._base_query.filter_by(**kwargs)
        return self

    def order_by(self, *args):
        self._base_query = self._base_query.order_by(*args)
        return self

    def join(self, *args):
        self._base_query = self._base_query.join(*args)
        return self

    def first(self):
        result = self.session_factory.execute(self._base_query)
        return result.scalar_one_or_none()

    def all(self):
        result = self.session_factory.execute(self._base_query)
        return result.scalars().all()

    def base(self, query):
        self._base_query = query
        return self

    def query(self):
        return self._base_query

    def fetch(self, limit, page=1):
        page = int(page)
        limit = int(limit)
        if page <= 0:
            raise ValueError("page value must be greater or equal 1")
        if limit <= 0:
            raise ValueError("limit value must be greater or equal 1")

        stmt = self._base_query.offset((page - 1) * limit).limit(limit)
        result = self.session_factory.execute(stmt).scalars().all()

        stmt = select(func.ceil(func.count() / limit)).select_from(self._base_query)

        total_pages = self.session_factory.execute(stmt).scalar_one_or_none()
        next_page = page + 1
        if next_page > total_pages:
            next_page = None
        prev_page = page - 1
        if prev_page < 1:
            prev_page = None
        current_page = page

        return {
            "result": result,
            "prev_page": prev_page,
            "next_page": next_page,
            "total_pages": total_pages,
            "current_page": current_page,
        }

    def delete_all(self):
        self.session_factory.query(self.Config.model).delete()
        self.session_factory.commit()
