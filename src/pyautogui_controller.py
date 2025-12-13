from core import AbstractMouseController, HoldMouseButton
from core import Coordinate

try:
    import pyautogui
except ImportError:
    raise OSError("You need install windmouse[pyautogui]")


class PyautoguiMouseController(AbstractMouseController):
    """
    Mouse controller implementation using pyautogui.
    """

    def tick(self, step_duration: float = 0.1) -> bool:
        coords = self._get_next_point()
        if coords is None:
            return False
        pyautogui.moveTo(coords[0], coords[1], duration=step_duration)
        return True

    def _get_current_mouse_x(self) -> Coordinate:
        return Coordinate(pyautogui.position().x)

    def _get_current_mouse_y(self) -> Coordinate:
        return Coordinate(pyautogui.position().y)

    def _hold_mouse_button(self, button: HoldMouseButton) -> None:
        match button:
            case HoldMouseButton.LEFT:
                pyautogui.mouseDown(button="left")
            case HoldMouseButton.RIGHT:
                pyautogui.mouseDown(button="right")
            case HoldMouseButton.MIDDLE:
                pyautogui.mouseDown(button="middle")

    def _release_mouse_button(self, button: HoldMouseButton) -> None:
        match button:
            case HoldMouseButton.LEFT:
                pyautogui.mouseUp(button="left")
            case HoldMouseButton.RIGHT:
                pyautogui.mouseUp(button="right")
            case HoldMouseButton.MIDDLE:
                pyautogui.mouseUp(button="middle")
