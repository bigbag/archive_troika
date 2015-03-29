import logging
from flask.ext.script import Command, Option

from troika.user.models import User


class AddUser(Command):
    "Added new user"

    option_list = (
        Option('-e', '--email', dest='email', required=True),
        Option('-p', '--password', dest='password', required=True),
        Option('--status', dest='status', default=User.STATUS_ACTIVE),
        Option('--is_admin', dest='is_admin', default=False),
    )

    def run(self, **args):

        user = User(args['email'], args['password'])
        user.status = args['status']
        user.is_admin = args['is_admin']

        old_user = User.query.filter_by(email=user.email).first()
        if old_user:
            msg = "Error adding. Email %(email)s already registered" % {
                'email': user.email}
            logging.debug(msg)
            return

        try:
            user.save()
        except Exception as e:
            logging.exception("Exception: %(body)s", {'body': e})
            return
        else:
            print user.id
