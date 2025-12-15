WindMouse Documentation
=======================

**WindMouse** is a Python library that generates human-like mouse movements to avoid bot detection in automation scripts. It implements the WindMouse algorithm, which creates realistic, non-linear trajectories with variable speed—mimicking natural human mouse behavior.

Why WindMouse?
--------------

Traditional automation tools move the mouse in straight lines at constant speeds, making them easy to detect. WindMouse solves this by:

* ✨ **Generating curved, natural-looking paths** instead of straight lines
* ⚡ **Varying movement speed** dynamically throughout the trajectory
* 🎯 **Supporting multiple backends**: AutoHotkey (Windows) and PyAutoGUI (cross-platform)
* 🧩 **Offering fine-grained control** over movement physics (gravity, wind, damping)

Perfect for web scraping, game automation, UI testing, or any scenario where you need to simulate realistic human interaction.

Key Features
------------

* **Human-like Movement**: Creates non-linear, curved trajectories that mimic natural mouse behavior
* **Physics-based Algorithm**: Uses gravity, wind, and damping parameters to simulate realistic motion
* **Multi-backend Support**: Works with PyAutoGUI (cross-platform) or AutoHotkey (Windows)
* **Drag & Drop Support**: Hold mouse buttons during movement for drag operations
* **Fine-grained Control**: Adjust movement speed, curvature, and physics parameters
* **Type-safe**: Fully typed with mypy support

Quick Example
-------------

.. code-block:: python

   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   # Initialize the controller
   mouse = PyautoguiMouseController()

   # Set destination and move
   mouse.dest_position = (Coordinate(800), Coordinate(600))
   mouse.move_to_target()

Get Started
-----------

To get started with WindMouse, check out the :doc:`installation` guide, then explore the :doc:`usage` examples.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   quickref
   examples
   recomendations
   algorithm
   api
   contributing

.. toctree::
   :maxdepth: 1
   :caption: Additional Resources:

   GitHub Repository <https://github.com/AsfhtgkDavid/windmouse>
   PyPI Package <https://pypi.org/project/windmouse/>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

