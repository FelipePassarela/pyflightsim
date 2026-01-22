import argparse

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from pyglm import glm

from pyflightsim.RigidBody import RigidBody
from pyflightsim.Transform import Transform

N_FRAMES = 480
DELTA_TIME = 0.016
BOX_SIZE = 10.0
AXIS_LENGTH = BOX_SIZE * 0.15

transform = Transform(
    position=glm.vec3(0, BOX_SIZE / 2, 0),
    rotation=glm.quat(),
    scale=glm.vec3(1, 1, 1),
)
rigid_body = RigidBody(transform=transform, mass=10.0)

fig = plt.figure()
ax: Axes3D = fig.add_subplot(111, projection="3d")

# Matplotlib -> OpenGL axis convention mapping
ax.set_xlabel(r"$Z$")
ax.set_ylabel(r"$X$")
ax.set_zlabel(r"$Y$")

ax.set_xlim(-BOX_SIZE / 2, BOX_SIZE / 2)
ax.set_ylim(-BOX_SIZE / 2, BOX_SIZE / 2)
ax.set_zlim(-BOX_SIZE / 2, BOX_SIZE / 2)

scat = ax.scatter(*transform.position, s=50)


def draw_quivers(transform: Transform):
    origin = transform.position.zxy
    axis_x = transform.right * AXIS_LENGTH
    axis_y = transform.up * AXIS_LENGTH
    axis_z = transform.forward * AXIS_LENGTH

    quiver_x = ax.quiver(*origin, *axis_z, color="r", arrow_length_ratio=0.2)
    quiver_y = ax.quiver(*origin, *axis_x, color="g", arrow_length_ratio=0.2)
    quiver_z = ax.quiver(*origin, *axis_y, color="b", arrow_length_ratio=0.2)
    return quiver_x, quiver_y, quiver_z


quiver_x, quiver_y, quiver_z = draw_quivers(transform)

applied_force = glm.vec3(400, 400, 400)
impact_point = glm.vec3(1, 0, 0)
rigid_body.apply_force_at(applied_force, impact_point)


def update(frame: int) -> tuple:
    global quiver_x, quiver_y, quiver_z

    rigid_body.update(dt=0.016)

    for coord_idx in range(len(transform.position)):
        coord = transform.position[coord_idx]
        if coord < -BOX_SIZE / 2:
            rigid_body.velocity *= -0.8
            rigid_body.angular_velocity *= -0.9
            transform.position[coord_idx] = -BOX_SIZE / 2
        if coord > BOX_SIZE / 2:
            rigid_body.velocity *= -0.8
            rigid_body.angular_velocity *= -0.9
            transform.position[coord_idx] = BOX_SIZE / 2

    scat._offsets3d = (
        np.array([transform.position.z]),
        np.array([transform.position.x]),
        np.array([transform.position.y]),
    )

    quiver_x.remove()
    quiver_y.remove()
    quiver_z.remove()
    quiver_x, quiver_y, quiver_z = draw_quivers(transform)

    return (scat,)


def main() -> None:
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "--no-gui",
        "-n",
        action="store_true",
        help="Run the simulation without displaying the GUI and save it as a GIF file "
        "instead.",
    )
    args = parse.parse_args()

    ani = animation.FuncAnimation(
        fig, update, frames=N_FRAMES, repeat=True, blit=False, interval=16
    )

    if args.no_gui:
        ani.save("rigid_body_simulation.gif", writer="pillow", fps=50)
    else:
        plt.show()


if __name__ == "__main__":
    main()
