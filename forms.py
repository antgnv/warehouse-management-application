from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class AddProductForm(FlaskForm):
    name = StringField('Название',
                       validators=[DataRequired(), Length(max=50)])
    description = StringField('Описание',
                              validators=[DataRequired(), ])
    price = FloatField('Цена',
                       validators=[DataRequired(), NumberRange(min=0,)])


class AddLocationForm(FlaskForm):
    name = StringField('Название',
                       validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Добавить локацию')
