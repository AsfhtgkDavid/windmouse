Best Practices
=================

Type Safety
-----------

Always use ``Coordinate`` type for coordinates to ensure type safety:

.. code-block:: python

   from windmouse import Coordinate

   # Good ✓
   mouse.dest_position = (Coordinate(800), Coordinate(600))

   # Avoid - may work but not type-safe
   # mouse.dest_position = (800, 600)

Error Handling
--------------

Handle exceptions gracefully:

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
   except OSError as e:
       print(f"Platform error: {e}")

Resource Management
-------------------

For AHK backend, reuse the AHK instance across multiple controllers to avoid resource overhead:

.. code-block:: python

   from ahk import AHK
   from windmouse.ahk_controller import AHKMouseController
   from windmouse import Coordinate

   # Good ✓ - Create once, reuse multiple times
   ahk = AHK()
   mouse1 = AHKMouseController(ahk)
   mouse2 = AHKMouseController(ahk)

   # Avoid - Creates new AHK instance each time
   # mouse1 = AHKMouseController(AHK())
   # mouse2 = AHKMouseController(AHK())

Controller Reuse
----------------

Reuse controller instances for multiple movements:

.. code-block:: python

   # Good ✓ - Reuse controller
   mouse = PyautoguiMouseController()
   for target in targets:
       mouse.dest_position = target
       mouse.move_to_target()

   # Avoid - Creates unnecessary instances
   # for target in targets:
   #     mouse = PyautoguiMouseController()
   #     mouse.dest_position = target
   #     mouse.move_to_target()

Adding Natural Variation
-------------------------

Use random offsets and parameter variations to make movements less predictable:

.. code-block:: python

   import random
   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   # Vary physics parameters
   mouse = PyautoguiMouseController(
       gravity_magnitude=random.randint(8, 12),
       wind_magnitude=random.randint(2, 5),
       max_step=random.randint(12, 18)
   )

   # Add random offset to target
   target_x = Coordinate(800 + random.randint(-10, 10))
   target_y = Coordinate(600 + random.randint(-10, 10))
   mouse.dest_position = (target_x, target_y)
   mouse.move_to_target()

