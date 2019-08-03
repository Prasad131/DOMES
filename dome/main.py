from correction_factors import Factors


class Gear:
    def __init__(self, Ft, m, Np, Ng, np, phi, b, r, vp, vg, Ep, Eg, hp, hg, cycle_p, cycle_g, tR=2, hT=1, gear_type=1,
                 crown=False, centered=True, variety=0, grade=1, power_source=0, driven_machine=0, Qv=6):

        factors = Factors(m, Np, Ng, np, phi, b, r, vp, vg, Ep, Eg, hp, hg, cycle_p, cycle_g, tR, hT, gear_type, crown,
                          centered, variety, grade, power_source, driven_machine, Qv)

        d = m * Np

        sb_all = self.sigma_b_all(Ft, factors.ko_, factors.kv_, factors.ks_, factors.kh_, factors.kb_, b, m, factors.yj_)
        sc_all = self.sigma_c_all(Ft, factors.ko_, factors.kv_, factors.ks_, factors.kh_, d, b, factors.zi_, factors.ze_)

        self.sf_ = self.sf(factors.st_, factors.yn_, factors.yz_, sb_all)
        self.sh_ = self.sh(factors.sc_, factors.zn_, factors.zw_, factors.yz_, sc_all)


    def sigma_b_all(self, ft, ko, kv, ks, kh, kb, b, m, yj):
        s = (ft * ko * kv * ks * kh * kb) / (b * m * yj)
        return s

    def sigma_c_all(self, ft, ko, kv, ks, kh, d, b, zi, ze):
        s = ze * ((ft * ko - kv * ks * kh) / (d * b * zi)) ** 0.5
        return s

    def sf(self, st, yn, yz, sb_all):
        k = (st * yn) / (sb_all * yz)
        return k

    def sh(self, sc, zn, zw, yz, sc_all):
        k = (sc * zn * zw) / (sc_all * yz)
        return k


if __name__ == '__main__':
    gear = Gear(11538, 4.5, 16, 76, 388.88, 20, 40, 0.99, 0.3, 0.3, 210000, 210000, 300, 300, 10**8, 21052631, Qv=7)
    print(gear.sf_)
    print(gear.sh_)
