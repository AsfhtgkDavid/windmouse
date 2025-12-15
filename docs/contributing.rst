Contributing
============

Thank you for your interest in contributing to WindMouse! This document provides guidelines and instructions for contributing to the project.

We welcome contributions of all kinds:

* 🐛 Bug reports and fixes
* ✨ New features and enhancements
* 📖 Documentation improvements
* 🧪 Tests and test coverage improvements
* 💡 Ideas and suggestions

Getting Started
---------------

Development Setup
^^^^^^^^^^^^^^^^^

1. **Fork and Clone**

   Fork the repository on GitHub and clone your fork:

   .. code-block:: bash

      git clone https://github.com/YOUR_AsfhtgkDavid/windmouse.git
      cd windmouse

2. **Install Dependencies**

   Using pip:

   .. code-block:: bash

      pip install -e .[all,dev,docs]

   Or using uv (recommended):

   .. code-block:: bash

      uv sync --all-groups

3. **Verify Installation**

   Run a quick test to ensure everything is working:

   .. code-block:: python

      python -c "from windmouse.pyautogui_controller import PyautoguiMouseController; print('Success!')"

Code Style
----------

WindMouse follows strict code quality standards to maintain consistency and readability.

Formatting
^^^^^^^^^^

We use **Black** for code formatting with a line length of 79 characters:

.. code-block:: bash

   # Format your code before committing
   black src/

Black configuration is in ``pyproject.toml``:

.. code-block:: toml

   [tool.black]
   line-length = 79

Type Checking
^^^^^^^^^^^^^

We use **mypy** with strict mode enabled. All code must pass type checking:

.. code-block:: bash

   # Run type checker
   mypy src/

Mypy configuration is in ``pyproject.toml``:

.. code-block:: toml

   [tool.mypy]
   strict = true

Key type checking requirements:

* All function parameters must have type hints
* All return types must be annotated
* No ``Any`` types without explicit justification
* Use ``Optional[T]`` for nullable values
* Use ``NewType`` for semantic type safety (like ``Coordinate``)

Code Guidelines
^^^^^^^^^^^^^^^

Follow these guidelines when writing code:

1. **Docstrings**: Use Google or NumPy style docstrings for all public APIs:

   .. code-block:: python

      def example_function(param1: int, param2: str) -> bool:
          """
          Brief description of the function.

          Args:
              param1: Description of param1.
              param2: Description of param2.

          Returns:
              Description of return value.

          Raises:
              ValueError: When invalid input is provided.
          """
          pass

2. **Import Order**: Follow standard Python import conventions:

   .. code-block:: python

      # Standard library
      import enum
      import time
      from abc import ABC, abstractmethod

      # Third-party
      import numpy as np

      # Local
      from .core import Coordinate

3. **Naming Conventions**:

   * Classes: ``PascalCase`` (e.g., ``PyautoguiMouseController``)
   * Functions/methods: ``snake_case`` (e.g., ``move_to_target``)
   * Constants: ``UPPER_SNAKE_CASE`` (e.g., ``GRAVITY_MAGNITUDE_DEFAULT``)
   * Private methods: ``_leading_underscore`` (e.g., ``_get_next_point``)

4. **Abstract Methods**: Use ``@abstractmethod`` decorator for interface definitions

5. **Type Safety**: Prefer ``NewType`` for semantic clarity (like ``Coordinate``)

Making Changes
--------------

Branch Naming
^^^^^^^^^^^^^

Use descriptive branch names with prefixes:

* ``feature/`` - New features (e.g., ``feature/add-bezier-mode``)
* ``fix/`` - Bug fixes (e.g., ``fix/velocity-clamp-issue``)
* ``docs/`` - Documentation (e.g., ``docs/improve-api-reference``)
* ``refactor/`` - Code refactoring (e.g., ``refactor/simplify-tick-logic``)
* ``test/`` - Test additions/improvements (e.g., ``test/add-ahk-tests``)

Commit Messages
^^^^^^^^^^^^^^^

Write clear, descriptive commit messages using conventional commits format:

