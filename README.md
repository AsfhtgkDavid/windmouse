# WindMouse

[![codecov](https://codecov.io/gh/AsfhtgkDavid/windmouse/branch/main/graph/badge.svg)](https://codecov.io/gh/AsfhtgkDavid/windmouse)
[![PyPI - Version](https://img.shields.io/pypi/v/windmouse)](https://pypi.org/project/windmouse/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Documentation Status](https://readthedocs.org/projects/windmouse/badge/?version=latest)](https://windmouse.readthedocs.io/en/latest/?badge=latest)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

**WindMouse** is a Python library that generates human-like mouse movements to avoid bot detection in automation scripts. It implements the WindMouse algorithm, which creates realistic, non-linear trajectories with variable speed—mimicking natural human mouse behavior.

## Why WindMouse?

Traditional automation tools move the mouse in straight lines at constant speeds, making them easy to detect. WindMouse solves this by:

- ✨ **Generating curved, natural-looking paths** instead of straight lines
- ⚡ **Varying movement speed** dynamically throughout the trajectory
- 🎯 **Supporting multiple backends**: AutoHotkey (Windows) and PyAutoGUI (cross-platform)
- 🧩 **Offering fine-grained control** over movement physics (gravity, wind, damping)

Perfect for web scraping, game automation, UI testing, or any scenario where you need to simulate realistic human interaction.

---

## Demo

![Demo Animation](demo.gif)

*Demonstration of the WindMouse algorithm in action.*

---

## Installation

### Standard Installation

```bash
pip install windmouse
```

### Modern Alternative (using `uv`)

```bash
uv add windmouse
```

### Optional Dependencies

WindMouse supports multiple backends. Choose the one that fits your needs:

**For PyAutoGUI (cross-platform):**
```bash
pip install windmouse[pyautogui]
# or with uv:
uv add "windmouse[pyautogui]"
```

**For AutoHotkey (Windows only):**
```bash
pip install windmouse[ahk]
# or with uv:
uv add "windmouse[ahk]"
```

**Install all backends:**
```bash
pip install windmouse[all]
# or with uv:
uv add "windmouse[all]"
```

> **Note for Windows + AHK users**: You must have [AutoHotkey](https://www.autohotkey.com/) installed on your system to use the `ahk` backend.

---

## Quick Start

### Using PyAutoGUI (Cross-Platform)

```python
from windmouse.pyautogui_controller import PyautoguiMouseController
from windmouse import Coordinate

# Initialize the controller
mouse = PyautoguiMouseController()

# Set destination coordinates
mouse.dest_position = (Coordinate(800), Coordinate(600))

# Move the mouse using WindMouse algorithm
mouse.move_to_target(
    tick_delay=0.005,      # Small delay between steps
    step_duration=0.1      # Duration of each movement step
)
```

### Using AutoHotkey (Windows Only)

```python
from ahk import AHK
from windmouse.ahk_controller import AHKMouseController
from windmouse import Coordinate

# Initialize AHK and controller
ahk = AHK()
mouse = AHKMouseController(ahk)

# Set destination coordinates
mouse.dest_position = (Coordinate(800), Coordinate(600))

# Move the mouse using WindMouse algorithm
mouse.move_to_target(
    tick_delay=0.005,
    step_duration=0.1
)
```

### Advanced: Fine-Tuning the Algorithm

You can customize the physics of the mouse movement:

```python
from windmouse.pyautogui_controller import PyautoguiMouseController
from windmouse import Coordinate

mouse = PyautoguiMouseController(
    gravity_magnitude=9,    # Strength of attraction to target (default: 9)
    wind_magnitude=3,       # Randomness/curvature of path (default: 3)
    max_step=15,            # Maximum speed (default: 15)
    damped_distance=12      # Distance where movement starts to slow (default: 12)
)

mouse.dest_position = (Coordinate(1000), Coordinate(500))
mouse.move_to_target()
```

### Drag and Drop

Hold a mouse button while moving (useful for drag-and-drop operations):

```python
from windmouse import HoldMouseButton

mouse.dest_position = (Coordinate(500), Coordinate(300))
mouse.move_to_target(hold_button=HoldMouseButton.LEFT)
```

---

## Documentation

📖 **[Read the Full Documentation on ReadTheDocs](https://windmouse.readthedocs.io/)**

The documentation includes:
- Detailed algorithm explanation and mathematical background
- API reference for all classes and methods
- Advanced usage examples and best practices
- Performance tuning guide

---

## Contributing

Contributions are welcome! Whether it's bug reports, feature requests, or pull requests—your input helps make WindMouse better.

To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows the project's style guidelines and includes appropriate tests.

---

## License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**.

Portions of this software are derived from the WindMouse reference implementation by Ben Land and have been refactored and modified.

Original work:
https://ben.land/post/2021/04/25/windmouse-human-mouse-movement/

See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

The WindMouse algorithm is inspired by research on human-computer interaction and originally designed to prevent bot detection in automation scenarios. This implementation brings that algorithm to the Python ecosystem with a clean, extensible API.

