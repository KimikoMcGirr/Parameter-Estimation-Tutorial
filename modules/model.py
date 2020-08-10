from scipy.integrate import odeint
from scipy.optimize import fsolve # note: scipy.integrate.solve_ivp is updated function

class Model:
    def __init__(self, inits, time, model):
        self.inits = inits
        self.time = time
        self.model = model

    def run_ss(self, params):
        return fsolve(self.model, self.inits, args=(0, params, 0))

    def run_simulation(self, params, sig):
        return odeint(self.model, self.run_ss(params), self.time, args=(params, sig))

def m1(inits, t, params, sig):
    X, Y = inits
    B, kb, s1, d1, d2 = params

    dX = kb + sig - B * Y - d1 * X
    dY = s1 * X - d2*Y  # * (Y_t-Y)

    return dX, dY

def m2(inits, t, params, sig):
    X, Y = self.inits
    B, kb, s1, d1, d2 = self.params

    dX = kb + sig - B * Y - d1 * X
    dY = s1 * X - d2*Y  # * (Y_t-Y)

    return dX, dY
