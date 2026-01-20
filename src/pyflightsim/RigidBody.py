from pyglm import glm

from pyflightsim.Transform import Transform


class RigidBody:
    def __init__(self, transform: Transform, mass: float = 1.0):
        self.transform = transform
        self.mass = mass
        self.velocity = glm.vec3(0)  # world space
        self.force = glm.vec3(0)  # world space
        self.gravity = glm.vec3(0, -9.81, 0)

        self.torque = glm.vec3(0)  # local space
        self.inertia = glm.vec3(1)  # simplified
        self.angular_velocity = glm.vec3(0)  # local space

    def add_force(self, force: glm.vec3):
        self.force += force

    def add_force_at(self, force: glm.vec3, position: glm.vec3):
        """Apply a force at a specific position, generating both linear force and torque.

        Args:
            force: The force vector to apply in world space.
            position: The position in local space where the force is applied.
        """
        self.force += force
        self.torque += glm.cross(position, force)

    def update(self, dt: float):
        # Linear
        self.force += self.gravity * self.mass
        acceleration = self.force / self.mass
        self.velocity += acceleration * dt
        self.transform.position += self.velocity * dt

        # Angular
        angular_acceleration = self.torque / self.inertia
        self.angular_velocity += angular_acceleration * dt
        rotation = glm.quat(self.angular_velocity * dt)
        self.transform.rotation *= rotation

        self.force = glm.vec3(0)
        self.torque = glm.vec3(0)
