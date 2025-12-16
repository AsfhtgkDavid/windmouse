"""Tests for core windmouse functionality."""

import numpy as np
import pytest

from windmouse.core import (AbstractMouseController, Coordinate,
                            HoldMouseButton, wind_mouse)


class TestWindMouse:
    """Test the wind_mouse algorithm."""

    def test_wind_mouse_basic_movement(self):
        """Test that wind_mouse generates a path from start to destination."""
        start_x, start_y = Coordinate(0), Coordinate(0)
        dest_x, dest_y = Coordinate(100), Coordinate(100)

        path = list(wind_mouse(start_x, start_y, dest_x, dest_y))

        # Path should not be empty
        assert len(path) > 0

        # Last point should be close to destination
        last_x, last_y = path[-1]
        assert abs(last_x - dest_x) <= 1
        assert abs(last_y - dest_y) <= 1

    def test_wind_mouse_returns_coordinates(self):
        """Test that wind_mouse returns valid Coordinate types."""
        path = list(
            wind_mouse(
                Coordinate(0), Coordinate(0), Coordinate(50), Coordinate(50)
            )
        )

        for x, y in path:
            assert isinstance(x, int)
            assert isinstance(y, int)

    def test_wind_mouse_short_distance(self):
        """Test wind_mouse with very short distance."""
        # Very short distance (less than 1 pixel) should generate minimal path
        path = list(
            wind_mouse(
                Coordinate(10), Coordinate(10), Coordinate(10), Coordinate(10)
            )
        )

        # Should complete without error
        assert isinstance(path, list)

    def test_wind_mouse_custom_parameters(self):
        """Test wind_mouse with custom parameters."""
        path = list(
            wind_mouse(
                Coordinate(0),
                Coordinate(0),
                Coordinate(100),
                Coordinate(100),
                gravity_magnitude=15,
                wind_magnitude=5,
                max_step=20,
                damped_distance=15,
            )
        )

        assert len(path) > 0
        last_x, last_y = path[-1]
        assert abs(last_x - 100) <= 1
        assert abs(last_y - 100) <= 1

    def test_wind_mouse_negative_coordinates(self):
        """Test wind_mouse with negative coordinates."""
        path = list(
            wind_mouse(
                Coordinate(-50),
                Coordinate(-50),
                Coordinate(50),
                Coordinate(50),
            )
        )

        assert len(path) > 0

    def test_wind_mouse_determinism(self):
        """Test that wind_mouse produces different paths (non-deterministic)."""
        np.random.seed(42)
        path1 = list(
            wind_mouse(
                Coordinate(0), Coordinate(0), Coordinate(100), Coordinate(100)
            )
        )

        np.random.seed(43)
        path2 = list(
            wind_mouse(
                Coordinate(0), Coordinate(0), Coordinate(100), Coordinate(100)
            )
        )

        # Paths should be different (randomness)
        assert path1 != path2

    def test_wind_mouse_horizontal_movement(self):
        """Test wind_mouse with purely horizontal movement."""
        path = list(
            wind_mouse(
                Coordinate(0), Coordinate(50), Coordinate(100), Coordinate(50)
            )
        )

        assert len(path) > 0
        last_x, last_y = path[-1]
        assert abs(last_x - 100) <= 1

    def test_wind_mouse_vertical_movement(self):
        """Test wind_mouse with purely vertical movement."""
        path = list(
            wind_mouse(
                Coordinate(50), Coordinate(0), Coordinate(50), Coordinate(100)
            )
        )

        assert len(path) > 0
        last_x, last_y = path[-1]
        assert abs(last_y - 100) <= 1


class TestHoldMouseButton:
    """Test HoldMouseButton enum."""

    def test_hold_mouse_button_values(self):
        """Test that HoldMouseButton has expected values."""
        assert HoldMouseButton.NONE.value == "none"
        assert HoldMouseButton.LEFT.value == "left"
        assert HoldMouseButton.RIGHT.value == "right"
        assert HoldMouseButton.MIDDLE.value == "middle"


