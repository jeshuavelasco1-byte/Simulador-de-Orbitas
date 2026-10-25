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


def energia(r, v):
    """Energía por unidad de masa: cinética + potencial."""
    return 0.5 * np.sum(v**2, axis=1) - GM / np.linalg.norm(r, axis=1)


if __name__ == "__main__":
    dt, pasos = 0.001, 5000
    v_circular = 2 * np.pi  # velocidad circular a 1 UA
    r0 = np.array([1.0, 0.0])
    v0 = np.array([0.0, 0.8 * v_circular])

    # 1. Simular con ambos métodos (una sola vez)
    r_verlet, v_verlet = simular_verlet(r0, v0, dt, pasos)
    r_euler, v_euler = simular_euler(r0, v0, dt, pasos)

    # 2. Configurar Fig 1: Animación de las órbitas
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    ax.set_xlim(-2.0, 2.0)  # Ampliado para ver la divergencia de Euler
    ax.set_ylim(-2.0, 2.0)

    # Sol
    ax.plot(0, 0, "yo", markersize=12, label="Sol")

    # Inicializar líneas y planetas para ambos métodos
    (linea_verlet,) = ax.plot([], [], "b-", lw=0.8, label="Verlet (Energia casi constante)")
    (planeta_verlet,) = ax.plot([], [], "bo")

    (linea_euler,) = ax.plot([], [], "r--", lw=0.8, label="Euler (Energia crece)")
    (planeta_euler,) = ax.plot([], [], "ro")

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

    # 3. Configurar Fig 2: Cálculo y Gráfica de energía
    t = np.arange(pasos) * dt
    E0 = energia(r_verlet[:1], v_verlet[:1])[0]
    err_verlet = np.abs((energia(r_verlet, v_verlet) - E0) / E0)
    err_euler = np.abs((energia(r_euler, v_euler) - E0) / E0)

    print(f"Error final de energía, Euler:  {err_euler[-1]:.2e}")
    print(f"Error final de energía, Verlet: {err_verlet[-1]:.2e}")

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    ax2.semilogy(t[1:], err_euler[1:], "r--", label="Euler Explícito")
    ax2.semilogy(t[1:], err_verlet[1:], "b-", label="Velocity Verlet")
    ax2.set_xlabel("Tiempo (años)")
    ax2.set_ylabel("Error relativo de energía |ΔE/E₀|")
    ax2.set_title("Conservación de la energía")
    ax2.legend()
    ax2.grid(True, which="both", alpha=0.3)

    # Guardar gráfica de energía antes de renderizar pantallas
    fig2.savefig("energia.png", dpi=150, bbox_inches="tight")

    # Muestra ambas ventanas en paralelo simultáneamente
    plt.show()
