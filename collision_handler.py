from typing import Any, Callable, Tuple
import pymunk


CollisionCallback = Callable[[pymunk.Arbiter, pymunk.Space, Any], None]

PUNCH = 1
EARTH = 2
asteroid = 3
SHEILD = 4


def add_collision_handler(space: pymunk.Space, objects: Tuple[int, int], begin: CollisionCallback = None, post: CollisionCallback = None):
    handler = space.add_collision_handler(*objects)
    if begin is not None:
        def col_begin(*args):
            begin(*args)
            return True
        handler.begin = col_begin
    if post is not None:
        def col_post(*args):
            post(*args)
            return True
        handler.post_solve = col_post
