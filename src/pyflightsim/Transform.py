from pyglm import glm


class Transform:
    def __init__(self, position: glm.vec3, rotation: glm.quat, scale: glm.vec3):
        self.position = position
        self.rotation = rotation
        self.scale = scale

    def get_matrix(self) -> glm.mat4:
        T = glm.translate(self.position)
        R = glm.mat4_cast(self.rotation)
        S = glm.scale(self.scale)
        return T * R * S

    def apply_to_vec(self, vec: glm.vec3) -> glm.vec3:
        return self.rotation * vec

    def apply_to_point(self, point: glm.vec3) -> glm.vec3:
        p_homogeneous = glm.vec4(point, 1)  # ty:ignore[no-matching-overload]
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
