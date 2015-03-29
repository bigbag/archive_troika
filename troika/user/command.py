from flask.ext.script import Command, Option

from troika.user.models import User


class CreateUser(Command):
    "Create new user"

    option_list = (
        Option('-e', '--email', dest='email', required=True),
        Option('-p', '--password', dest='password', required=True),
        Option('--status', dest='status', default=User.STATUS_ACTIVE),
        Option('--is_admin', dest='is_admin', default=False),
    )

    def run(self, email, password, status, is_admin):

        user = User(email, password)
        user.status = status
        user.is_admin = is_admin
        user.create_user()