class MockMouseController(AbstractMouseController):
    """Mock implementation of AbstractMouseController for testing."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mouse_x = 0
        self.mouse_y = 0
        self.held_button = None
        self.released_button = None
        self.move_calls = []

    def tick(self, step_duration: float = 0.1) -> bool:
        coords = self._get_next_point()
        if coords is None:
            return False
        self.mouse_x, self.mouse_y = coords
        self.move_calls.append((coords[0], coords[1], step_duration))
        return True

    def _hold_mouse_button(self, button: HoldMouseButton) -> None:
        self.held_button = button

    def _release_mouse_button(self, button: HoldMouseButton) -> None:
        self.released_button = button

    def _get_current_mouse_x(self) -> Coordinate:
        return Coordinate(self.mouse_x)

    def _get_current_mouse_y(self) -> Coordinate:
        return Coordinate(self.mouse_y)


class TestAbstractMouseController:
    """Test AbstractMouseController functionality."""

    def test_initialization_with_all_parameters(self):
        """Test controller initialization with all parameters."""
        controller = MockMouseController(
            start_x=Coordinate(10),
            start_y=Coordinate(20),
            dest_x=Coordinate(100),
            dest_y=Coordinate(200),
            gravity_magnitude=15,
            wind_magnitude=5,
            max_step=20,
            damped_distance=15,
        )

        assert controller.start_x == 10
        assert controller.start_y == 20
        assert controller.dest_x == 100
        assert controller.dest_y == 200

    def test_initialization_with_defaults(self):
        """Test controller initialization with default parameters."""
        controller = MockMouseController()

        assert controller.start_x is None
        assert controller.start_y is None
        assert controller.dest_x is None
        assert controller.dest_y is None

    def test_start_position_property(self):
        """Test start_position getter and setter."""
        controller = MockMouseController()
        controller.start_position = (Coordinate(50), Coordinate(60))

        assert controller.start_x == 50
        assert controller.start_y == 60
        assert controller.start_position == (50, 60)

    def test_dest_position_property(self):
        """Test dest_position getter and setter."""
        controller = MockMouseController()
        controller.dest_position = (Coordinate(150), Coordinate(160))

        assert controller.dest_x == 150
        assert controller.dest_y == 160
        assert controller.dest_position == (150, 160)

    def test_move_to_target_basic(self):
        """Test move_to_target with basic parameters."""
        controller = MockMouseController(
            start_x=Coordinate(0),
            start_y=Coordinate(0),
            dest_x=Coordinate(50),
            dest_y=Coordinate(50),
        )

        controller.move_to_target(tick_delay=0, step_duration=0.1)

        # Should have moved
        assert len(controller.move_calls) > 0
        # Should not have held any button
        assert controller.held_button is None

    def test_move_to_target_with_hold_button(self):
        """Test move_to_target with button hold."""
        controller = MockMouseController(
            start_x=Coordinate(0),
            start_y=Coordinate(0),
            dest_x=Coordinate(50),
            dest_y=Coordinate(50),
        )

        controller.move_to_target(
            tick_delay=0, step_duration=0.1, hold_button=HoldMouseButton.LEFT
        )

        # Should have held and released left button
        assert controller.held_button == HoldMouseButton.LEFT
        assert controller.released_button == HoldMouseButton.LEFT

    def test_tick_returns_true_while_moving(self):
        """Test that tick returns True while movement continues."""
        controller = MockMouseController(
            start_x=Coordinate(0),
            start_y=Coordinate(0),
            dest_x=Coordinate(100),
            dest_y=Coordinate(100),
        )

        # First tick should return True
        assert controller.tick() is True

    def test_tick_returns_false_when_complete(self):
        """Test that tick returns False when movement is complete."""
        controller = MockMouseController(
            start_x=Coordinate(0),
            start_y=Coordinate(0),
            dest_x=Coordinate(10),
            dest_y=Coordinate(10),
        )

        # Exhaust all moves
        while controller.tick():
            pass

        # Next tick should return False
        assert controller.tick() is False

    def test_raises_error_without_destination(self):
        """Test that error is raised if destination is not set."""
        controller = MockMouseController(
            start_x=Coordinate(0), start_y=Coordinate(0)
        )

        with pytest.raises(
            ValueError, match="Destination coordinates must be set"
        ):
            controller.tick()

    def test_uses_current_position_if_start_not_set(self):
        """Test that controller uses current position if start not set."""
        controller = MockMouseController(
            dest_x=Coordinate(100), dest_y=Coordinate(100)
        )
        controller.mouse_x = 50
        controller.mouse_y = 50

        # Should not raise error
        result = controller.tick()
        assert result is True

    def test_changing_destination_recreates_generator(self):
        """Test that changing destination recreates the path generator."""
        controller = MockMouseController(
            start_x=Coordinate(0),
            start_y=Coordinate(0),
            dest_x=Coordinate(50),
            dest_y=Coordinate(50),
        )

        # Start moving
        controller.tick()
        first_call = controller.move_calls[0]

        # Change destination
        controller.dest_x = Coordinate(100)

        # Continue moving
        controller.tick()

        # Should have more calls
        assert len(controller.move_calls) >= 2

    def test_property_setters_trigger_regeneration(self):
        """Test that property setters trigger path regeneration."""
        controller = MockMouseController(
            start_x=Coordinate(0),
            start_y=Coordinate(0),
            dest_x=Coordinate(50),
            dest_y=Coordinate(50),
        )

        # Modifying start should trigger regeneration
        controller.start_x = Coordinate(10)
        assert controller._create_generator is True

        controller._create_generator = False
        controller.start_y = Coordinate(10)
        assert controller._create_generator is True

        controller._create_generator = False
        controller.dest_x = Coordinate(60)
        assert controller._create_generator is True

        controller._create_generator = False
        controller.dest_y = Coordinate(60)
        assert controller._create_generator is True
