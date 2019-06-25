from flask import flash, redirect

from .models import Product, PrincipioActivo, Contact
from flask_appbuilder import expose, has_access
from flask_appbuilder.views import ModelView, BaseView, SimpleFormView
from flask_appbuilder.charts.views import ChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.widgets import ListBlock, ShowBlockWidget
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget, BS3TextAreaFieldWidget
from flask_appbuilder.forms import DynamicForm

from wtforms import StringField
from wtforms.validators import DataRequired, Email

from app import appbuilder, db


class ProductPubView(ModelView):
    datamodel = SQLAInterface(Product)
    base_permissions = ['can_list', 'can_show']
    list_widget = ListBlock
    show_widget = ShowBlockWidget

    label_columns = {'image_1_markup': 'Image'}

    list_columns = ['code_label', 'name', 'image_1_markup']
    search_columns = ['code', 'name', 'description', 'principio_activo']

    show_fieldsets = [
        ('Summary', {'fields': ['code_label', 'name', 'principio_activo', 'size',
                                'image_1_markup', 'image_2_markup', 'image_3_markup']}),
        ('Description', {'fields': ['description'], 'expanded': True}),
    ]


class ProductView(ModelView):
    datamodel = SQLAInterface(Product)
    list_columns = ['name', 'code_label', 'principio_activo']


class PrincipioActivo(ModelView):
    datamodel = SQLAInterface(PrincipioActivo)
    related_views = [ProductView]
    list_columns = ['name', 'code']


class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)
    can_edit = False


class ContactForm(DynamicForm):
    email = StringField(('Email'), validators=[DataRequired(), Email()],
        description=('Email we can use to contact you'),
        widget=BS3TextFieldWidget())
    name = StringField(('Name'), validators=[DataRequired()],
        widget=BS3TextFieldWidget())
    message = StringField(('Message'), validators=[DataRequired()],
        widget=BS3TextAreaFieldWidget())


class ContactFormView(SimpleFormView):
    form = ContactForm
    form_title = ('If you have any questions or feedback, please feel free to'
                  'get in touch with us using the contact form below.')

    def form_post(self, form):
        # post process form
        c = Contact(email=form.email.data, name=form.name.data, message=form.message.data)
        db.session.add(c)
        db.session.commit()
        flash('Our administrator will be contacting you soon!', 'success')
        return redirect(self.appbuilder.get_url_for_index)


class StaticViews(BaseView):

    @expose('/help/')
    # @has_access
    def help(self):
        return self.render_template('help.html')

    # @expose('/contact/')
    # # @has_access
    # def contact(self):
    #     return self.render_template('contact.html')


db.create_all()

appbuilder.add_view(ProductPubView, 'Our Products', icon='fa-list')
appbuilder.add_view(StaticViews, 'Help', href='/staticviews/help/', icon='fa-info')
appbuilder.add_view(ContactFormView, 'Contact Us')
appbuilder.add_view(ProductView, 'Products', icon='fa-gear', category='Administer')
appbuilder.add_separator('Administer')
appbuilder.add_view(PrincipioActivo, 'Principios Activos', icon='fa-flask', category='Administer')
appbuilder.add_separator('Administer')
appbuilder.add_view(ContactModelView, 'Contacts', icon='fa-envelope', category='Administer')


appbuilder.security_cleanup()

# Permisos predefinidos para el cliente
client = appbuilder.sm.add_role('Client')
for view_name in ['ResetMyPasswordView', 'ProductPubView', 'Our Products',
                  'UserInfoEditView', 'UserDBModelView', 'Help', 'Contact Us',
                  'ContactFormView']:
    view = appbuilder.sm.find_view_menu(view_name)
    for perm in appbuilder.sm.find_permissions_view_menu(view):
        appbuilder.sm.add_permission_role(client, perm)
