"""Tests for PyAutoGUI mouse controller."""

from unittest.mock import Mock, patch

# Mock pyautogui at module level to avoid X11 issues
# sys.modules["pyautogui"] = MagicMock()


class TestPyautoguiMouseController:
    """Test PyAutoGUI mouse controller implementation."""

    @patch("windmouse.pyautogui_controller.pyautogui")
    def test_initialization(self, mock_pyautogui):
        """Test PyautoguiMouseController initialization."""
        from windmouse.core import Coordinate
        from windmouse.pyautogui_controller import PyautoguiMouseController

        controller = PyautoguiMouseController(
            start_x=Coordinate(10),
            start_y=Coordinate(20),
            dest_x=Coordinate(100),
            dest_y=Coordinate(200),
        )

        assert controller.start_x == 10
        assert controller.start_y == 20
        assert controller.dest_x == 100
        assert controller.dest_y == 200

    @patch("windmouse.pyautogui_controller.pyautogui")
    def test_tick_moves_mouse(self, mock_pyautogui):
        """Test that tick calls pyautogui.moveTo."""
        from windmouse.core import Coordinate
        from windmouse.pyautogui_controller import PyautoguiMouseController

        mock_pyautogui.position.return_value = Mock(x=0, y=0)

        controller = PyautoguiMouseController(
            start_x=Coordinate(0),
            start_y=Coordinate(0),
            dest_x=Coordinate(50),
            dest_y=Coordinate(50),
        )

        result = controller.tick(step_duration=0.1)

        assert result is True
        assert mock_pyautogui.moveTo.called

    @patch("windmouse.pyautogui_controller.pyautogui")
    def test_get_current_mouse_position(self, mock_pyautogui):
        """Test getting current mouse position."""
        from windmouse.pyautogui_controller import PyautoguiMouseController

        mock_pyautogui.position.return_value = Mock(x=150, y=250)

        controller = PyautoguiMouseController()

        x = controller._get_current_mouse_x()
        y = controller._get_current_mouse_y()

        assert x == 150
        assert y == 250

    @patch("windmouse.pyautogui_controller.pyautogui")
    def test_hold_mouse_button(self, mock_pyautogui):
        """Test holding mouse button."""
        from windmouse.core import HoldMouseButton
        from windmouse.pyautogui_controller import PyautoguiMouseController

        controller = PyautoguiMouseController()

        controller._hold_mouse_button(HoldMouseButton.LEFT)
        mock_pyautogui.mouseDown.assert_called_with(button="left")

        controller._hold_mouse_button(HoldMouseButton.RIGHT)
        mock_pyautogui.mouseDown.assert_called_with(button="right")

    @patch("windmouse.pyautogui_controller.pyautogui")
    def test_release_mouse_button(self, mock_pyautogui):
        """Test releasing mouse button."""
        from windmouse.core import HoldMouseButton
        from windmouse.pyautogui_controller import PyautoguiMouseController

        controller = PyautoguiMouseController()

        controller._release_mouse_button(HoldMouseButton.LEFT)
        mock_pyautogui.mouseUp.assert_called_with(button="left")

        controller._release_mouse_button(HoldMouseButton.RIGHT)
        mock_pyautogui.mouseUp.assert_called_with(button="right")

    @patch("windmouse.pyautogui_controller.pyautogui")
    def test_move_to_target_complete_movement(self, mock_pyautogui):
        """Test complete movement with move_to_target."""
        from windmouse.core import Coordinate
        from windmouse.pyautogui_controller import PyautoguiMouseController

        mock_pyautogui.position.return_value = Mock(x=0, y=0)

        controller = PyautoguiMouseController(
            start_x=Coordinate(0),
            start_y=Coordinate(0),
            dest_x=Coordinate(30),
            dest_y=Coordinate(30),
        )

        controller.move_to_target(tick_delay=0, step_duration=0.01)

        # Should have called moveTo at least once
        assert mock_pyautogui.moveTo.call_count > 0

    @patch("windmouse.pyautogui_controller.pyautogui")
    def test_move_with_drag(self, mock_pyautogui):
        """Test movement with button held (drag)."""
        from windmouse.core import Coordinate, HoldMouseButton
        from windmouse.pyautogui_controller import PyautoguiMouseController

        mock_pyautogui.position.return_value = Mock(x=0, y=0)

        controller = PyautoguiMouseController(
            start_x=Coordinate(0),
            start_y=Coordinate(0),
            dest_x=Coordinate(30),
            dest_y=Coordinate(30),
        )

        controller.move_to_target(
            tick_delay=0, step_duration=0.01, hold_button=HoldMouseButton.LEFT
        )

        # Should have called mouseDown and mouseUp
        assert mock_pyautogui.mouseDown.called
        assert mock_pyautogui.mouseUp.called
