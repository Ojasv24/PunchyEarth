import pymunk


class GravityPoint():
    def __init__(self, space) -> None:
        self.body = pymunk.body
        self.body.apply_force_at_world_point((10, 10), (100, 100))
        self.shape = pymunk.Circle(self.body, 10)
        space.add(self.body, self.shape)
