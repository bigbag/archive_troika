# -*- coding: utf-8 -*-
import json

from flask.ext.login import current_user

from troika.database import Model, ReferenceCol, SurrogatePK, db, relationship
from troika.helpers import date_helper

from troika.campus.models import Campus


class Card(SurrogatePK, Model):

    __tablename__ = 'cards'

    PER_PAGE = 50

    SEARCH_KEYS = ('troika_id', 'hard_id')

    STATUS_NEW = 'new'
    STATUS_INPROGRESS = 'inprogress'
    STATUS_RELEASED = 'released'
    STATUS_DELIVERED = 'delivered'
    STATUS_REMOVED = 'removed'

    STATUS_TITLE = {STATUS_NEW: u'Новая',
                    STATUS_INPROGRESS: u'В процессе',
                    STATUS_RELEASED: u'Выпущена',
                    STATUS_DELIVERED: u'Доставлена',
                    STATUS_REMOVED: u'Удалена'}

    STATE_ACTIVE = 0
    STATE_LOST = 1
    STATE_BROKEN = 3
    STATE_NOT_NEED = 5
    STATE_REISSUED = 6

    TROIKA_STATE_TITLE = {STATE_ACTIVE: u'Рабочая',
                          STATE_LOST: u'Утеряна',
                          STATE_BROKEN: u'Испорчена',
                          STATE_NOT_NEED: u'Не нужна',
                          STATE_REISSUED: u'Перевыпущена'}

    TROIKA_STATE_LOCKED = (STATE_LOST, STATE_BROKEN, STATE_NOT_NEED, STATE_REISSUED)
    
    SPOT_URL = "spot/hard_id"

    hard_id = db.Column(db.String(128), unique=True, nullable=False)
    troika_id = db.Column(db.String(128), unique=True, nullable=False)
    name_ru = db.Column(db.String(300))
    name_en = db.Column(db.String(300))
    creation_date = db.Column(db.DateTime, nullable=False)
    update_date = db.Column(db.DateTime, default=date_helper.get_current_date())
    troika_state = db.Column(db.Integer(), index=True, nullable=False, default=STATE_ACTIVE)
    status = db.Column(db.String(128), nullable=False, default=STATUS_NEW)
    order_id = ReferenceCol('orders', nullable=True)
    order = relationship('Order', backref='cards')
    report_id = ReferenceCol('reports', nullable=True)
    report = relationship('Report', backref='cards')
    campus_id = ReferenceCol('campus', nullable=True)
    campus = relationship('Campus', backref='cards')
    

    def __init__(self, hard_id=None, troika_id=None, **kwargs):
        self.old_card = None
        if hard_id and troika_id:
            self.hard_id = hard_id
            self.troika_id = troika_id
            self.creation_date = date_helper.get_current_date()
            self.troika_state = self.STATE_ACTIVE
            self.status = self.STATUS_NEW

        db.Model.__init__(self, **kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'hard_id': self.hard_id,
            'troika_id': self.troika_id,
            'name_ru': self.name_ru,
            'troika_state': self.troika_state,
            'status': self.status,
            'order_id': self.order_id,
            'report_id': self.report_id,
            'campus_id': self.campus_id,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def get_status_title(self):
        status_title = self.STATUS_TITLE

        if self.status == self.STATUS_NEW:
            return status_title

        if self.status == self.STATUS_INPROGRESS:
            return {
                self.STATUS_INPROGRESS: u'В процессе',
                self.STATUS_RELEASED: u'Выпущена',
                self.STATUS_DELIVERED: u'Доставлена',
                self.STATUS_REMOVED: u'Удалена'
            }

        if self.status == self.STATUS_RELEASED:
            return {
                self.STATUS_RELEASED: u'Выпущена',
                self.STATUS_DELIVERED: u'Доставлена',
                self.STATUS_REMOVED: u'Удалена'
            }

        if self.status == self.STATUS_DELIVERED:
            return {
                self.STATUS_DELIVERED: u'Доставлена',
                self.STATUS_REMOVED: u'Удалена'
            }

        return {self.status: status_title.get(self.status)}

    def get_troika_state_title(self):
        troika_state_title = self.TROIKA_STATE_TITLE
        if self.troika_state == self.STATE_ACTIVE:
            return troika_state_title

        return {self.troika_state: troika_state_title.get(self.troika_state)}

    def get_locked(self):
        return self.query.filter(Card.troika_state.in_(self.TROIKA_STATE_LOCKED)).\
            filter(Card.report_id.is_(None)).all()

    def get_new_and_active(self, hard_id):
        return self.query.filter_by(hard_id=hard_id).\
            filter_by(status=self.STATUS_NEW).\
            filter_by(troika_state=self.STATE_ACTIVE).first()

    def save(self):
        from troika.history import tasks as history_tasks
        self.update_date = date_helper.get_current_date()
        
        if self.campus_id == 0:
            self.campus_id = None

        result = super(Card, self).save()

        if not result:
            return result

        user_id = None
        if not current_user.is_anonymous():
            user_id = current_user.id

        history_tasks.update_action.delay(
            user_id, result.id, result.old_card, result.to_json())

        return result
        
    def get_campus_title(self):
        campuses = Campus.query.all()
        
        list = {}
        
        for campus in campuses:
            list[campus.id] = u'%s %s (%s)' % (campus.id, campus.name, campus.address)

        return list
        
    def __repr__(self):
        return '<Card ({hard_id!r})>'.format(hard_id=self.hard_id)
