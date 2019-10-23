import json

from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField,  StringField, validators, ValidationError


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

class RungeKuttaForm(CubicSplinesForm):
    x0 = FloatField(
        'Known value x',
        [validators.required()]
    )
    y0 = FloatField(
        'Known value y',
        [validators.required()]
    )
    expected_f = StringField(
        'Expected function',
        [validators.required()]
    )


class RungeKuttaPendulumForm(CubicSplinesForm):
    f = StringField(
        'Function',
        [validators.required()]
    )
    g = StringField(
        'Function',
        [validators.required()]
    )
    left_bound = FloatField(
        'Left bound',
        [validators.required()],
        default=0
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
    x0 = FloatField(
        'Start x\' ',
        [validators.required()],
        default=0
    )

    y0 = FloatField(
        'Start y\' ',
        [validators.required()],
        default=0
    )

    g_const = FloatField(
        'Gravity coef',
        [validators.required()],
        default=9.8
    )

    l_const = FloatField(
        'Length of the pendulum',
        [validators.required()],
        default=1
    )



class PelengateProblem(FlaskForm):
    N = IntegerField(
        'N',
        [validators.required(), validators.NumberRange(2, 100)],
        default=2,
    )
    iters = IntegerField(
        'iters',
        [validators.required(), validators.NumberRange(1, 1000)],
        default=1
    )

    xstart = FloatField(
        'xstart',
        [validators.required()],
        default=0,
    )
    ystart = FloatField(
        'ystart',
        [validators.required()],
        default=0,
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

    #should be json with format [[x1, y1, r1], [x2, y2, r2], ...]
    coefs = StringField(
        'String'
    )

    def validate_coefs(self, field):
        print(field, flush=True)
        try:
            jsondecoded = json.loads(field.data)
        except json.JSONDecodeError:
            raise ValidationError('Field should be json-encoded')
        if type(jsondecoded) != list:
            raise ValidationError('Field should be an array')
        if len(jsondecoded) != self.N.data:
            raise ValidationError('Length of array should be equal to N')
        for row in jsondecoded:
            if len(row) != 3:
                raise ValidationError('Legth of each row should be equal to 3')
            for val in row:
                if type(val) != float and type(val) != int:
                    raise ValidationError('Each value should be either int or float')