.. code-block:: text

   <type>: <short description>

   <optional longer description>

   <optional footer>

Types:

* ``feat``: New feature
* ``fix``: Bug fix
* ``docs``: Documentation changes
* ``style``: Formatting, missing semicolons, etc.
* ``refactor``: Code restructuring without behavior change
* ``test``: Adding or updating tests
* ``chore``: Maintenance tasks

Examples:

.. code-block:: text

   feat: Add support for circular mouse paths

   Implements a new CircularPathController that moves the mouse
   in circular trajectories instead of WindMouse paths.

.. code-block:: text

   fix: Correct velocity clamping calculation

   The max_step parameter was not being applied correctly in
   close-range scenarios. This fixes the clamping logic.

.. code-block:: text

   docs: Add troubleshooting section for Linux permissions

Testing
-------

Running Tests
^^^^^^^^^^^^^

Before submitting a pull request, ensure all tests pass:

.. code-block:: bash

   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=src --cov-report=html

   # Run specific test file
   pytest tests/test_core.py

Writing Tests
^^^^^^^^^^^^^

When adding new features, include appropriate tests:

.. code-block:: python

   import pytest
   from windmouse.core import wind_mouse, Coordinate


   def test_wind_mouse_convergence():
       """Test that wind_mouse reaches the target."""
       start_x, start_y = Coordinate(0), Coordinate(0)
       dest_x, dest_y = Coordinate(100), Coordinate(100)

       path = list(wind_mouse(start_x, start_y, dest_x, dest_y))

       # Check that we have a path
       assert len(path) > 0

       # Check that final position is close to target
       final_x, final_y = path[-1]
       assert abs(final_x - dest_x) <= 1
       assert abs(final_y - dest_y) <= 1

Test guidelines:

* Test both success and failure cases
* Use descriptive test names
* Include docstrings explaining what the test verifies
* Mock external dependencies (like ``pyautogui`` or ``ahk``)
* Aim for high code coverage (target: >80%)

Documentation
-------------

Building Documentation
^^^^^^^^^^^^^^^^^^^^^^

Build the documentation locally to preview changes:

.. code-block:: bash

   cd docs
   make html

   # View in browser
   open _build/html/index.html  # macOS
   xdg-open _build/html/index.html  # Linux
   start _build/html/index.html  # Windows

Or use Sphinx directly:

.. code-block:: bash

   sphinx-build -b html docs docs/_build/html

Documentation Guidelines
^^^^^^^^^^^^^^^^^^^^^^^^

When updating documentation:

1. **Use reStructuredText (.rst) format** for all documentation files
2. **Include code examples** that are tested and working
3. **Cross-reference** related sections using ``:doc:`` directives
4. **Update API documentation** if you change function signatures
5. **Add new pages** to the ``toctree`` in ``index.rst``

Example of good documentation:

.. code-block:: rst

   Advanced Usage
   ==============

   This section covers advanced usage patterns.

   Custom Physics
   --------------

   You can customize the physics parameters:

   .. code-block:: python

      from windmouse.pyautogui_controller import PyautoguiMouseController

      mouse = PyautoguiMouseController(
          gravity_magnitude=12,
          wind_magnitude=5
      )

   See :doc:`algorithm` for details on parameter effects.

Pull Request Process
--------------------

1. **Create a Feature Branch**

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. **Make Your Changes**

   * Write code following the style guidelines
   * Add tests for new functionality
   * Update documentation as needed

3. **Format and Check**

   .. code-block:: bash

      # Format code
      black src/

      # Type check
      mypy src/

      # Run tests
      pytest

4. **Commit Your Changes**

   .. code-block:: bash

      git add .
      git commit -m "feat: Add your feature description"

5. **Push to Your Fork**

   .. code-block:: bash

      git push origin feature/your-feature-name

6. **Open a Pull Request**

   * Go to the original repository on GitHub
   * Click "New Pull Request"
   * Select your fork and branch
   * Fill out the PR template with:

     * Description of changes
     * Motivation and context
     * Testing performed
     * Screenshots (if applicable)

