"""Core module for mouse movement using WindMouse algorithm."""

import enum
import time
from abc import ABC, abstractmethod
from typing import Generator, NewType

import numpy as np

GRAVITY_MAGNITUDE_DEFAULT = 9
WIND_MAGNITUDE_DEFAULT = 3
MAX_STEP_DEFAULT = 15
DAMPED_DISTANCE_DEFAULT = 12

Coordinate = NewType("Coordinate", int)

sqrt3 = np.sqrt(3)
sqrt5 = np.sqrt(5)


def wind_mouse(
    start_x: Coordinate,
    start_y: Coordinate,
    dest_x: Coordinate,
    dest_y: Coordinate,
    gravity_magnitude: float = GRAVITY_MAGNITUDE_DEFAULT,
    wind_magnitude: float = WIND_MAGNITUDE_DEFAULT,
    max_step: float = MAX_STEP_DEFAULT,
    damped_distance: float = DAMPED_DISTANCE_DEFAULT,
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


class HoldMouseButton(enum.Enum):
    NONE = "none"
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"


class AbstractMouseController(ABC):
    """
    Abstract Mouse controller class.
    """

    _create_generator: bool

    def __init__(
        self,
        start_x: Coordinate | None = None,
        start_y: Coordinate | None = None,
        dest_x: Coordinate | None = None,
        dest_y: Coordinate | None = None,
        *,
        gravity_magnitude: float = GRAVITY_MAGNITUDE_DEFAULT,
        wind_magnitude: float = WIND_MAGNITUDE_DEFAULT,
        max_step: float = MAX_STEP_DEFAULT,
        damped_distance: float = DAMPED_DISTANCE_DEFAULT,
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
        self._start_x = start_x
        self._start_y = start_y
        self._dest_x = dest_x
        self._dest_y = dest_y
        self._gravity_magnitude = gravity_magnitude
        self._wind_magnitude = wind_magnitude
        self._max_step = max_step
        self._damped_distance = damped_distance

        self._create_generator = True

    def move_to_target(
        self,
        tick_delay: float = 0,
        step_duration: float = 0.1,
        hold_button: HoldMouseButton = HoldMouseButton.NONE,
    ) -> None:
        """
        Moves the mouse to the target coordinates using a generated path.

        Args:
            tick_delay: Sleep time between movement updates (in seconds).
            step_duration: Duration of each movement step.
                           Lower values result in faster overall movement.
            hold_button: Which mouse button to hold down during movement (for drag & drop).
        """
        if hold_button != HoldMouseButton.NONE:
            self._hold_mouse_button(hold_button)

        self._create_generator = True

        while self.tick(step_duration):
            time.sleep(tick_delay)

        if hold_button != HoldMouseButton.NONE:
            self._release_mouse_button(hold_button)

    @property
    def start_x(self) -> Coordinate | None:
        """
        Start x coordinate
        None means current mouse x coordinate
        """
        return self._start_x

    @start_x.setter
    def start_x(self, value: Coordinate | None) -> None:
        self._start_x = value
        self._create_generator = True

    @property
    def start_y(self) -> Coordinate | None:
        """
        Start y coordinate
        None means current mouse y coordinate
        """
        return self._start_y

    @start_y.setter
    def start_y(self, value: Coordinate | None) -> None:
        self._start_y = value
        self._create_generator = True

    @property
    def start_position(self) -> tuple[Coordinate | None, Coordinate | None]:
        """
        Synonym for `self.start_x`, `self.start_y`
        """
        return self.start_x, self.start_y

    @start_position.setter
    def start_position(self, value: tuple[Coordinate, Coordinate]) -> None:
        self.start_x, self.start_y = value

    @property
    def dest_x(self) -> Coordinate | None:
        """
        Destination x coordinate
        """
        return self._dest_x

    @dest_x.setter
    def dest_x(self, value: Coordinate) -> None:
        self._dest_x = value
        self._create_generator = True

    @property
    def dest_y(self) -> Coordinate | None:
        """
        Destination y coordinate
        """
        return self._dest_y

    @dest_y.setter
    def dest_y(self, value: Coordinate) -> None:
        self._dest_y = value
        self._create_generator = True

    @property
    def dest_position(self) -> tuple[Coordinate | None, Coordinate | None]:
        """
        Synonym for `self.dest_x`, `self.dest_y`
        """
        return self.dest_x, self.dest_y

    @dest_position.setter
    def dest_position(self, value: tuple[Coordinate, Coordinate]) -> None:
        self.dest_x, self.dest_y = value

    def _recreate_generator(self) -> None:
        """
        Recreate generator if needed

        If start coordinates are not set, get current mouse coordinates.

        Raises:
            ValueError: If destination coordinates are not set
        """
        if not self._create_generator:
            return
        self._start_x = self._start_x or self._get_current_mouse_x()
        self._start_y = self._start_y or self._get_current_mouse_y()

        if self._dest_x is None or self._dest_y is None:
            raise ValueError(
                "Destination coordinates must be set before creating generator."
            )

        self._generator = (  # pylint: disable=attribute-defined-outside-init
            wind_mouse(
                self._start_x,
                self._start_y,
                self._dest_x,
                self._dest_y,
                self._gravity_magnitude,
                self._wind_magnitude,
                self._max_step,
                self._damped_distance,
            )
        )
        self._create_generator = False

    def _get_next_point(self) -> tuple[Coordinate, Coordinate] | None:
        """
        Get next point from generator

        If needed, recreate generator.

        Returns:
            Tuple of x, y coordinates or None if generator is exhausted
        """
        self._recreate_generator()
        try:
            return next(self._generator)
        except StopIteration:
            return None

    @abstractmethod
    def tick(self, step_duration: float = 0.1) -> bool:
        """
        Advances the mouse cursor to the next point in the trajectory.

        This method is designed to be called iteratively in a loop.
        It moves the mouse one step towards the current target.

        Args:
            step_duration: The duration of this single movement step (in seconds).
                           Used to control the overall speed of the gesture.

        Return:
            True if the cursor moved to a new point (movement continues).
            False if the target has been reached or no path remains.
        """

    @abstractmethod
    def _hold_mouse_button(self, button: HoldMouseButton) -> None:
        """
        Hold left mouse button

        Args:
            button: Which mouse button to hold down
        """

    @abstractmethod
    def _release_mouse_button(self, button: HoldMouseButton) -> None:
        """
        Release left mouse button

        Args:
            button: Which mouse button to release
        """

    @abstractmethod
    def _get_current_mouse_x(self) -> Coordinate:
        """
        Get current mouse x coordinate
        """

    @abstractmethod
    def _get_current_mouse_y(self) -> Coordinate:
        """
        Get current mouse y coordinate
        """


__all__ = [
    "AbstractMouseController",
    "HoldMouseButton",
    "Coordinate",
    "GRAVITY_MAGNITUDE_DEFAULT",
    "WIND_MAGNITUDE_DEFAULT",
    "MAX_STEP_DEFAULT",
    "DAMPED_DISTANCE_DEFAULT",
    "wind_mouse",
]
