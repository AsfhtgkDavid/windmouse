Usage Guide
===========

This guide provides comprehensive examples and explanations for using WindMouse in your projects.

Basic Usage
-----------

PyAutoGUI Backend (Cross-Platform)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The PyAutoGUI backend is the recommended choice for cross-platform projects:

.. code-block:: python

   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   # Create a controller instance
   mouse = PyautoguiMouseController()

   # Set the destination coordinates
   mouse.dest_position = (Coordinate(800), Coordinate(600))

   # Move to the target with default settings
   mouse.move_to_target()

AutoHotkey Backend (Windows)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For Windows-specific projects, the AHK backend may provide smoother movements:

.. code-block:: python

   from ahk import AHK
   from windmouse.ahk_controller import AHKMouseController
   from windmouse import Coordinate

   # Initialize AHK
   ahk = AHK()

   # Create a controller instance with AHK
   mouse = AHKMouseController(ahk)

   # Set destination and move
   mouse.dest_position = (Coordinate(1920), Coordinate(1080))
   mouse.move_to_target()

Understanding Movement Parameters
----------------------------------

The ``move_to_target()`` method accepts several parameters that control the movement behavior:

tick_delay
^^^^^^^^^^

**Type**: ``float`` (default: ``0``)

**Description**: Sleep time in seconds between each movement step. Higher values slow down the overall movement.

**Use Cases**:

* **0** (default): Maximum speed, no delay
* **0.001-0.01**: Natural speed for most applications
* **0.05-0.1**: Slower, more deliberate movements

**Example**:

.. code-block:: python

   # Fast movement (no delay)
   mouse.move_to_target(tick_delay=0)

   # Natural speed
   mouse.move_to_target(tick_delay=0.005)

   # Slow, deliberate movement
   mouse.move_to_target(tick_delay=0.1)

step_duration
^^^^^^^^^^^^^

**Type**: ``float`` (default: ``0.1``)

**Description**: Duration in seconds for each individual movement step. This affects the smoothness and speed of the transition between points.

* **Lower values** (0.01-0.05): Faster, more abrupt movements
* **Medium values** (0.1-0.2): Natural, smooth movements
* **Higher values** (0.5-1.0): Very slow, exaggerated movements

**Example**:

.. code-block:: python

   # Quick, snappy movement
   mouse.move_to_target(step_duration=0.05)

   # Smooth, natural movement (default)
   mouse.move_to_target(step_duration=0.1)

   # Slow, deliberate movement
   mouse.move_to_target(step_duration=0.5)

hold_button
^^^^^^^^^^^

**Type**: ``HoldMouseButton`` (default: ``HoldMouseButton.NONE``)

**Description**: Specifies which mouse button to hold down during movement, enabling drag-and-drop operations.

**Available Options**:

* ``HoldMouseButton.NONE``: No button held (default)
* ``HoldMouseButton.LEFT``: Hold left mouse button
* ``HoldMouseButton.RIGHT``: Hold right mouse button
* ``HoldMouseButton.MIDDLE``: Hold middle mouse button

**Example**:

.. code-block:: python

   from windmouse import HoldMouseButton

   # Drag with left mouse button
   mouse.dest_position = (Coordinate(500), Coordinate(300))
   mouse.move_to_target(hold_button=HoldMouseButton.LEFT)

   # Right-click drag
   mouse.dest_position = (Coordinate(700), Coordinate(400))
   mouse.move_to_target(hold_button=HoldMouseButton.RIGHT)

Fine-Tuning the Physics
------------------------

The WindMouse algorithm simulates physical forces to create realistic movement. You can customize these parameters when creating the controller.

Understanding the Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**gravity_magnitude** (default: ``9``)
   Strength of the attractive force pulling the cursor toward the target.

   * **Higher values** (12-15): More direct paths, faster convergence
   * **Lower values** (5-7): More curved, wandering paths

**wind_magnitude** (default: ``3``)
   Amount of random "wind" force creating curvature and unpredictability.

   * **Higher values** (5-10): More curved, chaotic paths
   * **Lower values** (1-2): Straighter, more predictable paths

**max_step** (default: ``15``)
   Maximum velocity/speed of the cursor (measured in pixels per step).

   * **Higher values** (20-30): Faster overall movement
   * **Lower values** (5-10): Slower, more controlled movement

**damped_distance** (default: ``12``)
   Distance from target (in pixels) where the movement begins to slow down and wind effects decrease.

   * **Higher values** (20-30): Slows down earlier, more cautious approach
   * **Lower values** (5-10): Maintains speed closer to target

