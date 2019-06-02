from .models import Product, PrincipioActivo
from flask_appbuilder.views import ModelView, BaseView
from flask_appbuilder.charts.views import ChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.widgets import ListBlock, ShowBlockWidget

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


db.create_all()

appbuilder.add_view(ProductPubView, 'Our Products', icon='fa-list')
appbuilder.add_view(ProductView, 'Products', icon='fa-gear', category='Administer')
appbuilder.add_separator('Administer')
appbuilder.add_view(PrincipioActivo, 'Principios Activos', icon='fa-flask', category='Administer')

appbuilder.security_cleanup()

# Permisos predefinidos para el cliente
client = appbuilder.sm.add_role('Client')
for view_name in ['ResetMyPasswordView', 'ProductPubView', 'Our Products', 'UserInfoEditView', 'UserDBModelView']:
    view = appbuilder.sm.find_view_menu(view_name)
    for perm in appbuilder.sm.find_permissions_view_menu(view):
        appbuilder.sm.add_permission_role(client, perm)
