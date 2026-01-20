from pyglm import glm


class Transform:
    def __init__(
        self,
        position: glm.vec3 = glm.vec3(0),
        rotation: glm.quat = glm.quat(),
        scale: glm.vec3 = glm.vec3(1),
    ):
        self.position = position
        self.rotation = rotation
        self.scale = scale

    def get_matrix(self) -> glm.mat4:
        T = glm.translate(self.position)
        R = glm.mat4_cast(self.rotation)
        S = glm.scale(self.scale)
        return T * R * S

    def translate_by(self, translation: glm.vec3):
        self.position += translation

    def rotate_by(self, euler: glm.vec3):
        self.euler_angles += euler

    def scale_by(self, scale: glm.vec3):
        self.scale += scale

    def transform_direction(self, dir: glm.vec3) -> glm.vec3:
        return self.rotation * dir

    def transform_point(self, point: glm.vec3) -> glm.vec3:
        p_homogeneous = glm.vec4(point, 1)
        return glm.vec3(self.get_matrix() * p_homogeneous)

    @property
    def forward(self) -> glm.vec3:
        return self.rotation * glm.vec3(0, 0, 1)

    @property
    def up(self) -> glm.vec3:
        return self.rotation * glm.vec3(0, 1, 0)

    @property
    def right(self) -> glm.vec3:
        return self.rotation * glm.vec3(1, 0, 0)

    @property
    def euler_angles(self) -> glm.vec3:
        return glm.degrees(glm.eulerAngles(self.rotation))

    @euler_angles.setter
    def euler_angles(self, degrees: glm.vec3):
        self.rotation = glm.quat(glm.radians(degrees))
