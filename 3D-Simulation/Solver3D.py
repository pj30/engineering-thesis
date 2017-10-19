import numpy as np
import math as mt
import time

def IX(i, j, k): return (size_2D * i + size_1D * j + k) # takes index of 3D matrix and returns index for 1D array

def add_source(x, s): return (x + dt * s)

def set_bnd(b, x):

    if b == 1:
        x[0, :, :] = -x[1, :, :]
        x[N + 1, :, :] = -x[N, :, :]
    else:
        x[0, :, :] = x[1, :, :]
        x[N + 1, :, :] = x[N, :, :]
    if b == 2:
        x[:, 0, :] = -x[:, 1, :]
        x[:, M + 1, :] = -x[:, M, :]
    else:
        x[:, 0, :] = x[:, 1, :]
        x[:, M + 1, :] = x[:, M, :]
    if b == 3:
        x[:, :, 0] = -x[:, :, 1]
        x[:, :, L + 1] = -x[:, :, L]
    else:
        x[:, :, 0] = x[:, :, 1]
        x[:, :, L + 1] = x[:, :, L]

    x[0, 0, 0] = .5 * (x[1, 0, 0] + x[0, 1, 0] + x[0, 0, 1])
    x[0, 0, L + 1] = .5 * (x[1, 0, L + 1] + x[0, 1, L + 1] + x[0, 0, L])
    x[0, M + 1, 0] = .5 * (x[1, M + 1, 0] + x[0, M + 1, 1] + x[0, M, 0])
    x[N + 1, 0, 0] = .5 * (x[N + 1, 0, 0] + x[N + 1, 0, 1] + x[N, 0, 0])
    x[N + 1, M + 1, 0] = .5 * (x[N + 1, M + 1, 1] + x[N + 1, M, 0] + x[N, M + 1, 0])
    x[N + 1, 0, L + 1] = .5 * (x[N + 1, 1, L + 1] + x[N + 1, 0, L] + x[N, 0, L + 1])
    x[0, M + 1, L + 1] = .5 * (x[1, M + 1, L + 1] + x[0, M + 1, L] + x[0, M, L + 1])
    x[N + 1, M + 1, L + 1] = .5 * (x[N + 1, M, L] + x[N, M + 1, L] + x[N, M, L + 1])

    return x

def diffuse(b, x, x0, diff, dt):
    a = dt * diff * N * M * L
    den = (1 + 6 * a)
    for l in range(10):
        x[1 : N, 1 : M, 1 : L] = x0[1 : N, 1 : M, 1 : L] + a * (x[0 : -3, 1 : M, 1 : L] + x[2 : -1, 1 : M, 1 : L]
                                                                + x[1 : N, 0 : -3, 1 : L] + x[1 : N, 2 : -1, 1 : L]
                                                                + x[1 : N, 1 : M, 0 : -3] + x[1 : N, 1 : M, 2 : -1]) / den
        return set_bnd(b, x)

def advect(b, d, d0, h_vel, v_vel, d_vel, dt):
    dx = dt * N
    dy = dt * M
    dz = dt * L
    d = np.reshape(d, size_3D)
    d0 = np.reshape(d0, size_3D)
    h_vel = np.reshape(h_vel, size_3D)
    v_vel = np.reshape(v_vel, size_3D)
    d_vel = np.reshape(d_vel, size_3D)
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            for k in range(1, L + 1):

                x = i - dx * h_vel[IX(i, j, k)]
                y = j - dy * v_vel[IX(i, j, k)]
                z = k - dz * d_vel[IX(i, j, k)]

                if (x < .5): x = .5
                if (x > N + .5): x = N + .5
                i0 = int(x)
                i1 = i0 + 1

                if (y < .5): y = .5
                if (y > M + .5): y = M + .5
                j0 = int(y)
                j1 = j0 + 1

                if (z < .5): z = .5
                if (z > L + .5): z = L + .5
                k0 = int(z)
                k1 = k0 + 1

                r1 = x - i0
                r0 = 1 - r1
                s1 = y - j0
                s0 = 1 - s1
                t1 = z - k0
                t0 = 1 - t1

                d[IX(i, j, k)] = r0 * (s0 * (t0 * d0[IX(i0, j0, k0)] + t1 * d0[IX(i0, j0, k1)]) + s1 * (t0 * d0[IX(i0, j1, k0)] + t1 * d0[IX(i0, j1, k1)])) + r1 * (s0 * (t0 * d0[IX(i1, j0, k0)] + t1 * d0[IX(i1, j0, k1)]) + s1 * (t0 * d0[IX(i1, j1, k0)] + t1 * d0[IX(i1, j1, k1)]))
    d = np.reshape(d, (N + 2, M + 2, L + 2))
    if b == 0:
        d *= sum_dens / d[1 : N, 1 : N, 1 : N].sum()

    return set_bnd(b, d)

def dens_step(x, x0, h_vel, v_vel, d_vel, diff, dt0):
    x = add_source(x, x0)
    x, x0 = x0, x
    x = diffuse(0, x, x0, diff, dt)
    x, x0 = x0, x
    x = advect(0, x, x0, h_vel, v_vel, d_vel, dt)
    return x, x0