Customization Examples
^^^^^^^^^^^^^^^^^^^^^^^

**Aggressive, Fast Movement**:

.. code-block:: python

   mouse = PyautoguiMouseController(
       gravity_magnitude=15,  # Strong pull toward target
       wind_magnitude=1,      # Minimal curvature
       max_step=25,           # High speed
       damped_distance=8      # Late slowdown
   )

**Natural, Human-like Movement** (Default):

.. code-block:: python

   mouse = PyautoguiMouseController(
       gravity_magnitude=9,
       wind_magnitude=3,
       max_step=15,
       damped_distance=12
   )

**Cautious, Curved Movement**:

.. code-block:: python

   mouse = PyautoguiMouseController(
       gravity_magnitude=6,   # Weaker attraction
       wind_magnitude=7,      # High curvature
       max_step=10,           # Lower speed
       damped_distance=25     # Early slowdown
   )

**Drunk/Chaotic Movement** (for testing detection):

.. code-block:: python

   mouse = PyautoguiMouseController(
       gravity_magnitude=5,
       wind_magnitude=10,
       max_step=8,
       damped_distance=30
   )

Advanced Usage Patterns
------------------------

Setting Start and Destination Separately
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can set start and destination coordinates independently:

.. code-block:: python

   mouse = PyautoguiMouseController()

   # Set start position explicitly
   mouse.start_position = (Coordinate(100), Coordinate(100))

   # Set destination
   mouse.dest_position = (Coordinate(500), Coordinate(500))

   # Or set coordinates individually
   mouse.dest_x = Coordinate(800)
   mouse.dest_y = Coordinate(600)

   mouse.move_to_target()

If you don't set ``start_position``, the controller automatically uses the current mouse position.

Multiple Sequential Movements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Chain multiple movements together for complex patterns:

.. code-block:: python

   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate
   import time

   mouse = PyautoguiMouseController()

   # Define a series of waypoints
   waypoints = [
       (Coordinate(200), Coordinate(200)),
       (Coordinate(600), Coordinate(200)),
       (Coordinate(600), Coordinate(600)),
       (Coordinate(200), Coordinate(600)),
       (Coordinate(400), Coordinate(400)),  # Return to center
   ]

   # Move through each waypoint
   for dest in waypoints:
       mouse.dest_position = dest
       mouse.move_to_target(tick_delay=0.005)
       time.sleep(0.5)  # Pause at each waypoint

Manual Tick-Based Movement
^^^^^^^^^^^^^^^^^^^^^^^^^^^

For advanced control, you can manually call ``tick()`` instead of ``move_to_target()``:

.. code-block:: python

   import time

   mouse = PyautoguiMouseController()
   mouse.dest_position = (Coordinate(800), Coordinate(600))

   # Manual control loop
   while mouse.tick(step_duration=0.1):
       # Do something between each step
       time.sleep(0.01)

       # You could check conditions and break early
       if some_condition:
           break

This is useful when you need to:

* Check conditions during movement
* Synchronize with other operations
* Implement custom stopping logic

Drag and Drop Operations
^^^^^^^^^^^^^^^^^^^^^^^^^

Complete drag-and-drop example:

.. code-block:: python

   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate, HoldMouseButton
   import time

   mouse = PyautoguiMouseController()

   # Move to the item to drag
   mouse.dest_position = (Coordinate(300), Coordinate(300))
   mouse.move_to_target()
   time.sleep(0.2)  # Brief pause

   # Drag to destination
   mouse.dest_position = (Coordinate(700), Coordinate(500))
   mouse.move_to_target(hold_button=HoldMouseButton.LEFT)
   time.sleep(0.1)  # Brief pause after drop

Context Manager Pattern
^^^^^^^^^^^^^^^^^^^^^^^

While not built-in, you can create a context manager for cleanup:

.. code-block:: python

   from contextlib import contextmanager
   from windmouse.pyautogui_controller import PyautoguiMouseController

   @contextmanager
   def windmouse_controller(**kwargs):
       """Context manager for WindMouse controller."""
       controller = PyautoguiMouseController(**kwargs)
       try:
           yield controller
       finally:
           # Cleanup if needed
           pass

   # Usage
   with windmouse_controller(gravity_magnitude=10) as mouse:
       mouse.dest_position = (Coordinate(800), Coordinate(600))
       mouse.move_to_target()

Performance Considerations
--------------------------

