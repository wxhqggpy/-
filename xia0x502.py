# -*- coding:utf-8 -*-
# 打开0x502模式的数据文件并取出相应结果

from pandas import read_csv

class Xia0x502():
    def __init__(self):
        pass

    # 取出每个通道的能量值做成字典
    def elist(self, addr):
        data = read_csv(addr, skiprows=[0, 1])

        def energy(data):
            for i in data['Energy']:
                yield i

        e = energy(data)
        e0, e1, e2, e3 = [], [], [], []
        for i in data['Channel_No']:
            if i == 0:
                e0.append(next(e))
            elif i == 1:
                e1.append(next(e))
            elif i == 2:
                e2.append(next(e))
            elif i == 3:
                e3.append(next(e))
            else:
                next(e)
        e = {'ch0': e0, 'ch1': e1, 'ch2': e2, 'ch3': e3}
        return e

    # 取出每个通道的PSA值做成字典
    def psa_list(self, addr):
        data = read_csv(addr, skiprows=[0, 1])

        def psa(data):
            for i in data['PSAvalue']:
                yield i

        pv = psa(data)
        pv0, pv1, pv2, pv3 = [], [], [], []
        for i in data['Channel_No']:
            if i == 0:
                pv0.append(next(pv))
            elif i == 1:
                pv1.append(next(pv))
            elif i == 2:
                pv2.append(next(pv))
            elif i == 3:
                pv3.append(next(pv))
            else:
                next(pv)
        pv = {'ch0': pv0, 'ch1': pv1, 'ch2': pv2, 'ch3': pv3}
        return pv

    # 取出每个通道的CFD值，把2,3通道的CFD值逐个相减输出
    def cfd_list(self, addr):
        data = read_csv(addr, skiprows=[0, 1])

        def CFD(data):
            for i in data['CFD']:
                yield i

        cfd = CFD(data)
        cfd0, cfd1, cfd2, cfd3 = [], [], [], []
        for i in data['Channel_No']:
            if i == 0:
                cfd0.append(next(cfd))
            elif i == 1:
                cfd1.append(next(cfd))
            elif i == 2:
                cfd2.append(next(cfd))
            elif i == 3:
                cfd3.append(next(cfd))
            else:
                next(cfd)
        cfd = []
        l = len(cfd3)
        for i in range(l):
            cfd.append(cfd2[i] - cfd3[i])
        return cfd

if __name__ == '__main__':
    f = Xia0x502()
    e = f.elist(r'C:\net test\for python\LMdata setting10 RaBe EJ-339A.dt2')
    pv = f.psa_list(r'C:\net test\for python\LMdata setting10 RaBe EJ-339A.dt2')
    cfd = f.cfd_list(r'C:\net test\for python\LMdata C6 setting13.dt2')
    print(e['ch0'])
    print(pv['ch1'])
    print(cfd[:20])

