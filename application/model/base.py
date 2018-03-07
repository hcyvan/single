import datetime

from application.ext import db


class BaseModel(db.Model):
    __abstract__ = True
    db = db
    exclude_fields = []

    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow)

    def to_dict(self):
        result = {}
        for c in self.__dict__.keys():
            if c.startswith('_') or c in self.exclude_fields:
                continue
            value = getattr(self, c, None)
            if isinstance(value, list):
                result[c] = [e.to_dict() if isinstance(e, db.Model) else e for e in value]
            else:
                result[c] = value

        return result

    def update(self):
        self.db.session.commit()
        return self

    def save(self):
        try:
            self.db.session.add(self)
            self.db.session.commit()
            # self.db.session.refresh(self)
        except Exception as e:
            self.db.session.rollback()

    def delete(self):
        self.db.session.delete(self)
        self.db.session.commit()


def parse_model_list(models):
    model_list = []
    for model in models:
        model_list.append(model.to_dict())

    return model_list


def parse_paginate(paginate):
    models = paginate.items
    model_list = parse_model_list(models)
    result = {
        'items': model_list,
        'pages': paginate.pages,
        'page_index': paginate.page,
        'page_size': paginate.per_page,
        'total': paginate.total,
    }

    return result
