from flask import Blueprint, redirect, render_template, request, url_for
from flask.ext.login import (current_user, login_required, login_user,
                             logout_user)

from troika.extensions import login_manager
from troika.user.forms import LoginForm
from troika.user.models import User
from troika.utils import flash_errors

blueprint = Blueprint('user', __name__, url_prefix='/user',
                      static_folder="../static")


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


def extra_login_user(user, remember=False, force=False):
    if login_user(user, remember, force):
        current_user.update_lastvisit()


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            extra_login_user(form.user)
            redirect_url = request.args.get("next") or url_for('public.index')
            return redirect(redirect_url)
        else:
            flash_errors(form)

    return render_template("user/login.html", form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))
