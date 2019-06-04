import logging
from flask import Flask, flash, redirect
from flask_appbuilder import SQLA
from flask_appbuilder import AppBuilder
from sqlalchemy.engine import Engine
from sqlalchemy import event
from config import basedir

from flask_appbuilder import IndexView
from flask_appbuilder.security.registerviews import RegisterUserDBView
from flask_appbuilder.security.forms import RegisterUserDBForm
from flask_appbuilder.security.sqla.manager import SecurityManager
from flask_appbuilder._compat import as_unicode

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)


class CustomRegisterUserDBForm(RegisterUserDBForm):
    recaptcha = None


class CustomRegisterUserDBView(RegisterUserDBView):
    form = CustomRegisterUserDBForm

    def form_post(self, form):
        self.add_form_unique_validations(form)

        if not self.appbuilder.sm.add_user(username=form.username.data,
                                           email=form.email.data,
                                           first_name=form.first_name.data,
                                           last_name=form.last_name.data,
                                           role=self.appbuilder.sm.find_role(
                                                       self.appbuilder.sm.auth_user_registration_role),
                                           password=form.password.data):
            flash(as_unicode(self.error_message), 'danger')
            return redirect(self.appbuilder.get_url_for_index)
        else:
            return self.render_template(self.activation_template,
                                        username=form.username.data,
                                        first_name=form.first_name.data,
                                        last_name=form.last_name.data,
                                        appbuilder=self.appbuilder)


class CustomSecurityManager(SecurityManager):
    registeruserdbview = CustomRegisterUserDBView

    def register_views(self):
        self.appbuilder.add_api(self.security_api)

        if self.auth_user_registration:
            self.registeruser_view = self.registeruserdbview()
            self.appbuilder.add_view_no_menu(self.registeruser_view)

        self.appbuilder.add_view_no_menu(self.resetpasswordview())
        self.appbuilder.add_view_no_menu(self.resetmypasswordview())
        self.appbuilder.add_view_no_menu(self.userinfoeditview())

        self.auth_view = self.authdbview()
        self.appbuilder.add_view_no_menu(self.auth_view)

        self.user_view = self.appbuilder.add_view(
            self.userdbmodelview, "List Users",
            icon="fa-user", label="List Users",
            category="Security", category_icon="fa-cogs",
            category_label='Security'
        )

        self.appbuilder.add_view(
            self.userstatschartview,
            "User's Statistics", icon="fa-bar-chart-o",
            label="User's Statistics",
            category="Security"
        )

        self.appbuilder.add_view_no_menu(self.registerusermodelview)


class CustomIndexView(IndexView):
    index_template = 'custom_index.html'


app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
appbuilder = AppBuilder(app, db.session,
                        security_manager_class=CustomSecurityManager,
                        base_template='custom_base.html',
                        indexview=CustomIndexView)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


from app import models, views
