from .models import Producto, PrincipioActivo
from flask_appbuilder.views import ModelView, BaseView
from flask_appbuilder.charts.views import ChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.widgets import ListBlock, ShowBlockWidget

from app import appbuilder, db


class ProductoPubView(ModelView):
    datamodel = SQLAInterface(Producto)
    base_permissions = ['can_list', 'can_show']
    list_widget = ListBlock
    show_widget = ShowBlockWidget

    label_columns = {'imagen_1_markup': 'Imagen'}

    list_columns = ['codigo_label', 'nombre', 'imagen_1_markup']
    search_columns = ['codigo', 'nombre', 'descripcion', 'principio_activo']

    show_fieldsets = [
        ('Summary', {'fields': ['codigo_label', 'nombre', 'principio_activo',
                                'imagen_1_markup', 'imagen_2_markup', 'imagen_3_markup']}),
        ('Description', {'fields': ['description'], 'expanded': True}),
    ]


class ProductoView(ModelView):
    datamodel = SQLAInterface(Producto)


class PrincipioActivo(ModelView):
    datamodel = SQLAInterface(PrincipioActivo)
    related_views = [ProductoView]


db.create_all()

appbuilder.add_view(ProductoPubView, 'Nuestros Productos', icon='fa-list')
appbuilder.add_view(ProductoView, 'Productos', icon='fa-gear', category='Administrar')
appbuilder.add_separator('Administrar')
appbuilder.add_view(PrincipioActivo, 'Principios Activos', icon='fa-flask', category='Administrar')

appbuilder.security_cleanup()

# Permisos predefinidos para el cliente
client = appbuilder.sm.add_role('Client')
for view_name in ['ResetMyPasswordView', 'ProductoPubView', 'Nuestros Productos', 'UserInfoEditView', 'UserDBModelView']:
    view = appbuilder.sm.find_view_menu(view_name)
    for perm in appbuilder.sm.find_permissions_view_menu(view):
        appbuilder.sm.add_permission_role(client, perm)
