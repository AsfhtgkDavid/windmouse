# Contributing to WindMouse

🎉 **Thank you for your interest in contributing to WindMouse!** 🎉

We welcome all contributions-whether you're fixing a bug, improving documentation, adding new features, or suggesting enhancements. Every contribution helps make WindMouse better for everyone.

---

## Philosophy

WindMouse aims to provide a clean, efficient, and extensible implementation of human-like mouse movement. We value:

- **Simplicity**: Code should be easy to understand and maintain
- **Performance**: Movements should be smooth and efficient
- **Developer Experience**: Contributing should be straightforward and enjoyable

---

## Prerequisites

This project uses [**uv**](https://github.com/astral-sh/uv), an extremely fast Python package installer and resolver. You'll need to have `uv` installed to work with this project.

### Installing uv

If you don't have `uv` installed yet, you can install it with:

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative (via pip):**
```bash
pip install uv
```

For more installation options, visit the [uv documentation](https://github.com/astral-sh/uv).

---

## Local Development Setup

### 1. Fork and Clone the Repository

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/windmouse.git
cd windmouse
```

### 2. Install Dependencies

With `uv`, setting up your development environment is incredibly fast:

```bash
# Sync all dependencies (including dev dependencies)
uv sync --all-groups
```

This will:
- Create a virtual environment (if it doesn't exist)
- Install all project dependencies
- Install development tools (black, mypy)
- Install optional dependencies (pyautogui, ahk)

**Alternative: Install only core dependencies**
```bash
uv sync
```

**Alternative: Install with specific dependency groups**
```bash
# Just pyautogui support
uv sync --group pyautogui --group dev

# Just ahk support (Windows only)
uv sync --group ahk --group dev
```

---

## Working with the Code

### Running Scripts

You can run Python scripts in the project environment using:

```bash
uv run python your_script.py
```

Or activate the virtual environment:

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python your_script.py
```

### ⚠️ Important Warning

**Be careful when running tests or example scripts!** This library controls mouse movement, which means:

- Your mouse **will move** automatically during execution
- This can interfere with your work or cause unexpected clicks

---

## Code Quality

We use industry-standard tools to maintain code quality and consistency.

### Code Formatting with Black

We use [Black](https://black.readthedocs.io/) with a line length of 79 characters:

```bash
# Format all code
uv run black src/

# Check formatting without making changes
uv run black --check src/
```

### Type Checking with mypy

We enforce strict type checking:

```bash
# Run type checker
uv run mypy src/
```

### Before Submitting a PR

Make sure your code passes all checks:

```bash
# Format code
uv run black src/

# Type check
uv run mypy src/
```

---

## Running Tests

> **Note**: At the time of writing, the project doesn't have automated tests yet. This is a great area where contributions are welcome! If you'd like to help set up a testing framework (pytest, for example), please open an issue to discuss the approach.

If tests are added in the future:

```bash
uv run pytest
```

---

## Pull Request Process

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Write clear, concise code
- Follow the existing code style (Black formatting, type hints)
- Add docstrings to new functions/classes
- Update documentation if you're changing behavior or adding features

### 3. Test Your Changes

- Manually test your changes (remember the mouse movement warning!)
- Ensure formatting and type checking pass:
  ```bash
  uv run black src/
  uv run mypy src/
  ```

### 4. Commit Your Changes

Write meaningful commit messages:

```bash
git add .
git commit -m "Add feature: descriptive message about what changed"
```

Good commit message examples:
- `feat: add support for custom easing functions`
- `fix: correct calculation in damped distance logic`
- `docs: update README with new examples`
- `refactor: simplify wind force calculation`

### 5. Push and Create a Pull Request

```bash
git push origin feature/your-feature-name
```

Then, open a Pull Request on GitHub with:
- A clear title describing the change
- A description explaining:
  - **What** changed
  - **Why** it was needed
  - **How** it works (if non-obvious)
- Any relevant issue numbers (e.g., "Closes #42")

---

## Project Structure

```
windmouse/
├── src/
│   ├── __init__.py
│   ├── core.py                    # Core WindMouse algorithm
│   ├── ahk_controller.py          # AutoHotkey backend (Windows)
│   └── pyautogui_controller.py    # PyAutoGUI backend (cross-platform)
├── pyproject.toml                 # Project configuration
├── README.md
└── CONTRIBUTING.md                # You are here!
```

---

## Areas Where We Need Help

Here are some ways you can contribute:

- 🧪 **Testing**: Help us set up a comprehensive test suite
- 📚 **Documentation**: Improve examples, add tutorials, or write better docstrings
- 🐛 **Bug Fixes**: Found a bug? Fix it and submit a PR!
- ✨ **Features**: Add new backends, easing functions, or configuration options
- 🎨 **Code Quality**: Improve performance, readability, or maintainability
- 🌍 **Platform Support**: Test on different platforms and report/fix issues

---

## Code of Conduct

Be respectful and constructive in all interactions. We're all here to learn and build something great together.

---

## Questions?

If you have questions or need help:
1. Check existing [Issues](https://github.com/AsfhtgkDavid/windmouse/issues)
2. Open a new issue with the `question` label
3. Reach out to the maintainers

---

## Thank You!

Your contributions make WindMouse better for everyone. We appreciate your time and effort! 🚀

Happy coding! 🖱️✨

