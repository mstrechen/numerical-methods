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


class FixedPointIterationForm(FlaskForm):
    f = StringField(
        'Function',
        [validators.required()]
    )

    lamb = StringField(
        'Lambda',
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
        'Iterations count',
        [validators.required(), validators.NumberRange(0, 10000)]
    )

    x0 = FloatField(
        'x_0',
        [validators.required()]
    )

    tracing = FloatField(
        'Iterations count',
        [validators.optional(), validators.NumberRange(0, 1)],
        default=1
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


class LinearSystems(FlaskForm):
    n = IntegerField(
        'N',
        [validators.required(), validators.NumberRange(100, 1000)]
    )

class UnnamedMatrixForm(FlaskForm):
    n = IntegerField(
        'N',
        [validators.required(), validators.NumberRange(1, 1000)]
    )
    m = IntegerField(
        'M',
        [validators.required(), validators.NumberRange(1, 1000)]
    )
    k = IntegerField(
        'K',
        [validators.required(), validators.NumberRange(1, 1000)]
    )
    func = StringField(
        'func',
        [validators.required()]
    )
    



class CubicSplinesForm(FlaskForm):
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

    N = IntegerField(
        'Count of segments',
        [validators.required(), validators.NumberRange(1, 1000)]
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

class ChebyshevApproxForm(CubicSplinesForm):
    M = IntegerField(
        'Count of functions',
        [validators.required(), validators.NumberRange(1, 100)]
    )