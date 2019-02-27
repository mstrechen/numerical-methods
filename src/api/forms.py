from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField,  StringField, validators


class DichotomyForm(FlaskForm):
    f = StringField(
        'Function',
        [validators.required()]
    )

    left_bound = FloatField(
        'Left bound',
        [validators.required()]
    )

    right_bound = FloatField(
        'Right bound',
        [validators.required()]
    )

    eps = FloatField(
        'Epsilon',
        [validators.required()]
    )

    w = IntegerField(
        'Width',
        [validators.optional(), validators.NumberRange(96, 10000)],
        default=100,
    )

    h = IntegerField(
        'Heigth',
        [validators.optional(), validators.NumberRange(96, 10000)],
        default=100,
    )
