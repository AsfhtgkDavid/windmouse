"""Tests for AHK mouse controller."""

from unittest.mock import Mock

from windmouse.ahk_controller import AHKMouseController
from windmouse.core import Coordinate, HoldMouseButton


class TestAHKMouseController:
    """Test AHK mouse controller implementation."""

    def test_initialization(self):
        """Test AHKMouseController initialization."""

        mock_ahk = Mock()
        controller = AHKMouseController(
            ahk=mock_ahk,
            start_x=Coordinate(10),
            start_y=Coordinate(20),
            dest_x=Coordinate(100),
            dest_y=Coordinate(200),
        )

        assert controller.start_x == 10
        assert controller.start_y == 20
        assert controller.dest_x == 100
        assert controller.dest_y == 200
        assert controller._ahk == mock_ahk

    def test_tick_moves_mouse(self):
        """Test that tick calls AHK mouse_move."""

        mock_ahk = Mock()
        mock_ahk.get_mouse_position.return_value = (0, 0)

        controller = AHKMouseController(
            ahk=mock_ahk,
            start_x=Coordinate(0),
            start_y=Coordinate(0),
            dest_x=Coordinate(50),
            dest_y=Coordinate(50),
        )

        result = controller.tick(step_duration=2)

        assert result is True
        assert mock_ahk.mouse_move.called
        # Verify it was called with coord_mode="Screen"
        call_args = mock_ahk.mouse_move.call_args
        assert call_args[1]["coord_mode"] == "Screen"

    def test_get_current_mouse_position(self):
        """Test getting current mouse position."""

        mock_ahk = Mock()
        mock_ahk.get_mouse_position.return_value = (150, 250)

        controller = AHKMouseController(ahk=mock_ahk)

        x = controller._get_current_mouse_x()
        y = controller._get_current_mouse_y()

        assert x == 150
        assert y == 250
        # Verify coord_mode was passed
        assert mock_ahk.get_mouse_position.call_count == 2
        for call in mock_ahk.get_mouse_position.call_args_list:
            assert call[1]["coord_mode"] == "Screen"

    def test_hold_mouse_button(self):
        """Test holding mouse button."""

        mock_ahk = Mock()
        controller = AHKMouseController(ahk=mock_ahk)

        controller._hold_mouse_button(HoldMouseButton.LEFT)
        mock_ahk.click.assert_called_with(button="left", direction="D")

        controller._hold_mouse_button(HoldMouseButton.RIGHT)
        mock_ahk.click.assert_called_with(button="right", direction="D")

    def test_release_mouse_button(self):
        """Test releasing mouse button."""

        mock_ahk = Mock()
        controller = AHKMouseController(ahk=mock_ahk)

        controller._release_mouse_button(HoldMouseButton.LEFT)
        mock_ahk.click.assert_called_with(button="left", direction="U")

        controller._release_mouse_button(HoldMouseButton.RIGHT)
        mock_ahk.click.assert_called_with(button="right", direction="U")

    def test_move_to_target_complete_movement(self):
        """Test complete movement with move_to_target."""

        mock_ahk = Mock()
        mock_ahk.get_mouse_position.return_value = (0, 0)

        controller = AHKMouseController(
            ahk=mock_ahk,
            start_x=Coordinate(0),
            start_y=Coordinate(0),
            dest_x=Coordinate(30),
            dest_y=Coordinate(30),
        )

        controller.move_to_target(tick_delay=0, step_duration=0.01)

        # Should have called mouse_move at least once
        assert mock_ahk.mouse_move.call_count > 0

    def test_move_with_drag(self):
        """Test movement with button held (drag)."""

        mock_ahk = Mock()
        mock_ahk.get_mouse_position.return_value = (0, 0)

        controller = AHKMouseController(
            ahk=mock_ahk,
            start_x=Coordinate(0),
            start_y=Coordinate(0),
            dest_x=Coordinate(30),
            dest_y=Coordinate(30),
        )

        controller.move_to_target(
            tick_delay=0, step_duration=0.01, hold_button=HoldMouseButton.LEFT
        )

        # Should have called click with direction D and U
        click_calls = [call for call in mock_ahk.click.call_args_list]
        assert len(click_calls) >= 2

        # Check for mouseDown and mouseUp
        directions = [call[1]["direction"] for call in click_calls]
        assert "D" in directions
        assert "U" in directions

    def test_default_step_duration(self):
        """Test that default step_duration is used for AHK."""

        mock_ahk = Mock()
        mock_ahk.get_mouse_position.return_value = (0, 0)

        controller = AHKMouseController(
            ahk=mock_ahk,
            start_x=Coordinate(0),
            start_y=Coordinate(0),
            dest_x=Coordinate(50),
            dest_y=Coordinate(50),
        )

        # Call tick with default (which is 2 for AHK)
        controller.tick()

        # Verify speed parameter was passed
        call_args = mock_ahk.mouse_move.call_args
        assert "speed" in call_args[1]