def vel_step(h_vel, v_vel, d_vel, h_vel_prev, v_vel_prev, d_vel_prev, visc, dt):

    h_vel = add_source(h_vel, h_vel_prev)
    v_vel = add_source(v_vel, v_vel_prev)
    d_vel = add_source(d_vel, d_vel_prev)
    h_vel, h_vel_prev = h_vel_prev, h_vel
    h_vel = diffuse(1, h_vel, h_vel_prev, visc, dt)
    v_vel, v_vel_prev = v_vel_prev, v_vel
    v_vel = diffuse(2, v_vel, v_vel_prev, visc, dt)
    d_vel, d_vel_prev = d_vel_prev, d_vel
    d_vel = diffuse(3, d_vel, d_vel_prev, visc, dt)

    h_vel, v_vel, d_vel, h_vel_prev, v_vel_prev, d_vel_prev = project(h_vel, v_vel, d_vel)
    # swap
    h_vel, h_vel_prev = h_vel_prev, h_vel
    v_vel, v_vel_prev = v_vel_prev, v_vel
    d_vel, d_vel_prev = d_vel_prev, d_vel

    h_vel = advect(1, h_vel, h_vel_prev, h_vel_prev, v_vel_prev, d_vel_prev, dt)
    v_vel = advect(2, v_vel, v_vel_prev, h_vel_prev, v_vel_prev, d_vel_prev, dt)
    d_vel = advect(3, d_vel, d_vel_prev, h_vel_prev, v_vel_prev, d_vel_prev, dt)
    h_vel, v_vel, d_vel, h_vel_prev, v_vel_prev, d_vel_prev = project(h_vel, v_vel, d_vel)
    return h_vel, v_vel, d_vel

def project(h_vel, v_vel, d_vel):
    h = 1. / N
    div_v = np.zeros((N2, M2, L2))
    div_d = np.zeros((N2, M2, L2))
    p = np.zeros((N2, M2, L2))
    div_v[1 : N, 1 : M, 1 : L] = -.5 * h * (h_vel[2 : -1, 1 : M, 1 : L] - h_vel[0 : -3, 1 : M, 1 : L]
                                            + v_vel[1 : N, 1 : M, 2 : -1] - v_vel[1 : N, 1 : M, 0 : -3])

    div_d[1 : N, 1 : M, 1 : L] = -.5 * h * (h_vel[2 : -1, 1 : M, 1 : L] - h_vel[0 : -3, 1 : M, 1 : L]
                                            + d_vel[1 : N, 1 : M, 2 : -1] - d_vel[1 : N, 1 : M, 0 : -3])

    div_v = set_bnd(0, div_v)
    div_d = set_bnd(0, div_d)
    p = set_bnd(0, p)
    div = (div_v + div_d) / 2
    for l in range(10):
        p[1 : N, 1 : M, 1 : L] = (div[1 : N, 1 : M, 1 : L] + p[2 : N + 1, 1 : M, 1 : L] - p[0 : N - 1, 1 : M, 1 : L]
                                                            + p[1 : N, 2 : M + 1, 1 : L] - p[1 : N, 0 : M - 1, 1 : L]
                                                            + p[1 : N, 1 : M, 2 : L + 1] - p[1 : N, 1 : M, 0 : L - 1]) / 6
        p = set_bnd(0, p)

    h_vel[1 : N, 1 : M, 1 : L] -= .5 * (p[2 : -1, 1 : M, 1 : L] - p[0 : -3, 1 : M, 1 : L]) / h
    v_vel[1 : N, 1 : M, 1 : L] -= .5 * (p[1 : N, 2 : -1, 1 : L] - p[1 : N, 0 : -3, 1 : L]) / h
    d_vel[1 : N, 1 : M, 1 : L] -= .5 * (p[1 : N, 1 : M, 2 : -1] - p[1 : N, 1 : M, 0 : -3]) / h
    h_vel = set_bnd(1, h_vel)
    v_vel = set_bnd(2, v_vel)
    d_vel = set_bnd(3, d_vel)
    return h_vel, v_vel, d_vel, p, div_v, div_d

N = 10
M = 10
L = 10
N2 = N + 2
M2 = M + 2
L2 = L + 2
size_1D = N2
size_2D = N2 * M2
size_3D = N2 * M2 * L2
# horizontal, vertical and diagonal velocities
h_vel = np.zeros((N2, M2, L2))
v_vel = np.zeros((N2, M2, L2))
d_vel = np.zeros((N2, M2, L2))

h_vel_prev = np.zeros((N2, M2, L2))
v_vel_prev = np.zeros((N2, M2, L2))
d_vel_prev = np.zeros((N2, M2, L2))

dens = np.zeros((N2, M2, L2))
dens_prev = np.zeros((N2, M2, L2))
dt = .035
visc = .0000001
diff = .00001
x = np.zeros((500, N2, M2, L2))
dens[5 : 10, 5 : 10 : 5, 8 : 10] = 7.
sum_dens = dens[1 : N, 1 : M, 1 : L].sum()

x[0, :, :, :] = dens

for i in range(499):
    start = time.time()
    print('Progress: ', int((i/499) * 100), '%')

    h_vel, v_vel, d_vel = vel_step(h_vel, v_vel, d_vel, h_vel_prev, v_vel_prev, d_vel_prev, visc, dt)
    dens, dens_prev = dens_step(dens, dens_prev, h_vel, v_vel, d_vel, diff, dt)
    v_vel_prev = -.15 * np.absolute(dens)

    #h_vel_prev = .15 * np.absolute(dens)
    h_vel_prev = np.zeros((N2, M2, L2))
    d_vel_prev = np.zeros((N2, M2, L2))
    dens_prev = np.zeros((N2, M2, L2))

    x[i + 1, :, :, :] = dens
    print(' Left', int((time.time() - start) * (499 - i)), 's')
x = np.reshape(x, (500, size_3D))
np.save('array2.npy',x)
