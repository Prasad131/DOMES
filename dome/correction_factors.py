from math import sin, pi, log
from lewis_factor import LewisFactor
from bending_geometry_factor import BendingGeometryFactor


class Factors:

    def __init__(self, m, Np, Ng, np, phi, b, r, vp, vg, Ep, Eg, hp, hg, cycle_p, cycle_g, tR=2, hT=1, gear_type=1,
                 crown=False, centered=True, variety=0, grade=1, power_source=0, driven_machine=0, Qv=6):
        mg = Ng / Np
        self.ko_ = self.ko(power_source, driven_machine)
        d = m * Np
        v = pi * d * np / 60
        self.kv_ = self.kv(v, Qv)
        self.ks_ = self.ks(b, m, Np)
        self.kh_ = self.kh(b, d, gear_type, crown, centered)
        self.kb_ = self.kb(tR, hT)
        self.zi_ = self.zi(phi, mg)
        self.ze_ = self.ze(vp, vg, Ep, Eg)
        self.yz_ = self.yz(r)
        self.zw_ = self.zw(hp, hg, mg, gear=False)
        self.st_ = self.st(hp, variety, grade)
        self.sc_ = self.sc(hp, variety, grade)
        self.yj_ = self.yj(Np, Ng)
        self.yn_ = self.yn(cycle_p)
        self.zn_ = self.zn(cycle_g)

    def kv(self, v, qv=None):
        if qv is None:
            qv = 7
        b = 0.25 * (12 - qv) ** (2 / 3)
        a = 50 + 56 * (1 - b)
        k = ((a + (200 * v) ** 0.5) / a) ** b
        return k

    def ks(self, b, m, n):
        Y = LewisFactor(20, n)
        Y = Y.val_
        k = 0.904 * (b * m * Y ** 0.5) ** 0.0535
        return k

    def kh(self, b, d, gear_type=1, crown=False, centered=True):
        if crown:
            cmc = 0.8
        else:
            cmc = 1
        if centered:
            cpm = 1
        else:
            cpm = 1.1
        if b <= 25:
            cpf = b / (10 * d) - 0.025
        elif 25 < b <= 425:
            cpf = b / (10 * d) - 0.0375 + 4.92 * (10 ** -4) * b
        else:
            cpf = b / (10 * d) - 0.01109 + 8.15 * 10 ** -4 * b - 3.53 * 10 ** -7 * b ** 2
        f = b / 25.4
        """
            Gear types are as follows:
            0 --> open gearing
            1 --> commercial enclosed units
            2 --> precision enclosed units
            3 --> extra-precision enclosed units 
        """
        if gear_type == 0:
            A, B, C = 0.247, 0.0167, -0.765 * 10 ** -4
        elif gear_type == 1:
            A, B, C = 0.127, 0.0158, -0.93 * 10 ** -4
        elif gear_type == 2:
            A, B, C = 0.0675, 0.0128, -0.926 * 10 ** -4
        else:
            A, B, C = 0.0036, 0.0102, -0.822 * 10 ** -4
        cma = A + B * f + C * f ** 2
        ce = 1
        k = 1 + cmc * (cpf * cpm + cma * ce)
        return k

    def ko(self, power_source=0, driven_machine=0):
        """

        :param power_source: 0 --> Uniform, 1 --> Light shock, 2 --> Medium shock
        :param driven_machine: 0 --> uniform 1 --> Moderate shock, 2 --> Heavy shock
        :return: Ko
        """
        a = [[1, 1.25, 1.75], [1.25, 1.5, 2], [1.5, 1.75, 2.25]]
        k = a[power_source][driven_machine]
        return k

    def kb(self, tR=2, hT=1):
        mB = tR / hT
        if mB < 1.2:
            k = 1.6 * log(2.242 / mB)
        else:
            k = 1
        return k

    def zi(self, phi, mg, external=True):
        temp = sin(2 * phi) * mg / 4
        if external:
            k = temp / (mg + 1)
        else:
            k = temp / (mg - 1)
        return k

    def ze(self, vp, vg, Ep, Eg):
        k = (1 / (pi * ((1 - vp ** 2) / Ep + (1 - vg ** 2) / Eg))) ** 0.5
        return k

    def yz(self, r):
        if 0.5 < r < 0.99:
            k = 0.658 - 0.0759 * log(1 - r)
        else:
            k = 0.5 - 0.109 * log(1 - r)
        return k

    def zw(self, hp, hg, mg, gear=True):
        if gear:
            if 1.2 <= hp / hg <= 1.7:
                a = 8.98 * 10 ** -3 * (hp / hg) - 8.29 * 10 ** -3
                k = 1 + a * (mg - 1)
            elif hp / hg < 1.2:
                k = 1
            else:
                k = 1 + 0.00698 * (mg - 1)
        else:
            k = 1
        return k

    def st(self, hb, variety=0, grade=1):
        """

        :param variety: 0 --> hardened steels, 1 --> nitrided through hardened steels, 2 --> nitriding steels
        :param grade: 1 --> 1, 2 --> 2
        :param hb: Brinell Hardness number
        :return: St
        """
        grade_error = 'Other grades are not defined as of now'
        if variety == 0:
            if grade == 1:
                k = 0.533 * hb + 88.3
            elif grade == 2:
                k = 0.703 * hb + 113
            else:
                raise ValueError(grade_error)
        elif variety == 1:
            if grade == 1:
                k = 0.568 * hb + 83.8
            elif grade == 2:
                k = 0.749 * hb + 110
            else:
                raise ValueError(grade_error)
        elif variety == 2:
            if grade == 1:
                k = 0.594 * hb + 87.76
            elif grade == 2:
                k = 0.784 * hb + 114.81
            else:
                raise ValueError(grade_error)
        return k

    def sc(self, hb, variety=0, grade=1):
        """

        :param variety: 0 --> through hardened steels
        :param grade: 1 --> 1, 2 --> 2
        :param hb: Brinell Hardness number
        :return: Sc
        """
        grade_error = 'Other grades are not defined as of now'
        type_error = 'Other types are not defined as of now'

        if variety == 0:
            if grade == 1:
                k = 2.22 * hb + 200
            elif grade == 2:
                k = 2.41 * hb + 237
            else:
                raise ValueError(grade_error)
        else:
            raise ValueError(type_error)

        return k

    def yj(self, np, ng):
        y = BendingGeometryFactor(np, ng)
        return y.val_

    def yn(self, n):
        k = 1.3558 * n ** -.0178
        return k

    def zn(self, n):
        k = 1.4488 * n ** -0.023
        return k
