class SqlObjectInterface:
    def write_to_db(self, sql_session):
        sql_session.add(self)
        sql_session.commit()

    @classmethod
    def get_from_db_by_kwargs(cls, sql_session, **kwargs):
        return cls.get_all_from_db_by_kwargs(sql_session, **kwargs).first()

    @classmethod
    def get_all_from_db_by_kwargs(cls, sql_session, **kwargs):
        return sql_session.query(cls).filter_by(**kwargs)

    @classmethod
    def get_from_db_by_attr(cls, sql_session, attr, key):
        return cls.get_from_db_by_kwargs(sql_session, **{attr: key})

    @classmethod
    def get_from_db_by_id(cls, sql_session, my_id):
        return cls.get_from_db_by_attr(sql_session, 'id', my_id)

    @classmethod
    def new_object_from_crest(cls, crest, **kwargs):
        columns = dict()
        for column in cls.__table__.columns.keys():
            if hasattr(crest, column):
                columns[column] = getattr(crest, column)
        return cls(**columns)