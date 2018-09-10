# -*- coding:utf-8 -*-

import tkinter
from matplotlib.pyplot import figure, hist, legend
import xia0x400
import xia0x502
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# 生成能谱图
def energy_spec(addr):
    if addr[-3:] == 'b00':
        data = xia0x400.Xia0x400()
    elif addr[-3:] == 'dt2':
        data = xia0x502.Xia0x502()
    e = data.elist(addr)
    e0 = list(map(lambda x: x / 64, e['ch0']))
    e1 = list(map(lambda x: x / 64, e['ch1']))
    e2 = list(map(lambda x: x / 64, e['ch2']))
    e3 = list(map(lambda x: x / 64, e['ch3']))

    fig = figure(figsize=(4, 3))

    num_bins = 1024
    n0, bins0, patches0 = hist(e0, num_bins, range=(0, num_bins), facecolor='green', alpha=1, label='ch0')
    n1, bins1, patches1 = hist(e1, num_bins, range=(0, num_bins), facecolor='blue', alpha=1, label='ch1')
    n2, bins2, patches2 = hist(e2, num_bins, range=(0, num_bins), facecolor='red', alpha=1, label='ch2')
    n3, bins3, patches3 = hist(e3, num_bins, range=(0, num_bins), facecolor='purple', alpha=1, label='ch3')
    legend(prop={'size': 5})

    return fig


# 生成PSA谱图
def PSA_spec(addr, scal):
    if addr[-3:] == 'b00':
        return None
    elif addr[-3:] == 'dt2':
        data = xia0x502.Xia0x502()
    pv = data.psa_list(addr)
    pv0 = list(map(lambda x: x / scal, pv['ch0']))
    pv1 = list(map(lambda x: x / scal, pv['ch1']))
    pv2 = list(map(lambda x: x / scal, pv['ch2']))
    pv3 = list(map(lambda x: x / scal, pv['ch3']))

    fig = figure(figsize=(4, 3))

    num_bins = 256
    n0, bins0, patches0 = hist(pv0, num_bins, range=(0, num_bins), facecolor='green', alpha=1, label='ch0')
    n1, bins1, patches1 = hist(pv1, num_bins, range=(0, num_bins), facecolor='blue', alpha=1, label='ch1')
    n2, bins2, patches2 = hist(pv2, num_bins, range=(0, num_bins), facecolor='red', alpha=1, label='ch2')
    n3, bins3, patches3 = hist(pv3, num_bins, range=(0, num_bins), facecolor='purple', alpha=1, label='ch3')
    legend(prop={'size': 5})

    return fig


# 生成2,3通道的demo版CFD谱图
def CFD_spec(addr, scal):
    if addr[-3:] == 'b00':
        data = xia0x400.Xia0x400()
    elif addr[-3:] == 'dt2':
        data = xia0x502.Xia0x502()
    cfd = list(map(lambda x: x / scal, data.cfd_list(addr)))

    fig = figure(figsize=(4, 3))

    num_bins = 256
    n, bins, patches = hist(cfd, num_bins * 2, range=(-num_bins, num_bins), facecolor='green', alpha=1,
                                label='ch2-ch3')
    legend(prop={'size': 5})

    return fig


# 产生PSA谱的刻度值填写窗口
def scale_value(b):
    def start():
        s = float(en.get())
        plot(b, s)

    window = tkinter.Tk()

    if b == 'b3':
        t = '请输入合适的刻度值（建议“1”）'
    elif b == 'b4':
        t = '请输入合适的刻度值（建议“5”）'
    lb = tkinter.Label(window, text=t)
    lb.grid(row=0, column=0)

    en = tkinter.Entry(window)
    en.grid(row=1, column=0)

    b1 = tkinter.Button(window, text='start', command=start)
    b1.grid(row=2, column=0)

    window.mainloop()


# 产生谱图的新窗口
def plot(b, scal):
    global addrs
    plot = tkinter.Tk()
    if b == 'b2':
        figs = energy_spec(addrs)
    elif b == 'b3':
        figs = PSA_spec(addrs, scal)
    elif b == 'b4':
        figs = CFD_spec(addrs, scal)
    canvas = FigureCanvasTkAgg(figs, master=plot)
    # canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    plot.mainloop()


if __name__ == "__main__":
    window = tkinter.Tk()
    window.title('XIA数据分析demo')
    window.geometry('400x300')
    window1 = tkinter.LabelFrame(window)
    window1.grid(row = 0, column = 0)

    def xz():
        global lb1, addrs
        addrs = tkinter.filedialog.askopenfilename()
        if addrs != '':
            lb1.config(text=addrs)
        else:
            lb1.config(text="您没有选择任何文件")


    lb1 = tkinter.Label(window1, text="请选择一个文件")
    lb1.grid(row=0, column=0, stick=tkinter.W)

    b1 = tkinter.Button(window1, text='选择', command=xz)
    b1.grid(row=0, column=1)

    b2 = tkinter.Button(window1, text='start Energy_plot', command=lambda: plot(b='b2', scal=1))
    b2.grid(row=2, column=0)

    b3 = tkinter.Button(window1, text='start PSA_plot(only .dt2)', command=lambda: scale_value(b='b3'))
    b3.grid(row=3, column=0)

    b4 = tkinter.Button(window1, text='start CFD_demo', command=lambda: scale_value(b='b4'))
    b4.grid(row=4, column=0)

    window.mainloop()
