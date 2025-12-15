API Reference
=============

This page provides detailed API documentation for all public classes, functions, and types in the WindMouse library.

Core Module
-----------

wind_mouse Function
^^^^^^^^^^^^^^^^^^^

.. autofunction:: windmouse.core.wind_mouse

AbstractMouseController Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: windmouse.core.AbstractMouseController
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Types and Enums
^^^^^^^^^^^^^^^

.. autoclass:: windmouse.core.HoldMouseButton
   :members:
   :undoc-members:

.. data:: windmouse.core.Coordinate
   :annotation: = NewType('Coordinate', int)

   Type alias for coordinate values. Provides type safety for x and y coordinates.

   Example::

       from windmouse import Coordinate
       x = Coordinate(100)
       y = Coordinate(200)

Constants
^^^^^^^^^

.. data:: windmouse.core.GRAVITY_MAGNITUDE_DEFAULT
   :annotation: = 9

   Default gravity magnitude value.

.. data:: windmouse.core.WIND_MAGNITUDE_DEFAULT
   :annotation: = 3

   Default wind magnitude value.

.. data:: windmouse.core.MAX_STEP_DEFAULT
   :annotation: = 15

   Default maximum step size value.

.. data:: windmouse.core.DAMPED_DISTANCE_DEFAULT
   :annotation: = 12

   Default damped distance value.

PyAutoGUI Controller
--------------------

Cross-platform mouse controller using PyAutoGUI.

.. autoclass:: windmouse.pyautogui_controller.PyautoguiMouseController
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

AutoHotkey Controller
---------------------

Windows-only mouse controller using AutoHotkey.

.. autoclass:: windmouse.ahk_controller.AHKMouseController
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Exported Types
--------------

The main ``windmouse`` package exports commonly used types and enums for convenience:

.. code-block:: python

   from windmouse import Coordinate, HoldMouseButton

Common Exceptions
-----------------

**ValueError**
   Raised when destination coordinates are not set before movement.

**OSError**
   Raised when trying to use AHK backend on non-Windows platforms or when trying to import non-installed backends.

For error handling examples, see :doc:`examples`.

See Also
--------

* :doc:`usage` - Detailed usage guide and parameter explanations
* :doc:`examples` - Practical code examples and best practices
* :doc:`algorithm` - Detailed explanation of the WindMouse algorithm
* :doc:`installation` - Installation instructions and troubleshooting

