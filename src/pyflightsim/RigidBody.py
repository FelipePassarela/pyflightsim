from pyglm import glm

from pyflightsim.Transform import Transform


class RigidBody:
    def __init__(self, transform: Transform, mass: float = 1.0):
        self.mass = glm.max(0.0001, mass)
        self.transform = transform

        self.forces = glm.vec3()
        self.velocity = glm.vec3()
        self.gravity = glm.vec3(0.0, -9.81, 0.0)

        self.angular_velocity = glm.vec3()
        self.torque = glm.vec3()
        self.inertia = glm.mat3x3(1.0)
        self.inv_inertia = glm.inverse(self.inertia)

    def apply_force(self, force: glm.vec3):
        self.forces += force

    def apply_force_at(self, force: glm.vec3, position: glm.vec3):
        """position relative to body origin (local space)"""
        self.forces += force
        r_world = self.transform.rotation * position
        self.torque += glm.cross(r_world, force)

    def update(self, dt: float):
        # Linear
        self.forces += self.gravity * self.mass
        acc = self.forces / self.mass
        self.velocity += acc * dt
        self.transform.position += self.velocity * dt

        # Angular
        gyro = glm.cross(self.angular_velocity, self.inertia * self.angular_velocity)
        angular_acc = self.inv_inertia * (self.torque - gyro)
        self.angular_velocity += angular_acc * dt

        if glm.length(self.angular_velocity) > 1e-8:
            angle = glm.length(self.angular_velocity) * dt
            axis = glm.normalize(self.angular_velocity)
            dq = glm.angleAxis(angle, axis)
            self.transform.rotation *= glm.normalize(dq)

        self.velocity *= 0.999
        self.angular_velocity *= 0.999
        self.forces = glm.vec3()
        self.torque = glm.vec3()
