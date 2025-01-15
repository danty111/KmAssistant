import numpy as np

_w = np.asarray([0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65])
_b = np.asarray([0.35, 0.65])

# 假设有一条样本
_x = np.asarray(
    [5.0, 10.0]
)

_y = np.asarray(
    [0.1, 0.99]
)

lr = 0.5


def w(i):
    return _w[i - 1]


def b(i):
    return _b[i - 1]


def x(i):
    return _x[i - 1]


def y(i):
    return _y[i - 1]


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def set_w(i, gd):
    i = i - 1
    _w[i] = _w[i] - gd * lr


def training():
    h1 = sigmoid(z=x(1) * w(1) + x(2) * w(2) + b(1))
    h2 = sigmoid(z=x(1) * w(3) + x(1) * w(4) + b(1))
    h3 = sigmoid(z=x(1) * w(5) + x(2) * w(6) + b(1))

    o1 = sigmoid(z=h1 * w(7) + h2 * w(9) + h3 * w(11) + b(2))
    o2 = sigmoid(z=h1 * w(8) + h2 * w(10) +h3 * w(12) + b(2))

    loss = 0.5 * (o1 - y(1)) ** 2 + 0.5 * (o2 - y(2)) ** 2

    t1 = - (y(1) - o1) * o1 * (1 - o1)
    t2 = - (y(2) - o2) * o2 * (1 - o2)

    set_w(7, gd = t1*h1)
    set_w(8, gd=t2 * h1)
    set_w(9, gd=t1 * h2)
    set_w(10, gd=t2 * h2)
    set_w(11, gd=t1 * h3)
    set_w(12, gd=t2 * h3)
    
    
    set_w(1,gd = (t1 * w(7) + t2 * w(8))* h1 * (1-h1)*x(1))
    set_w(2, gd=(t1 * w(7) + t2 * w(8)) * h1 * (1 - h1) * x(2))
    set_w(3, gd=(t1 * w(9) + t2 * w(10)) * h2 * (1 - h1) * x(1))
    set_w(4, gd=(t1 * w(9) + t2 * w(10)) * h2 * (1 - h1) * x(2))
    set_w(5, gd=(t1 * w(11) + t2 * w(12)) * h3* (1 - h1) * x(1))
    set_w(6, gd=(t1 * w(11) + t2 * w(12)) * h3 * (1 - h1) * x(2))

    return loss


if __name__ == '__main__':
    losses = []
    r = training()
    losses.append(r[0])
    print(f"第一次更新后的结果：{r}")
    for i in range(100):
        r = training()
        losses.append(r[0])