import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from pyglm import glm

from pyflightsim.Transform import Transform

N_FRAMES = 120
AXIS_LENGTH = 0.3
DELTA_TIME = 0.016

transform = Transform(
    position=glm.vec3(0, 1, 0),
    rotation=glm.quat(),
    scale=glm.vec3(1, 1, 1),
)

fig = plt.figure()
ax: Axes3D = fig.add_subplot(111, projection="3d")
ax.set_xlabel(r"$X$")
ax.set_ylabel(r"$Y$")
ax.set_zlabel(r"$Z$")
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_zlim(0.0, 1.0)

scat = ax.scatter(*transform.position)

# Local transform axis
origin = transform.position
axis_x = transform.right * AXIS_LENGTH
axis_y = transform.up * AXIS_LENGTH
axis_z = transform.forward * AXIS_LENGTH

origin = transform.position
quiver_x = ax.quiver(*origin, *axis_x, color="r", arrow_length_ratio=0.2)
quiver_y = ax.quiver(*origin, *axis_y, color="g", arrow_length_ratio=0.2)
quiver_z = ax.quiver(*origin, *axis_z, color="b", arrow_length_ratio=0.2)


def update(frame: int) -> tuple:
    global quiver_x, quiver_y, quiver_z

    angle_step = 360 / N_FRAMES
    transform.rotate_by(glm.vec3(0, 0, angle_step))
    forward = transform.up  # matplotlib z-axis points "up" and the y-axis "forward"
    transform.position += forward * DELTA_TIME

    scat._offsets3d = (
        np.array([transform.position.x]),
        np.array([transform.position.y]),
        np.array([transform.position.z]),
    )

    quiver_x.remove()
    quiver_y.remove()
    quiver_z.remove()

    axis_x = transform.right * AXIS_LENGTH
    axis_y = transform.up * AXIS_LENGTH
    axis_z = transform.forward * AXIS_LENGTH

    origin = transform.position
    quiver_x = ax.quiver(*origin, *axis_x, color="r", arrow_length_ratio=0.2)
    quiver_y = ax.quiver(*origin, *axis_y, color="g", arrow_length_ratio=0.2)
    quiver_z = ax.quiver(*origin, *axis_z, color="b", arrow_length_ratio=0.2)

    return (scat,)


def main() -> None:
    _ = animation.FuncAnimation(fig, update, frames=N_FRAMES, interval=16, repeat=True)
    plt.show()


if __name__ == "__main__":
    main()
