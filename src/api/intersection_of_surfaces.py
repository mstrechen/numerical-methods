import math

class Ellipse:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        
    def get_triple(self, alpha, beta):
        return (
            self.a * math.cos(alpha) * math.cos(beta),
            self.b * math.cos(alpha) * math.sin(beta),
            self.c * math.sin(alpha)
        )

    def get_triple_str(self, alpha, beta):
        return "{}, {}, {}".format(*self.get_triple(alpha, beta))
    
DEFAULT_ELLIPSE = Ellipse(2, 1, 3)

class Plane:
    def __init__(self, a=1, b=1, c=1, const=1):
        self.a = a
        self.b = b
        self.c = c
        self.const = const

    def get_z(self, x, y):
        return (-self.const - self.a*x - self.b*y)/self.c

    def get_triple(self, x, y):
        return (x, y, self.get_z(x, y))
    
    def on_the_plane(self, x, y, z, eps):
        return abs(self.a * x + self.b * y + self.c * z + self.const) <= eps

DEFAULT_PLANE = Plane()

def get_ellipsoid():
    res = {
        'x': [],
        'y': [],
        'z': []
    }

    E = DEFAULT_ELLIPSE
    CNT = 20

    for i in range(CNT + 1):
        for j in range(CNT + 1):
            tmp = E.get_triple(
                (math.pi / 2) * (i - CNT / 2)  / (CNT / 2), 
                math.pi * (j - (CNT) / 2) / (CNT / 2)
            )
            res['x'].append(tmp[0])
            res['y'].append(tmp[1])
            res['z'].append(tmp[2])
    
    return res

def get_plane(xminmax, yminmax):
    P = DEFAULT_PLANE
    res = {
        'x': [],
        'y': [],
        'z': []
    }
    for x in xminmax:
        for y in yminmax:
            res['x'].append(x)
            res['y'].append(y)
            res['z'].append(P.get_z(x, y))
    return res


def get_plane_on_ellipsoid():
    res = {
        'x': [],
        'y': [],
        'z': []
    }

    E = DEFAULT_ELLIPSE
    P = DEFAULT_PLANE
    CNT = 200

    
    for i in range(CNT + 1):
        for j in range(CNT + 1):
            tmp = E.get_triple(
                (math.pi / 2) * (i - CNT / 2)  / (CNT / 2), 
                math.pi * (j - (CNT) / 2) / (CNT / 2)
            )
            if(P.on_the_plane(tmp[0], tmp[1], tmp[2], 1e-2)):
                res['x'].append(tmp[0])
                res['y'].append(tmp[1])
                res['z'].append(tmp[2])
    
    return res


def get_all_data():
    res = {
        'ellipsoid': get_ellipsoid()
    }
    res['plane'] = get_plane(
        [
            min(res['ellipsoid']['x']), 
            max(res['ellipsoid']['x']),
        ],
        [
            min(res['ellipsoid']['y']), 
            max(res['ellipsoid']['y']),
        ],
    )
    res['plane_on_ellipsoid'] = get_plane_on_ellipsoid()
    return res

methods = {
    'ellipsoid': get_ellipsoid,
    'all_data': get_all_data,
}