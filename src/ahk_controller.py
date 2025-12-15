import sys
from typing import Any

from .core import (
    AbstractMouseController,
    HoldMouseButton,
    Coordinate,
    GRAVITY_MAGNITUDE_DEFAULT,
    WIND_MAGNITUDE_DEFAULT,
    MAX_STEP_DEFAULT,
    DAMPED_DISTANCE_DEFAULT,
)

if sys.platform == "win32":
    try:
        from ahk import AHK
    except ImportError:
        raise OSError("You need install windmouse[ahk] extra to use ahk")
else:
    raise OSError("Ahk available only for Windows")


class AHKMouseController(AbstractMouseController):
    def __init__(
        self,
        ahk: AHK[Any],
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
        self._ahk = ahk
        super().__init__(
            start_x,
            start_y,
            dest_x,
            dest_y,
            gravity_magnitude=gravity_magnitude,
            wind_magnitude=wind_magnitude,
            max_step=max_step,
            damped_distance=damped_distance,
        )

    def tick(self, step_duration: float = 2) -> bool:
        coords = self._get_next_point()
        if coords is None:
            return False
        self._ahk.mouse_move(coords[0], coords[1], speed=step_duration, coord_mode="Screen")  # type: ignore[call-overload]
        return True

    def _get_current_mouse_x(self) -> Coordinate:
        return Coordinate(self._ahk.get_mouse_position(coord_mode="Screen")[0])

    def _get_current_mouse_y(self) -> Coordinate:
        return Coordinate(self._ahk.get_mouse_position(coord_mode="Screen")[1])

    def _hold_mouse_button(self, button: HoldMouseButton) -> None:
        self._ahk.click(button=button.value, direction="D")

    def _release_mouse_button(self, button: HoldMouseButton) -> None:
        self._ahk.click(button=button.value, direction="U")
