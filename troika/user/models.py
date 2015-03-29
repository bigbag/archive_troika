# -*- coding: utf-8 -*-
import datetime as dt
import hashlib
import time

from flask.ext.login import UserMixin

from troika.database import (Column, Model, ReferenceCol, SurrogatePK, db,
                             relationship)
from troika.extensions import bcrypt


class Role(SurrogatePK, Model):
    __tablename__ = 'roles'

    name = Column(db.String(80), unique=True, nullable=False)
    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):

    __tablename__ = 'users'

    STATUS_NEW = 'new'
    STATUS_ACTIVE = 'active'
    STATUS_BANNED = 'banned'

    STATUS = (STATUS_NEW, STATUS_ACTIVE, STATUS_BANNED)

    email = Column(db.String(80), unique=True, nullable=False)
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    lastvisit = Column(db.DateTime)
    activkey = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(128), default=STATUS_NEW, nullable=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, email=None, password=None, **kwargs):
        db.Model.__init__(self, email=email, **kwargs)
        if password:
            self.set_password(password)
            self.set_activkey(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def set_activkey(self, value):
        self.activkey = hashlib.sha1(str(time.time()) + value).hexdigest()

    def update_lastvisit(self):
        self.lastvisit = dt.datetime.utcnow()
        self.save()

    def create_user(self):
        user = User.query.filter_by(email=self.email).first()
        if user:
            print("Email %(email)s already registered" % {'email': self.email})
            return False

        self.save()
        return True

    def __repr__(self):
        return '<User({email!r})>'.format(email=self.email)
