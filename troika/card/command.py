import logging

from flask.ext.script import Command, Option

from troika.card.models import Card


class AddCard(Command):

    "Added new card"

    option_list = (
        Option('-hid', '--hard_id', dest='hard_id', required=True),
        Option('-tid', '--troika_id', dest='troika_id', required=True),
        Option('--name_ru', dest='name_ru'),
        Option('--name_en', dest='name_en'),
    )

    def run(self, **args):

        card = Card(args['hard_id'], args['troika_id'])
        if 'name_ru' in args:
            card.name_ru = args['name_ru']
        if 'name_en' in args:
            card.name_en = args['name_en']

        old_card = Card.query.filter(
            (Card.hard_id == card.hard_id) |
            (Card.troika_id == card.troika_id)).first()
        if old_card:
            msg = """Error adding. Card with hard_id %(hard_id)s
                    or troika_id %(troika_id)s already registered""" % {
                'hard_id': card.hard_id,
                'troika_id': card.troika_id}
            logging.debug(msg)
            return

        try:
            card.save()
        except Exception as e:
            logging.exception("Exception: %(body)s", {'body': e})
            return
        else:
            return card.id
