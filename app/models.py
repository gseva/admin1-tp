from flask import Markup, url_for
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from flask_appbuilder.models.mixins import ImageColumn
from flask_appbuilder.filemanager import ImageManager
from flask_appbuilder import Model
from flask_appbuilder.security.sqla.models import User


class PrincipioActivo(Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text())

    def __repr__(self):
        return self.name


class Product(Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text())
    image_1 = Column(ImageColumn)
    image_2 = Column(ImageColumn)
    image_3 = Column(ImageColumn)
    size = Column(Enum('70 ml', '100 ml', '150 ml', '250 ml', name='size'))
    principio_activo_id = Column(Integer, ForeignKey('principio_activo.id'), nullable=False)
    principio_activo = relationship('PrincipioActivo')

    def _image(self, name):
        im = ImageManager()
        imagen = getattr(self, name)
        if imagen:
            # url = url_for('ProductPubView.show', pk=str(self.id))
            # return Markup('<a href="' + url + '" class="thumbnail"><img src="' +
            #               im.get_url(imagen) + '" alt="Photo" class="img-rounded img-responsive"></a>')
            return Markup('<center><img src="' + im.get_url(imagen) + '" alt="Photo" class="img-rounded img-responsive"></center>')
        else:
            # return Markup('<a href="' + url_for('ProductPubView.show', pk=str(self.id)) +
            #               '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')
            #return Markup('<center><img src="//:0" alt="Photo" class="img-responsive"></center>')
            return ''

    def image_1_markup(self):
        return self._image('image_1')

    def image_2_markup(self):
        return self._image('image_2')

    def image_3_markup(self):
        return self._image('image_3')

    def code_label(self):
        return Markup('Code: <strong>{}</strong>'.format(self.code))

    def __repr__(self):
        return self.name


class Contact(Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(), nullable=False)
    name = Column(String())
    message = Column(String())


class Client(User):
    __tablename__ = 'ab_user'
