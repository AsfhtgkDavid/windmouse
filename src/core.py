from abc import ABC, abstractmethod
from typing import NewType, Generator

import numpy as np

Coordinate = NewType("Coordinate", int)

sqrt3 = np.sqrt(3)
sqrt5 = np.sqrt(5)


def wind_mouse(
    start_x: Coordinate,
    start_y: Coordinate,
    dest_x: Coordinate,
    dest_y: Coordinate,
    gravity_magnitude: float = 9,
    wind_magnitude: float = 3,
    max_step: float = 15,
    damped_distance: float = 12,
) -> Generator[tuple[Coordinate, Coordinate], None, None]:
    """
    WindMouse algorithm.

    Args:
        start_x: x coordinate of start point.
        start_y: y coordinate of start point.
        dest_x: x coordinate of destination point.
        dest_y: y coordinate of destination point.
        gravity_magnitude: magnitude of the gravitational force
        wind_magnitude: magnitude of the wind force fluctuations
        max_step: maximum step size (velocity clip threshold)
        damped_distance: distance where wind behavior changes from random to damped
    Return:
        Generator which yields current x,y coordinates
    """
    current_x, current_y = start_x, start_y
    velocity_x = velocity_y = wind_x = wind_y = 0
    while (dist := np.hypot(dest_x - start_x, dest_y - start_y)) >= 1:
        wind_magnitude_current = min(wind_magnitude, dist)
        if dist >= damped_distance:
            wind_x = (
                wind_x / sqrt3
                + (2 * np.random.random() - 1) * wind_magnitude_current / sqrt5
            )
            wind_y = (
                wind_y / sqrt3
                + (2 * np.random.random() - 1) * wind_magnitude_current / sqrt5
            )
        else:
            wind_x /= sqrt3
            wind_y /= sqrt3
            if max_step < 3:
                max_step = np.random.random() * 3 + 3
            else:
                max_step /= sqrt5
        velocity_x += wind_x + gravity_magnitude * (dest_x - start_x) / dist
        velocity_y += wind_y + gravity_magnitude * (dest_y - start_y) / dist
        velocity_magnitude = np.hypot(velocity_x, velocity_y)
        if velocity_magnitude > max_step:
            velocity_clip = max_step / 2 + np.random.random() * max_step / 2
            velocity_x = (velocity_x / velocity_magnitude) * velocity_clip
            velocity_y = (velocity_y / velocity_magnitude) * velocity_clip
        start_x += velocity_x
        start_y += velocity_y
        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))
        if current_x != move_x or current_y != move_y:
            current_x, current_y = start_x, start_y
            yield Coordinate(move_x), Coordinate(move_y)


class AbstractMouseController(ABC):
    """
    Abstract Mouse controller class.
    """

    @abstractmethod
    def __init__(
        self,
        start_x: Coordinate | None = None,
        start_y: Coordinate | None = None,
        dest_x: Coordinate | None = None,
        dest_y: Coordinate | None = None,
        *,
        gravity_magnitude: float | None = None,
        wind_magnitude: float | None = None,
        max_step: float | None = None,
        damped_distance: float | None = None,
    ):
        """
        Initialize Mouse controller.

        Args:
            start_x: Initial x-coordinate. If None, defaults to the current
                mouse position upon first use.
            start_y: Initial y-coordinate. If None, defaults to the current
                mouse position upon first use.
            dest_x: Destination x-coordinate. Can be set later if None.
            dest_y: Destination y-coordinate. Can be set later if None.
            gravity_magnitude: See :py:attr: `core.wind_mouse.gravity_magnitude`
            wind_magnitude: See :py:attr: `core.wind_mouse.wind_magnitude`
            max_step: See :py:attr: `core.wind_mouse.max_step`
            damped_distance: See :py:attr: `core.wind_mouse.damped_distance`
        """

    @abstractmethod
    def tick(self) -> bool:
        """
        Move mouse for one point

        Return:
            True if movement was successful, False otherwise (for example there are not more points)
        """

    @abstractmethod
    def move_to_target(self, delay: float, speed: float) -> None:
        """
        Move mouse to target coordinate without yielding (automatically)

        Args:
            delay: Delay between ticks
            speed: Moving speed between 'wind' points.
        """

    @property
    @abstractmethod
    def x(self) -> Coordinate:
        """
        Target x coordinate
        """

    @property
    @abstractmethod
    def y(self) -> Coordinate:
        """
        Target y coordinate
        """

    @property
    @abstractmethod
    def target(self) -> tuple[Coordinate, Coordinate]:
        """
        Synonym for `self.x` and `self.y`
        """
