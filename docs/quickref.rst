Quick Reference
===============

This page provides a quick reference for the most common WindMouse operations.

Installation
------------

.. code-block:: bash

   # Basic installation
   pip install windmouse

   # With PyAutoGUI (recommended)
   pip install windmouse[pyautogui]

   # With AutoHotkey (Windows only)
   pip install windmouse[ahk]

Basic Movement
--------------

PyAutoGUI (Cross-platform)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   mouse = PyautoguiMouseController()
   mouse.dest_position = (Coordinate(800), Coordinate(600))
   mouse.move_to_target()

AutoHotkey (Windows)
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from ahk import AHK
   from windmouse.ahk_controller import AHKMouseController
   from windmouse import Coordinate

   ahk = AHK()
   mouse = AHKMouseController(ahk)
   mouse.dest_position = (Coordinate(800), Coordinate(600))
   mouse.move_to_target()

Common Parameters
-----------------

Physics Parameters (Constructor)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   mouse = PyautoguiMouseController(
       gravity_magnitude=9,    # Attraction strength (default: 9)
       wind_magnitude=3,       # Curvature amount (default: 3)
       max_step=15,            # Maximum speed (default: 15)
       damped_distance=12      # Slowdown distance (default: 12)
   )

Movement Parameters (move_to_target)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   mouse.move_to_target(
       tick_delay=0.005,       # Delay between steps (seconds)
       step_duration=0.1,      # Duration per step (seconds)
       hold_button=HoldMouseButton.NONE  # Button to hold
   )

Preset Configurations
---------------------

Fast Movement
^^^^^^^^^^^^^

.. code-block:: python

   mouse = PyautoguiMouseController(
       gravity_magnitude=12,
       wind_magnitude=1,
       max_step=20
   )
   mouse.move_to_target(tick_delay=0, step_duration=0.05)

Natural Movement (Default)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   mouse = PyautoguiMouseController()  # Uses defaults
   mouse.move_to_target(tick_delay=0.005, step_duration=0.1)

Curved Movement
^^^^^^^^^^^^^^^

.. code-block:: python

   mouse = PyautoguiMouseController(
       gravity_magnitude=6,
       wind_magnitude=7,
       max_step=10
   )
   mouse.move_to_target()

Slow, Deliberate Movement
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   mouse = PyautoguiMouseController(
       max_step=8,
       damped_distance=25
   )
   mouse.move_to_target(tick_delay=0.01, step_duration=0.2)

Common Operations
-----------------

Drag and Drop
^^^^^^^^^^^^^

.. code-block:: python

   from windmouse import HoldMouseButton

   # Move to source
   mouse.dest_position = (Coordinate(300), Coordinate(300))
   mouse.move_to_target()

   # Drag to destination
   mouse.dest_position = (Coordinate(700), Coordinate(500))
   mouse.move_to_target(hold_button=HoldMouseButton.LEFT)

Sequential Movements
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   waypoints = [
       (Coordinate(200), Coordinate(200)),
       (Coordinate(600), Coordinate(200)),
       (Coordinate(600), Coordinate(600)),
   ]

   for dest in waypoints:
       mouse.dest_position = dest
       mouse.move_to_target()

Manual Control
^^^^^^^^^^^^^^

.. code-block:: python

   import time

   mouse.dest_position = (Coordinate(800), Coordinate(600))

   while mouse.tick(step_duration=0.1):
       time.sleep(0.01)
       # Custom logic here

Random Offset
^^^^^^^^^^^^^

.. code-block:: python

   import random

   base_x, base_y = 800, 600
   offset = 5

   mouse.dest_position = (
       Coordinate(base_x + random.randint(-offset, offset)),
       Coordinate(base_y + random.randint(-offset, offset))
   )
   mouse.move_to_target()

HoldMouseButton Values
-----------------------

.. code-block:: python

   from windmouse import HoldMouseButton

   HoldMouseButton.NONE    # No button (default)
   HoldMouseButton.LEFT    # Left mouse button
   HoldMouseButton.RIGHT   # Right mouse button
   HoldMouseButton.MIDDLE  # Middle mouse button

Default Constants
-----------------

.. code-block:: python

   from windmouse.core import (
       GRAVITY_MAGNITUDE_DEFAULT,  # 9
       WIND_MAGNITUDE_DEFAULT,     # 3
       MAX_STEP_DEFAULT,           # 15
       DAMPED_DISTANCE_DEFAULT     # 12
   )

Error Handling
--------------

.. code-block:: python

   try:
       mouse.dest_position = (Coordinate(800), Coordinate(600))
       mouse.move_to_target()
   except ValueError as e:
       print(f"Invalid configuration: {e}")
   except ImportError as e:
       print(f"Missing dependency: {e}")

Type Safety
-----------

.. code-block:: python

   from windmouse import Coordinate

   # Correct usage
   x = Coordinate(800)
   y = Coordinate(600)
   mouse.dest_position = (x, y)

   # Type checker will complain (good!)
   # mouse.dest_position = (800, 600)

See Also
--------

* :doc:`installation` - Detailed installation instructions
* :doc:`usage` - Comprehensive usage guide with examples
* :doc:`algorithm` - Algorithm explanation and mathematics
* :doc:`api` - Complete API reference

