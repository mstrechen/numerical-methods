from flask_wtf import FlaskForm
from wtforms import FloatField,  TextField, validators

class DichotomyForm(FlaskForm):
    f = TextField('Function', [validators.required()])
    left_bound = FloatField('Left bound', [validators.required()])
    right_bound = FloatField('Right bound', [validators.required()])
    eps = FloatField('Epsilon', [validators.required()])
