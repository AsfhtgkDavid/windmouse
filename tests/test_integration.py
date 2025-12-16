"""Integration tests for windmouse package."""

from unittest.mock import Mock, patch

from windmouse.ahk_controller import AHKMouseController
from windmouse.core import (
    Coordinate,
    HoldMouseButton,
    wind_mouse,
)


class TestIntegrationPyAutoGUI:
    """Integration tests for PyAutoGUI controller."""

    @patch("windmouse.pyautogui_controller.pyautogui")
    def test_full_movement_workflow(self, mock_pyautogui):
        """Test complete movement workflow with PyAutoGUI."""
        from windmouse.pyautogui_controller import PyautoguiMouseController

        mock_pyautogui.position.return_value = Mock(x=0, y=0)

        controller = PyautoguiMouseController(
            start_x=Coordinate(0),
            start_y=Coordinate(0),
            dest_x=Coordinate(100),
            dest_y=Coordinate(100),
        )

        # Move to target
        controller.move_to_target(tick_delay=0, step_duration=0.01)

        # Verify movement occurred
        assert mock_pyautogui.moveTo.call_count > 0

    @patch("windmouse.pyautogui_controller.pyautogui")
    def test_drag_and_drop_workflow(self, mock_pyautogui):
        """Test drag and drop workflow."""
        from windmouse.pyautogui_controller import PyautoguiMouseController

        mock_pyautogui.position.return_value = Mock(x=50, y=50)

        controller = PyautoguiMouseController(
            start_x=Coordinate(50),
            start_y=Coordinate(50),
            dest_x=Coordinate(150),
            dest_y=Coordinate(150),
        )

        # Perform drag
        controller.move_to_target(
            tick_delay=0, step_duration=0.01, hold_button=HoldMouseButton.LEFT
        )

        # Verify button was held during movement
        assert mock_pyautogui.mouseDown.called
        assert mock_pyautogui.mouseUp.called


class TestIntegrationAHK:
    """Integration tests for AHK controller."""

    def test_full_movement_workflow_ahk(self):
        """Test complete movement workflow with AHK."""

        mock_ahk = Mock()
        mock_ahk.get_mouse_position.return_value = (0, 0)

        controller = AHKMouseController(
            ahk=mock_ahk,
            start_x=Coordinate(0),
            start_y=Coordinate(0),
            dest_x=Coordinate(100),
            dest_y=Coordinate(100),
        )

        # Move to target
        controller.move_to_target(tick_delay=0, step_duration=0.01)

        # Verify movement occurred
        assert mock_ahk.mouse_move.call_count > 0


class TestPathGeneration:
    """Integration tests for path generation quality."""

    def test_path_smoothness(self):
        """Test that generated paths are reasonably smooth."""

        path = list(
            wind_mouse(
                Coordinate(0), Coordinate(0), Coordinate(100), Coordinate(100)
            )
        )

        # Path should have multiple points for smoothness
        assert len(path) > 5

    def test_path_reaches_destination(self):
        """Test that path reliably reaches destination."""

        # Test multiple random destinations
        test_cases = [
            (0, 0, 100, 100),
            (50, 50, 150, 200),
            (-50, -50, 50, 50),
        ]

        for start_x, start_y, dest_x, dest_y in test_cases:
            path = list(
                wind_mouse(
                    Coordinate(start_x),
                    Coordinate(start_y),
                    Coordinate(dest_x),
                    Coordinate(dest_y),
                )
            )

            # Should reach destination
            assert len(path) > 0
            last_x, last_y = path[-1]

            # Within 1 pixel tolerance
            assert abs(last_x - dest_x) <= 1
            assert abs(last_y - dest_y) <= 1
