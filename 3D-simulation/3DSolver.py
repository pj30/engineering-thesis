import numpy as np
import math as mt

N = 2
M = 2
L = 2
size_1D = N + 2
size_2D = size_1D * (M + 2)
size_3D = size_2D * (L + 2)

# horizontal, vertical and diagonal velocities
h_vel = np.empty(size_3D)
v_vel = np.empty(size_3D)
d_vel = np.empty(size_3D)

h_vel_prev = np.empty(size_3D)
v_vel_prev = np.empty(size_3D)
d_vel_prev = np.empty(size_3D))

dens = np.empty(size_3D)
dens_prev = np.empty(size_3D)

def IX(i, j, k): return (size_2D * i + size_1D * j + k) # takes index of 3D matrix and returns index for 1D array

def add_source(x, s): return (x + dt * s)

def set_bnd(b, d):
    print('a')

def diffuse(b, x, x0, diff, dt):
    a = dt * diff * N * M * L
    for l in range(20):
        for i in range(1, N + 1):
            for j in range(1, M + 1):
                for k in range(1, L + 1):
                    x[IX(i, j, k)] = (x0[IX(i, j, k)] + a * (x[IX(i - 1, j, k)] + x[IX(i + 1, j, k)] + x[IX(i, j - 1, k)] + x[IX(i, j + 1, k)] + x[IX(i, j, k - 1)] + x[IX(i, j, k + 1)])) / (1 + 6 * a)
    return set_bnd(b, x)

def advect(b, d, d0, h_vel, v_vel, d_vel, dt):
    dx = dt * N
    dy = dt * M
    dz = dt * L
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

                d(IX[i, j, k]) = r0 * (s0 * (t0 * d0[IX(i0, j0, k0)] + t1 * d0[IX(i0, j0, k1)])
                                    + s1 * (t0 * d0[IX(i0, j1, k0)] + t1 * d0[IX(i0, j1, k1)])) +
                                r1 * (s0 * (t0 * d0[IX(i1, j0, k0)] + t1 * d0[IX(i1, j0, k1)])
                                    + s1 * (t0 * d0[IX(i1, j1, k0)] + t1 * d0[IX(i1, j1, k1)]))
    return set_bnd(b, d)

def dens_step(x, x0, h_vel, v_vel, d_vel, diff, dt0):
    x = add_source(x, x0, dt)
    x, x0 = x0, x
    x = diffuse(0, x, x0, diff, dt)
    x, x0 = x0, x
    x = advect(0, x, x0, h_vel, v_vel, d_vel, dt)
    return x

def vel_step():
    
x = (2.,4.,5.,3.)
dt = .1
s = np.array([1.,1.,1.,1.])
