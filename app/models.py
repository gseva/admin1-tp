from flask import Markup, url_for
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from flask_appbuilder.models.mixins import ImageColumn
from flask_appbuilder.filemanager import ImageManager
from flask_appbuilder import Model
from flask_appbuilder.security.sqla.models import User


class PrincipioActivo(Model):
    id = Column(Integer, primary_key=True)
    codigo = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(50), unique=True, nullable=False)
    description = Column(Text())

    def __repr__(self):
        return self.nombre


class Producto(Model):
    id = Column(Integer, primary_key=True)
    codigo = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text())
    imagen_1 = Column(ImageColumn)
    imagen_2 = Column(ImageColumn)
    imagen_3 = Column(ImageColumn)
    tamanio = Column(Enum('70 ml', '100 ml', '150 ml', '250 ml'))
    principio_activo_id = Column(Integer, ForeignKey('principio_activo.id'), nullable=False)
    principio_activo = relationship('PrincipioActivo')

    def _imagen(self, nombre_imagen):
        im = ImageManager()
        imagen = getattr(self, nombre_imagen)
        if imagen:
            url = url_for('ProductoPubView.show', pk=str(self.id))
            return Markup('<a href="' + url + '" class="thumbnail"><img src="' +
                          im.get_url(imagen) + '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup('<a href="' + url_for('ProductoPubView.show', pk=str(self.id)) +
                          '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')

    def imagen_1_markup(self):
        return self._imagen('imagen_1')

    def imagen_2_markup(self):
        return self._imagen('imagen_2')

    def imagen_3_markup(self):
        return self._imagen('imagen_3')

    def codigo_label(self):
        return Markup('Codigo: <strong>{}</strong>'.format(self.codigo))

    def __repr__(self):
        return self.nombre


class Client(User):
    __tablename__ = 'ab_user'
