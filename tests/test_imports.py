"""Tests for package imports and structure."""

import sys
from unittest.mock import MagicMock

import pytest

# Mock pyautogui to avoid X11 issues
sys.modules["pyautogui"] = MagicMock()


class TestPackageImports:
    """Test that package can be imported correctly."""

    def test_import_core_module(self):
        """Test importing core module."""
        import windmouse.core

        assert hasattr(windmouse.core, "wind_mouse")
        assert hasattr(windmouse.core, "AbstractMouseController")
        assert hasattr(windmouse.core, "HoldMouseButton")
        assert hasattr(windmouse.core, "Coordinate")

    def test_import_constants(self):
        """Test importing default constants."""
        from windmouse.core import (DAMPED_DISTANCE_DEFAULT,
                                    GRAVITY_MAGNITUDE_DEFAULT,
                                    MAX_STEP_DEFAULT, WIND_MAGNITUDE_DEFAULT)

        assert GRAVITY_MAGNITUDE_DEFAULT == 9
        assert WIND_MAGNITUDE_DEFAULT == 3
        assert MAX_STEP_DEFAULT == 15
        assert DAMPED_DISTANCE_DEFAULT == 12

    def test_import_enum(self):
        """Test importing HoldMouseButton enum."""
        from windmouse.core import HoldMouseButton

        assert hasattr(HoldMouseButton, "NONE")
        assert hasattr(HoldMouseButton, "LEFT")
        assert hasattr(HoldMouseButton, "RIGHT")
        assert hasattr(HoldMouseButton, "MIDDLE")

    def test_coordinate_type(self):
        """Test Coordinate type."""
        from windmouse.core import Coordinate

        coord = Coordinate(100)
        assert isinstance(coord, int)
        assert coord == 100

    def test_abstract_controller_is_abstract(self):
        """Test that AbstractMouseController cannot be instantiated directly."""
        from windmouse.core import AbstractMouseController

        with pytest.raises(TypeError):
            AbstractMouseController()


class TestModuleStructure:
    """Test module structure and organization."""

    def test_all_modules_importable(self):
        """Test that all main modules can be imported."""
        modules = ["core", "ahk_controller", "pyautogui_controller"]

        for module_name in modules:
            try:
                __import__("windmouse." + module_name)
            except ImportError as e:
                # pyautogui_controller and ahk_controller may fail if dependencies not installed
                if "pyautogui" in str(e) or "ahk" in str(e):
                    pytest.skip(f"Optional dependency not installed: {e}")
                else:
                    raise

    def test_numpy_dependency(self):
        """Test that numpy is available."""
        try:
            import numpy as np

            assert hasattr(np, "sqrt")
            assert hasattr(np, "hypot")
            assert hasattr(np, "random")
        except ImportError:
            pytest.fail("numpy is required but not installed")

    def test_core_functions_callable(self):
        """Test that core functions are callable."""
        from windmouse.core import wind_mouse

        assert callable(wind_mouse)

        # Test that it's a generator function
        import types

        from windmouse.core import Coordinate

        result = wind_mouse(
            Coordinate(0), Coordinate(0), Coordinate(10), Coordinate(10)
        )
        assert isinstance(result, types.GeneratorType)

    def test_controller_abstract_methods(self):
        """Test that AbstractMouseController defines required abstract methods."""
        import inspect

        from windmouse.core import AbstractMouseController

        abstract_methods = {
            "tick",
            "_hold_mouse_button",
            "_release_mouse_button",
            "_get_current_mouse_x",
            "_get_current_mouse_y",
        }

        # Get all abstract methods
        controller_abstracts = set()
        for name, method in inspect.getmembers(AbstractMouseController):
            if (
                hasattr(method, "__isabstractmethod__")
                and method.__isabstractmethod__
            ):
                controller_abstracts.add(name)

        # Check that all required abstract methods are defined
        for method in abstract_methods:
            assert (
                method in controller_abstracts
            ), f"{method} should be abstract"

    def test_public_core_api(self):
        """Test that __all__ is defined in core module."""
        import windmouse.core

        if hasattr(windmouse.core, "__all__"):
            assert "AbstractMouseController" in windmouse.core.__all__
            assert "HoldMouseButton" in windmouse.core.__all__
            assert "Coordinate" in windmouse.core.__all__
        else:
            pytest.fail("__all__ not defined in core module")
