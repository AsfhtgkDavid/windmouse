Installation
============

This guide covers the installation process for WindMouse and its optional dependencies.

Requirements
------------

* Python 3.10 or higher
* NumPy 1.20 or higher (automatically installed)

Operating System Support:

* **PyAutoGUI backend**: Windows, macOS, Linux
* **AutoHotkey backend**: Windows only

Standard Installation
---------------------

The basic installation includes the core WindMouse algorithm and NumPy dependency:

.. code-block:: bash

   pip install windmouse

This installs the core library without any controller backends.

Modern Alternative (uv)
-----------------------

`uv <https://github.com/astral-sh/uv>`_ is a modern, fast Python package installer:

.. code-block:: bash

   uv add windmouse

Installing Backend Dependencies
--------------------------------

WindMouse supports multiple backends for controlling the mouse. Choose the one that fits your needs.

PyAutoGUI Backend (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PyAutoGUI is a cross-platform library that works on Windows, macOS, and Linux:

.. code-block:: bash

   pip install windmouse[pyautogui]

Or with uv:

.. code-block:: bash

   uv add "windmouse[pyautogui]"

**Additional PyAutoGUI Requirements:**

On **Linux**, you may need to install additional dependencies:

.. code-block:: bash

   # Ubuntu/Debian
   sudo apt-get install python3-tk python3-dev

   # Fedora
   sudo dnf install python3-tkinter python3-devel

   # Arch Linux
   sudo pacman -S tk

On **macOS**, PyAutoGUI should work out of the box on most systems.

AutoHotkey Backend (Windows Only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

AutoHotkey provides native Windows integration and potentially smoother mouse movements:

.. code-block:: bash

   pip install windmouse[ahk]

Or with uv:

.. code-block:: bash

   uv add "windmouse[ahk]"

**Important**: You must have `AutoHotkey <https://www.autohotkey.com/>`_ installed on your system:

1. Download AutoHotkey from https://www.autohotkey.com/
2. Install it (the default installation is sufficient)
3. Ensure it's accessible from your system PATH

Install All Backends
^^^^^^^^^^^^^^^^^^^^^

To install both backends at once:

.. code-block:: bash

   pip install windmouse[all]

Or with uv:

.. code-block:: bash

   uv add "windmouse[all]"

Development Installation
------------------------

If you want to contribute to WindMouse or run the examples, clone the repository and install in development mode:

.. code-block:: bash

   git clone https://github.com/AsfhtgkDavid/windmouse.git
   cd windmouse
   pip install -e .[all,dev]

Or with uv:

.. code-block:: bash

   git clone https://github.com/AsfhtgkDavid/windmouse.git
   cd windmouse
   uv sync --all-groups

Verifying Installation
----------------------

After installation, verify that WindMouse is working:

.. code-block:: python

   # Test with PyAutoGUI
   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   mouse = PyautoguiMouseController()
   print("PyAutoGUI backend loaded successfully!")

For AutoHotkey (Windows only):

.. code-block:: python

   # Test with AHK
   from ahk import AHK
   from windmouse.ahk_controller import AHKMouseController

   ahk = AHK()
   mouse = AHKMouseController(ahk)
   print("AHK backend loaded successfully!")

Troubleshooting
---------------

Import Errors
^^^^^^^^^^^^^

**Problem**: ``ImportError: You need install windmouse[pyautogui]``

**Solution**: Install the appropriate backend extras:

.. code-block:: bash

   pip install windmouse[pyautogui]

**Problem**: ``OSError: Ahk available only for Windows``

**Solution**: The AutoHotkey backend only works on Windows. Use PyAutoGUI on other platforms.

Permission Errors (Linux)
^^^^^^^^^^^^^^^^^^^^^^^^^

**Problem**: Mouse doesn't move or permission denied errors on Linux.

**Solution**: On some Linux systems, you may need to run your script with appropriate permissions or configure X11 access:

.. code-block:: bash

   # Option 1: Run with sudo (not recommended for production)
   sudo python your_script.py

   # Option 2: Configure X11 to allow connections (better approach)
   xhost +local:

   # Option 3: Use accessibility features (distro-specific)
   # Check your distribution's documentation for enabling accessibility

PyAutoGUI Issues on macOS
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Problem**: PyAutoGUI not working on macOS.

**Solution**: You may need to grant accessibility permissions:

1. Go to System Preferences → Security & Privacy → Privacy → Accessibility
2. Add your terminal application or Python interpreter to the list
3. Check the box to grant permission
4. Restart your terminal/IDE

AutoHotkey Not Found (Windows)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Problem**: ``AutoHotkey is not installed or not in PATH``

**Solution**:

1. Download and install AutoHotkey from https://www.autohotkey.com/
2. Ensure the installation directory is in your system PATH
3. Restart your terminal/IDE after installation
4. Verify by running ``ahk`` in Command Prompt

Virtual Display (Headless Servers)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Problem**: Need to run WindMouse on a headless server (no display).

**Solution**: Use a virtual display driver like Xvfb on Linux:

.. code-block:: bash

   # Install Xvfb
   sudo apt-get install xvfb

   # Run your script with virtual display
   xvfb-run python your_script.py

For Windows servers, consider using virtual desktop tools or remote desktop services.

NumPy Compatibility
^^^^^^^^^^^^^^^^^^^

**Problem**: NumPy version conflicts or import errors.

**Solution**: WindMouse requires NumPy >= 1.20. Update NumPy:

.. code-block:: bash

   pip install --upgrade numpy

Type Checking Issues
^^^^^^^^^^^^^^^^^^^^

**Problem**: mypy reports errors in WindMouse code.

**Solution**: Install type stubs for dependencies:

.. code-block:: bash

   pip install types-pyautogui

Next Steps
----------

Once installation is complete, head to the :doc:`usage` guide to learn how to use WindMouse in your projects.

