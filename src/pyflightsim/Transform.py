from glm import mat4x2
from pyglm import glm


class Transform:
    def __init__(self, position: glm.vec3, rotation: glm.vec3, scale: glm.vec3):
        self.position = position
        self.rotation = rotation  # degrees
        self.scale = scale

    def model(self) -> glm.mat4:
        model = glm.mat4(1)
        model = glm.translate(self.position)
        model = glm.rotate(model, glm.radians(self.rotation.x), (1, 0, 0))
        model = glm.rotate(model, glm.radians(self.rotation.y), (0, 1, 0))
        model = glm.rotate(model, glm.radians(self.rotation.z), (0, 0, 1))
        model = glm.scale(model, self.scale)
        return model

    def apply_to_vec(self, vec: glm.vec3) -> glm.vec3:
        rotation_only = glm.mat3(self.model())
        return rotation_only * vec

    def apply_to_point(self, point: glm.vec4) -> mat4x2:
        return self.model() * point

    @property
    def forward(self) -> glm.vec3:
        return glm.vec3(self.model()[2])

    @property
    def up(self) -> glm.vec3:
        return glm.vec3(self.model()[1])

    @property
    def right(self) -> glm.vec3:
        return glm.vec3(self.model()[0])
