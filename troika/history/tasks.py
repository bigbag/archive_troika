# -*- coding: utf-8 -*-
from troika.extensions import celery
from troika.history.models import CardsHistory


@celery.task()
def update_action(user_id, card_id, before, after):

    if before == after:
        return

    history = CardsHistory(user_id)
    history.action = CardsHistory.ACTION_UPDATE
    history.card_id = card_id
    history.before = before
    history.after = after
    history.save()
    return history.id


@celery.task()
def create_action(user_id, card_id, after):

    history = CardsHistory(user_id)
    history.action = CardsHistory.ACTION_CREATE
    history.card_id = card_id,
    history.before = ''
    history.after = after
    history.save()
    return history.id