7. **Respond to Review**

   * Address reviewer feedback promptly
   * Make requested changes
   * Push updates to the same branch

Pull Request Checklist
^^^^^^^^^^^^^^^^^^^^^^^

Before submitting, ensure:

- [ ] Code follows style guidelines (Black, mypy)
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive
- [ ] PR description explains the changes
- [ ] No unnecessary files are included
- [ ] Branch is up to date with main

Reporting Issues
----------------

Bug Reports
^^^^^^^^^^^

When reporting a bug, include:

1. **Clear Title**: Descriptive summary of the issue
2. **Environment**:

   * Python version
   * Operating system
   * WindMouse version
   * Backend (PyAutoGUI or AHK)

3. **Steps to Reproduce**: Minimal code example
4. **Expected Behavior**: What you expected to happen
5. **Actual Behavior**: What actually happened
6. **Screenshots/Logs**: If applicable

Example bug report:

.. code-block:: text

   Title: ValueError when using None as start_position

   **Environment:**
   - Python 3.11
   - Windows 11
   - WindMouse 1.0.0
   - PyAutoGUI backend

   **Steps to Reproduce:**
   ```python
   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   mouse = PyautoguiMouseController()
   mouse.start_position = (None, Coordinate(100))
   mouse.dest_position = (Coordinate(500), Coordinate(500))
   mouse.move_to_target()
   ```

   **Expected:** Should use current x position
   **Actual:** Raises ValueError

   **Traceback:**
   ```
   ValueError: start_x cannot be None when start_y is set
   ```

Feature Requests
^^^^^^^^^^^^^^^^

When requesting a feature:

1. **Describe the feature** clearly
2. **Explain the use case** - why is it needed?
3. **Provide examples** - how would it be used?
4. **Consider alternatives** - are there existing solutions?

Community Guidelines
--------------------

Code of Conduct
^^^^^^^^^^^^^^^

This project adheres to a Code of Conduct. By participating, you agree to:

* Be respectful and inclusive
* Welcome newcomers
* Accept constructive criticism gracefully
* Focus on what's best for the community
* Show empathy towards others

Communication
^^^^^^^^^^^^^

* **GitHub Issues**: For bugs, features, and questions
* **Pull Requests**: For code contributions
* **Discussions**: For general questions and ideas

Recognition
-----------

Contributors will be:

* Listed in the project's contributors list
* Credited in release notes for significant contributions
* Thanked in documentation and README

Development Tips
----------------

Debugging
^^^^^^^^^

Use the manual tick system for debugging:

.. code-block:: python

   mouse = PyautoguiMouseController()
   mouse.dest_position = (Coordinate(800), Coordinate(600))

   step = 0
   while mouse.tick(step_duration=0.1):
       step += 1
       print(f"Step {step}: Current position")
       time.sleep(0.1)

Testing Locally
^^^^^^^^^^^^^^^

Test with different parameters:

.. code-block:: python

   test_configs = [
       {"gravity_magnitude": 5, "wind_magnitude": 8},
       {"gravity_magnitude": 12, "wind_magnitude": 1},
       {"max_step": 5, "damped_distance": 30},
   ]

   for config in test_configs:
       mouse = PyautoguiMouseController(**config)
       mouse.dest_position = (Coordinate(500), Coordinate(500))
       mouse.move_to_target()

Virtual Environment
^^^^^^^^^^^^^^^^^^^

Always use a virtual environment:

.. code-block:: bash

   # Create venv
   python -m venv venv

   # Activate
   source venv/bin/activate  # Linux/macOS
   venv\\Scripts\\activate     # Windows

   # Install in development mode
   pip install -e .[all,dev,docs]

Questions?
----------

If you have questions about contributing:

* Check existing issues and discussions
* Review this contributing guide
* Ask in a GitHub discussion
* Open an issue with the "question" label

Thank you for contributing to WindMouse! 🎉

See Also
--------

* :doc:`installation` - Setup instructions
* :doc:`usage` - Usage examples
* :doc:`api` - API reference
* `GitHub Repository <https://github.com/AsfhtgkDavid/windmouse>`_

