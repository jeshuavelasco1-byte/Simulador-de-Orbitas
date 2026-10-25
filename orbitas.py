import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

GM = 4 * np.pi**2  # UA^3 / año^2 (masa del Sol = 1)


def aceleracion(r):
    return -GM * r / np.linalg.norm(r) ** 3


def simular_verlet(r0, v0, dt, pasos):
    r = np.zeros((pasos, 2))
    v = np.zeros((pasos, 2))
    r[0], v[0] = r0, v0
    a = aceleracion(r[0])
    for i in range(pasos - 1):
        r[i + 1] = r[i] + v[i] * dt + 0.5 * a * dt**2
        a_nueva = aceleracion(r[i + 1])
        v[i + 1] = v[i] + 0.5 * (a + a_nueva) * dt
        a = a_nueva
    return r, v


def simular_euler(r0, v0, dt, pasos):
    r = np.zeros((pasos, 2))
    v = np.zeros((pasos, 2))
    r[0], v[0] = r0, v0
    for i in range(pasos - 1):
        a = aceleracion(r[i])
        # Método de Euler explícito
        r[i + 1] = r[i] + v[i] * dt
        v[i + 1] = v[i] + a * dt
    return r, v


if __name__ == "__main__":
    dt, pasos = 0.001, 5000
    v_circular = 2 * np.pi  # velocidad circular a 1 UA
    r0 = np.array([1.0, 0.0])
    v0 = np.array([0.0, 0.8 * v_circular])

    # Simular con ambos métodos
    r_verlet, _ = simular_verlet(r0, v0, dt, pasos)
    r_euler, _ = simular_euler(r0, v0, dt, pasos)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    ax.set_xlim(-2.0, 2.0)  # Ampliado para ver la divergencia de Euler
    ax.set_ylim(-2.0, 2.0)

    # Sol
    ax.plot(0, 0, "yo", markersize=12, label="Sol")

    # Inicializar líneas y planetas para ambos métodos
    linea_verlet, = ax.plot([], [], "b-", lw=0.8, label="Verlet (Estable)")
    planeta_verlet, = ax.plot([], [], "bo")

    linea_euler, = ax.plot([], [], "r--", lw=0.8, label="Euler (Inestable)")
    planeta_euler, = ax.plot([], [], "ro")

    ax.legend(loc="upper right")

    def actualizar(i):
        # Actualizar Verlet
        linea_verlet.set_data(r_verlet[: i + 1, 0], r_verlet[: i + 1, 1])
        planeta_verlet.set_data([r_verlet[i, 0]], [r_verlet[i, 1]])

        # Actualizar Euler
        linea_euler.set_data(r_euler[: i + 1, 0], r_euler[: i + 1, 1])
        planeta_euler.set_data([r_euler[i, 0]], [r_euler[i, 1]])

        return linea_verlet, planeta_verlet, linea_euler, planeta_euler

    anim = FuncAnimation(
        fig, actualizar, frames=range(0, pasos, 10), interval=20, blit=True
    )
    plt.show()
