Examples
========

This page provides practical code examples for common WindMouse usage patterns.

Basic Movement
--------------

PyAutoGUI (Cross-Platform)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   # Create controller with default parameters
   mouse = PyautoguiMouseController()

   # Move to target
   mouse.dest_position = (Coordinate(800), Coordinate(600))
   mouse.move_to_target()

AutoHotkey (Windows)
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from ahk import AHK
   from windmouse.ahk_controller import AHKMouseController
   from windmouse import Coordinate

   # Initialize AHK
   ahk = AHK()

   # Create controller
   mouse = AHKMouseController(ahk)

   # Move to target
   mouse.dest_position = (Coordinate(1920), Coordinate(1080))
   mouse.move_to_target()

Custom Physics Parameters
--------------------------

.. code-block:: python

   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   # Customize physics parameters
   mouse = PyautoguiMouseController(
       gravity_magnitude=9,    # Attraction strength
       wind_magnitude=3,       # Curvature amount
       max_step=15,            # Maximum speed
       damped_distance=12      # Slowdown distance
   )

   mouse.dest_position = (Coordinate(800), Coordinate(600))
   mouse.move_to_target()

Changing Destination On-The-Fly
--------------------------------

You can dynamically change the destination **during movement** by setting a new target between ticks.
When you change ``dest_position``, the algorithm recalculates the path and smoothly redirects to the new target.

.. code-block:: python

   import time
   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   mouse = PyautoguiMouseController()

   # Start with initial target
   mouse.dest_position = (Coordinate(800), Coordinate(600))

   step_count = 0
   while mouse.tick(step_duration=0.1):
       step_count += 1
       time.sleep(0.01)

       # Change destination after 10 steps
       if step_count == 10:
           print("Redirecting to new target!")
           mouse.dest_position = (Coordinate(400), Coordinate(300))

       # Or change based on external condition
       # if target_moved:
       #     mouse.dest_position = get_new_target_position()

       # Can stop early if needed
       if should_abort:
           break

   print(f"Movement completed in {step_count} steps")

**Note:** Setting a new ``dest_position`` regenerates the internal path generator,
so the mouse will smoothly transition to the new target from its current position.

This technique is useful for:

* **Reactive movements** - responding to changing targets
* **Following moving objects** - tracking dynamic positions
* **Adaptive behavior** - adjusting path based on conditions
* **Emergency stops** - breaking out of movement early

Drag and Drop
-------------

.. code-block:: python

   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate, HoldMouseButton

   mouse = PyautoguiMouseController()

   # Move to source position
   mouse.dest_position = (Coordinate(300), Coordinate(300))
   mouse.move_to_target()

   # Drag to destination with left button held
   mouse.dest_position = (Coordinate(700), Coordinate(500))
   mouse.move_to_target(hold_button=HoldMouseButton.LEFT)

Sequential Movements
--------------------

.. code-block:: python

   import time
   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   mouse = PyautoguiMouseController()

   # Define waypoints
   waypoints = [
       (Coordinate(200), Coordinate(200)),
       (Coordinate(600), Coordinate(200)),
       (Coordinate(600), Coordinate(600)),
       (Coordinate(200), Coordinate(600)),
   ]

   # Move through each waypoint
   for dest in waypoints:
       mouse.dest_position = dest
       mouse.move_to_target(tick_delay=0.005)
       time.sleep(0.3)  # Pause at each waypoint

Movement Speed Control
----------------------

Fast Movement
^^^^^^^^^^^^^

.. code-block:: python

   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   mouse = PyautoguiMouseController(
       gravity_magnitude=12,   # Strong attraction
       wind_magnitude=1,       # Minimal curvature
       max_step=20             # High speed
   )

   mouse.dest_position = (Coordinate(800), Coordinate(600))
   mouse.move_to_target(tick_delay=0, step_duration=0.05)

Natural Movement
^^^^^^^^^^^^^^^^

.. code-block:: python

   mouse = PyautoguiMouseController()  # Default parameters

   mouse.dest_position = (Coordinate(800), Coordinate(600))
   mouse.move_to_target(tick_delay=0.005, step_duration=0.1)

Slow Movement
^^^^^^^^^^^^^

.. code-block:: python

   mouse = PyautoguiMouseController(
       max_step=8,             # Lower speed
       damped_distance=25      # Early slowdown
   )

   mouse.dest_position = (Coordinate(800), Coordinate(600))
   mouse.move_to_target(tick_delay=0.01, step_duration=0.2)

Manual Control with Tick
-------------------------

.. code-block:: python

   import time
   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   mouse = PyautoguiMouseController()
   mouse.dest_position = (Coordinate(800), Coordinate(600))

   # Manual control loop
   while mouse.tick(step_duration=0.1):
       time.sleep(0.01)

       # Perform custom logic between steps
       current_pos = pyautogui.position()
       print(f"Current position: {current_pos}")

       # Can break early based on conditions
       if some_condition:
           break

Error Handling
--------------

.. code-block:: python

   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   try:
       mouse = PyautoguiMouseController()
       mouse.dest_position = (Coordinate(800), Coordinate(600))
       mouse.move_to_target()
   except ValueError as e:
       print(f"Configuration error: {e}")
   except ImportError as e:
       print(f"Missing dependency: {e}")
   except Exception as e:
       print(f"Unexpected error: {e}")

Random Offset for Natural Variation
------------------------------------

.. code-block:: python

   import random
   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   def click_with_offset(base_x: int, base_y: int, offset: int = 5):
       """Click with slight random offset for more natural behavior."""
       mouse = PyautoguiMouseController()

       # Add random offset
       dest_x = Coordinate(base_x + random.randint(-offset, offset))
       dest_y = Coordinate(base_y + random.randint(-offset, offset))

       mouse.dest_position = (dest_x, dest_y)
       mouse.move_to_target(tick_delay=0.003)

   # Usage
   click_with_offset(800, 600)

Reusing Controllers
-------------------

.. code-block:: python

   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   # Create once
   mouse = PyautoguiMouseController()

   # Reuse for multiple movements
   destinations = [
       (Coordinate(100), Coordinate(100)),
       (Coordinate(500), Coordinate(500)),
       (Coordinate(900), Coordinate(300)),
   ]

   for dest in destinations:
       mouse.dest_position = dest
       mouse.move_to_target()

Resource Management (AHK)
-------------------------

.. code-block:: python

   from ahk import AHK
   from windmouse.ahk_controller import AHKMouseController
   from windmouse import Coordinate

   # Create AHK instance once
   ahk = AHK()

   # Reuse for multiple controllers
   mouse1 = AHKMouseController(ahk)
   mouse2 = AHKMouseController(ahk)

   # Use different controllers
   mouse1.dest_position = (Coordinate(100), Coordinate(100))
   mouse1.move_to_target()

   mouse2.dest_position = (Coordinate(500), Coordinate(500))
   mouse2.move_to_target()

See Also
--------

* :doc:`usage` - Comprehensive usage guide with explanations
* :doc:`api` - API reference documentation
* :doc:`quickref` - Quick reference for common operations
* :doc:`algorithm` - Algorithm explanation and parameter effects

