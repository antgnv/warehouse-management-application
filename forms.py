from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class AddProductForm(FlaskForm):
    name = StringField('Название',
                       validators=[DataRequired(), Length(max=50)])
    description = StringField('Описание',
                              validators=[DataRequired(), ])
    price = FloatField('Цена',
                       validators=[DataRequired(), ])
    submit = SubmitField('Добавить товар')


class AddLocationForm(FlaskForm):
    name = StringField('Название',
                       validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Добавить локацию')