Movement Speed vs. Realism
^^^^^^^^^^^^^^^^^^^^^^^^^^^

There's a trade-off between speed and realism:

* **Fast movements**: Low ``tick_delay`` (0-0.001), low ``step_duration`` (0.01-0.05)
* **Realistic movements**: Medium ``tick_delay`` (0.005-0.01), medium ``step_duration`` (0.1-0.2)
* **Exaggerated realism**: Higher values, more pronounced curves (``wind_magnitude`` 5-10)

Backend Performance
^^^^^^^^^^^^^^^^^^^

* **PyAutoGUI**: Slight overhead from Python → OS calls, but very portable
* **AutoHotkey**: Native Windows integration, potentially smoother on Windows systems

For maximum performance:

.. code-block:: python

   # Minimal delay configuration
   mouse.move_to_target(tick_delay=0, step_duration=0.01)

Screen Resolution Considerations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The WindMouse algorithm scales well across resolutions, but you may want to adjust parameters for different screen sizes:

.. code-block:: python

   import pyautogui

   # Get screen dimensions
   screen_width, screen_height = pyautogui.size()

   # Adjust max_step based on screen size
   max_step_adjusted = int(screen_width / 100)  # ~19 for 1920px width

   mouse = PyautoguiMouseController(max_step=max_step_adjusted)

Best Practices
--------------

1. **Always use Coordinate type**:

   .. code-block:: python

      # Good
      mouse.dest_position = (Coordinate(800), Coordinate(600))

      # Avoid (type checker will complain)
      mouse.dest_position = (800, 600)

2. **Add small delays between operations**:

   .. code-block:: python

      import time

      mouse.move_to_target()
      time.sleep(0.1)  # Brief pause before next action
      # Click or other operation

3. **Test parameter combinations**:

   Different applications may be more or less sensitive to mouse patterns. Experiment with physics parameters to find what works best.

4. **Handle exceptions**:

   .. code-block:: python

      try:
          mouse.dest_position = (Coordinate(800), Coordinate(600))
          mouse.move_to_target()
      except ValueError as e:
          print(f"Invalid coordinates: {e}")
      except Exception as e:
          print(f"Unexpected error: {e}")

5. **Consider adding random variations**:

   .. code-block:: python

      import random

      # Add slight randomness to destination
      base_x, base_y = 800, 600
      offset = 5
      dest_x = Coordinate(base_x + random.randint(-offset, offset))
      dest_y = Coordinate(base_y + random.randint(-offset, offset))

      mouse.dest_position = (dest_x, dest_y)
      mouse.move_to_target()

Common Patterns
---------------

Web Scraping
^^^^^^^^^^^^

.. code-block:: python

   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate
   import time
   import random

   def click_element(x: int, y: int):
       """Click an element with natural mouse movement."""
       mouse = PyautoguiMouseController(
           gravity_magnitude=9,
           wind_magnitude=3,
           max_step=12
       )

       # Add slight randomness
       offset = 3
       dest_x = Coordinate(x + random.randint(-offset, offset))
       dest_y = Coordinate(y + random.randint(-offset, offset))

       mouse.dest_position = (dest_x, dest_y)
       mouse.move_to_target(tick_delay=0.003)

       # Small pause before clicking
       time.sleep(random.uniform(0.1, 0.3))

       # Perform click
       import pyautogui
       pyautogui.click()

Game Automation
^^^^^^^^^^^^^^^

.. code-block:: python

   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate
   import time

   class GameBot:
       def __init__(self):
           self.mouse = PyautoguiMouseController(
               gravity_magnitude=12,  # Faster response
               wind_magnitude=2,      # Less curvature
               max_step=20            # Higher speed
           )

       def target_enemy(self, x: int, y: int):
           """Target and click enemy."""
           self.mouse.dest_position = (Coordinate(x), Coordinate(y))
           self.mouse.move_to_target(
               tick_delay=0,
               step_duration=0.05
           )
           time.sleep(0.05)
           # Perform attack

       def patrol(self, points: list[tuple[int, int]]):
           """Move through patrol points."""
           for x, y in points:
               self.mouse.dest_position = (Coordinate(x), Coordinate(y))
               self.mouse.move_to_target(tick_delay=0.002)
               time.sleep(1.0)  # Wait at each point

Next Steps
----------

* Learn more about the algorithm internals in :doc:`algorithm`
* Explore the complete API reference in :doc:`api`
* Check out advanced examples in the GitHub repository

