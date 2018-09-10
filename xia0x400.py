# -*- coding:utf-8 -*-
# 打开0x400模式的数据文件并取出相应结果

class Xia0x400():
    def __init__(self):
        pass

    # 取出每个通道的能量值做成字典
    def elist(self, addr):
        with open(addr, 'rb') as f:
            f.seek(4, 0)
            run_type = f.read(2)
            f.seek(16, 0)
            event_length0 = int.from_bytes(f.read(2), 'little') * 64
            event_length1 = int.from_bytes(f.read(2), 'little') * 64
            event_length2 = int.from_bytes(f.read(2), 'little') * 64
            event_length3 = int.from_bytes(f.read(2), 'little') * 64

            if run_type == b'\x00\x04':
                f.seek(64, 0)
                f.seek(16, 1)
                energy = f.read(2)
                channo = f.read(2)
                e0, e1, e2, e3 = [], [], [], []
            else:
                return None
            while channo:
                energy_d = int.from_bytes(energy, 'little')
                channo_d = int.from_bytes(channo, 'little')
                if channo_d == 0:
                    e0.append(energy_d)
                    f.seek(event_length0 - 4, 1)
                elif channo_d == 1:
                    e1.append(energy_d)
                    f.seek(event_length1 - 4, 1)
                elif channo_d == 2:
                    e2.append(energy_d)
                    f.seek(event_length2 - 4, 1)
                elif channo_d == 3:
                    e3.append(energy_d)
                    f.seek(event_length3 - 4, 1)
                energy = f.read(2)
                channo = f.read(2)
            e = {'ch0': e0, 'ch1': e1, 'ch2': e2, 'ch3': e3}
            return e

    #取出每个通道的CFD值，把2,3通道的CFD值逐个相减输出
    def cfd_list(self, addr):
        with open(addr, 'rb') as f:
            f.seek(4, 0)
            run_type = f.read(2)
            f.seek(16, 0)
            event_length0 = int.from_bytes(f.read(2), 'little') * 64
            event_length1 = int.from_bytes(f.read(2), 'little') * 64
            event_length2 = int.from_bytes(f.read(2), 'little') * 64
            event_length3 = int.from_bytes(f.read(2), 'little') * 64

            if run_type == b'\x00\x04':
                f.seek(64, 0)
                f.seek(18, 1)
                channo = f.read(2)
                f.seek(2, 1)
                cfd = f.read(2)
                cfd0, cfd1, cfd2, cfd3 = [], [], [], []
            else:
                return None
            while channo:
                cfd_d = int.from_bytes(cfd, 'little')
                channo_d = int.from_bytes(channo, 'little')
                if channo_d == 0:
                    cfd0.append(cfd_d)
                    f.seek(event_length0 - 6, 1)
                elif channo_d == 1:
                    cfd1.append(cfd_d)
                    f.seek(event_length1 - 6, 1)
                elif channo_d == 2:
                    cfd2.append(cfd_d)
                    f.seek(event_length2 - 6, 1)
                elif channo_d == 3:
                    cfd3.append(cfd_d)
                    f.seek(event_length3 - 6, 1)
                channo = f.read(2)
                f.seek(2, 1)
                cfd = f.read(2)
            cfd = []
            l = len(cfd2)
            for i in range(l):
                cfd.append(cfd2[i] - cfd3[i])
            return cfd

if __name__ == '__main__':
    f = Xia0x400()
    e = f.elist(r'C:\net test\for python\LMdata setting12 RaBe EJ-339A.b00')
    print(e['ch0'])
