Algorithm Explained
===================

This page provides an in-depth explanation of the WindMouse algorithm, its physics principles, and the mathematics behind human-like mouse movement generation.

Overview
--------

The WindMouse algorithm generates realistic, non-linear mouse trajectories by simulating physical forces acting on the cursor. Unlike simple linear interpolation (which moves in a straight line at constant speed), WindMouse creates curved paths with variable speed—closely mimicking how humans naturally move a mouse.

The Problem with Traditional Mouse Movement
--------------------------------------------

Most automation tools use linear interpolation:

.. code-block:: python

   # Naive linear movement (easily detectable)
   for t in range(steps):
       x = start_x + (dest_x - start_x) * (t / steps)
       y = start_y + (dest_y - start_y) * (t / steps)
       move_mouse(x, y)

This approach has several problems:

* **Perfect straight lines**: Humans rarely move the mouse in perfectly straight lines
* **Constant speed**: Real human movement accelerates and decelerates
* **No variation**: Repeated movements follow identical paths
* **Easily detectable**: Bot detection systems can identify these patterns

The WindMouse Solution
-----------------------

WindMouse solves these problems by simulating a physics-based system with three key forces:

1. **Gravity**: Attracts the cursor toward the target (directed force)
2. **Wind**: Adds randomness and curvature to the path (random force)
3. **Velocity Damping**: Slows down as the cursor approaches the target

The algorithm operates in discrete time steps, updating velocity and position at each iteration.

Mathematical Model
------------------

Physics Simulation
^^^^^^^^^^^^^^^^^^

At each time step, the algorithm updates the cursor state based on forces:

**Position Update**:

.. math::

   x_{t+1} = x_t + v_x

   y_{t+1} = y_t + v_y

**Velocity Update**:

.. math::

   v_x = v_x + W_x + G_x

   v_y = v_y + W_y + G_y

Where:
- :math:`v_x, v_y` are velocity components
- :math:`W_x, W_y` are wind force components
- :math:`G_x, G_y` are gravity force components

Gravity Force
^^^^^^^^^^^^^

Gravity provides the directed force pulling the cursor toward the target:

.. math::

   G_x = g \\cdot \\frac{(dest_x - x)}{dist}

   G_y = g \\cdot \\frac{(dest_y - y)}{dist}

Where:
- :math:`g` is ``gravity_magnitude`` (default: 9)
- :math:`dist = \\sqrt{(dest_x - x)^2 + (dest_y - y)^2}` is the distance to target

This creates a force vector pointing directly at the target with magnitude proportional to ``gravity_magnitude``.

Wind Force
^^^^^^^^^^

Wind adds randomness and curvature. Its behavior changes based on distance from target:

**Far from target** (:math:`dist \\geq damped\\_distance`):

.. math::

   W_x = \\frac{W_x}{\\sqrt{3}} + \\frac{(2r - 1) \\cdot w}{\\sqrt{5}}

   W_y = \\frac{W_y}{\\sqrt{3}} + \\frac{(2r - 1) \\cdot w}{\\sqrt{5}}

**Close to target** (:math:`dist < damped\\_distance`):

.. math::

   W_x = \\frac{W_x}{\\sqrt{3}}

   W_y = \\frac{W_y}{\\sqrt{3}}

Where:
- :math:`r` is a random value in [0, 1]
- :math:`w = \\min(wind\\_magnitude, dist)` is the effective wind magnitude
- :math:`\\sqrt{3} \\approx 1.732` is the damping factor
- :math:`\\sqrt{5} \\approx 2.236` is the fluctuation factor

The wind force:
- Decays over time (divided by √3 each step)
- Adds random fluctuations when far from target
- Only decays (no new randomness) when close to target

Velocity Clamping
^^^^^^^^^^^^^^^^^

The velocity magnitude is clamped to prevent excessive speed:

.. math::

   |v| = \\sqrt{v_x^2 + v_y^2}

If :math:`|v| > max\\_step`:

.. math::

   clip = \\frac{max\\_step}{2} + r \\cdot \\frac{max\\_step}{2}

   v_x = \\frac{v_x}{|v|} \\cdot clip

   v_y = \\frac{v_y}{|v|} \\cdot clip

Where :math:`r` is random in [0, 1].

This ensures the cursor doesn't move too fast while adding slight speed variation.

Algorithm Pseudocode
--------------------

Here's the complete algorithm in pseudocode:

.. code-block:: text

   function WindMouse(start_x, start_y, dest_x, dest_y, gravity, wind, max_step, damped_dist):
       x, y = start_x, start_y
       vx, vy = 0, 0
       wx, wy = 0, 0

       while distance(x, y, dest_x, dest_y) >= 1:
           dist = distance(x, y, dest_x, dest_y)
           wind_current = min(wind, dist)

           # Update wind
           if dist >= damped_dist:
               wx = wx/sqrt(3) + (2*random() - 1) * wind_current/sqrt(5)
               wy = wy/sqrt(3) + (2*random() - 1) * wind_current/sqrt(5)
           else:
               wx = wx/sqrt(3)
               wy = wy/sqrt(3)
               if max_step < 3:
                   max_step = random() * 3 + 3
               else:
                   max_step = max_step/sqrt(5)

           # Update velocity with wind and gravity
           vx = vx + wx + gravity * (dest_x - x) / dist
           vy = vy + wy + gravity * (dest_y - y) / dist

           # Clamp velocity
           v_mag = sqrt(vx^2 + vy^2)
           if v_mag > max_step:
               v_clip = max_step/2 + random() * max_step/2
               vx = (vx / v_mag) * v_clip
               vy = (vy / v_mag) * v_clip

           # Update position
           x = x + vx
           y = y + vy

           yield (round(x), round(y))

Parameter Effects
-----------------

Understanding how each parameter affects the generated path:

gravity_magnitude
^^^^^^^^^^^^^^^^^

**Effect**: Controls the strength of attraction to the target.

* **Low (3-6)**: Weak attraction
   - Path wanders more
   - Takes longer to reach target
   - More influenced by wind
   - Very curved trajectories

* **Medium (7-10)**: Balanced (Default: 9)
   - Natural-looking curves
   - Reasonable convergence time
   - Good balance of control and randomness

* **High (11-15)**: Strong attraction
   - More direct paths
   - Faster convergence
   - Less curve, more purposeful
   - Dominates wind effect

**Visual Effect**:

.. code-block:: text

   Low gravity (5):     Medium gravity (9):    High gravity (13):
        *----->              *---->                  *--->
       /       \\            /     \\                 |    \\
      /         \\          /       \\                |     \\
     o           T         o         T               o      T
   (very curved)        (natural)              (fairly direct)

wind_magnitude
^^^^^^^^^^^^^^

**Effect**: Controls the amount of random curvature and unpredictability.

* **Low (0-2)**: Minimal wind
   - Nearly straight paths
   - Predictable movement
   - Less human-like
   - Good for speed-priority scenarios

* **Medium (3-5)**: Moderate wind (Default: 3)
   - Natural curves
   - Good human-like appearance
   - Balanced unpredictability

* **High (6-10)**: Strong wind
   - Very curved paths
   - Highly unpredictable
   - May look drunk/erratic
   - Good for testing detection systems

**Visual Effect**:

.. code-block:: text

   Low wind (1):        Medium wind (3):       High wind (8):
        *-->                 *~>                    *~~>
        |  \\                /  \\                  / |\\
        |   \\              /    \\                /  | \\
        o    T             o      T              o   |  T
   (nearly straight)     (gentle curve)      (chaotic path)

max_step
^^^^^^^^

**Effect**: Controls the maximum speed (pixels per step).

* **Low (5-10)**: Slow movement
   - Takes longer to reach target
   - More controlled, deliberate
   - Good for precision tasks

* **Medium (12-18)**: Normal speed (Default: 15)
   - Balanced speed and control
   - Natural-looking pace

* **High (20-30)**: Fast movement
   - Quick traversal
   - May look less natural at very high values
   - Good for efficiency-priority scenarios

**Note**: The actual movement speed also depends on ``tick_delay`` and ``step_duration`` in ``move_to_target()``.

damped_distance
^^^^^^^^^^^^^^^

**Effect**: Distance from target (in pixels) where behavior changes.

* **Low (5-10)**: Late damping
   - Maintains speed and wind longer
   - Sharper approach to target
   - Less cautious

* **Medium (12-15)**: Balanced (Default: 12)
   - Natural slowdown
   - Smooth approach
   - Human-like deceleration

* **High (20-30)**: Early damping
   - Slows down far from target
   - Very cautious approach
   - May look hesitant

**Visual Effect**:

.. code-block:: text

   Low damped_dist (8):       Medium (12):         High (25):
        *=======>                  *=====>              *==>
        |||||||||                  ||||-->              ||---->
   -----o-------T            -----o-------T       -----o-------T
   (fast until close)       (gradual slow)      (early slowdown)

Why These Specific Constants?
------------------------------

You might wonder why the algorithm uses :math:`\\sqrt{3}` and :math:`\\sqrt{5}`:

**√3 ≈ 1.732** (Wind Damping)
   - Provides gradual decay of wind force
   - Balances persistence and decay
   - Empirically found to produce natural-looking curves
   - Fast enough to converge, slow enough to maintain influence

**√5 ≈ 2.236** (Wind Fluctuation & Velocity Reduction)
   - Scales random fluctuations appropriately
   - Prevents wind from overwhelming gravity
   - Creates smooth randomness rather than jitter
   - Also used for max_step reduction near target

These constants were likely chosen through experimentation to balance:
- Convergence speed
- Path naturalness
- Computational stability
- Aesthetic appeal

Algorithm Characteristics
-------------------------

Convergence Guarantee
^^^^^^^^^^^^^^^^^^^^^

The algorithm is **guaranteed to converge** to the target because:

1. Gravity always points toward target and doesn't decay
2. Wind decays over time (divided by √3 each step)
3. As distance decreases, wind becomes less effective
4. Close to target, only gravity remains (no new wind)

The stopping condition is ``distance < 1 pixel``, which is always eventually satisfied.

Non-Determinism
^^^^^^^^^^^^^^^

The algorithm is **non-deterministic** due to random wind fluctuations. Running it multiple times with the same parameters produces different paths.

This is a **feature**, not a bug:
- Prevents pattern recognition
- Mimics human inconsistency
- Makes bot detection harder

Scale Independence
^^^^^^^^^^^^^^^^^^

The algorithm works well across different screen resolutions and distances because:

- Parameters are pixel-based (scale-agnostic)
- Wind magnitude adapts to distance (``min(wind_magnitude, dist)``)
- Gravity is normalized by distance (``/ dist``)

However, you may want to tune parameters for very large distances (e.g., 4K displays) or very short distances (small UI elements).

Comparison to Other Algorithms
-------------------------------

Linear Interpolation
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Linear
   x = start_x + (dest_x - start_x) * t

**WindMouse advantages**:
- ✅ Non-linear paths
- ✅ Variable speed
- ✅ Unpredictable
- ❌ More computationally expensive

Bézier Curves
^^^^^^^^^^^^^

Bézier curves can create smooth paths but:

- ❌ Require predetermined control points
- ❌ Path is deterministic given control points
- ❌ No physical simulation
- ❌ Speed is uniform (unless manually varied)

**WindMouse advantages**:
- ✅ Physics-based (more natural)
- ✅ Emergent behavior
- ✅ No need to specify control points

Simplex/Perlin Noise
^^^^^^^^^^^^^^^^^^^^^

Noise functions can add randomness but:

- ❌ Don't inherently move toward target
- ❌ Require combining with directed movement
- ❌ May produce unnatural patterns

**WindMouse advantages**:
- ✅ Built-in target seeking
- ✅ Balanced randomness and purpose
- ✅ Complete solution in one algorithm

Implementation Details
-----------------------

Generator-Based Architecture
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``wind_mouse()`` function is a **generator**, yielding coordinates one at a time:

.. code-block:: python

   def wind_mouse(...) -> Generator[tuple[Coordinate, Coordinate], None, None]:
       # ...
       yield Coordinate(move_x), Coordinate(move_y)

**Benefits**:

- Memory efficient (doesn't store entire path)
- Allows real-time movement
- Can be interrupted mid-path
- Enables custom tick-based control

Coordinate Type Safety
^^^^^^^^^^^^^^^^^^^^^^

WindMouse uses ``NewType`` for coordinates:

.. code-block:: python

   Coordinate = NewType("Coordinate", int)

This provides type safety without runtime overhead, helping catch errors at type-check time.

Optimization Opportunities
--------------------------

For performance-critical applications, consider:

1. **Pre-compute sqrt(3) and sqrt(5)**: Already done in the library
2. **Use NumPy vectorization**: Already used for ``np.hypot()``
3. **Reduce tick_delay**: Set to 0 for maximum speed
4. **Reduce step_duration**: Use smaller values (0.01-0.05)
5. **Increase max_step**: Higher values = fewer total steps

Example optimized configuration:

.. code-block:: python

   from windmouse.pyautogui_controller import PyautoguiMouseController
   from windmouse import Coordinate

   mouse = PyautoguiMouseController(
       max_step=20,  # Increase speed
       gravity_magnitude=12,  # More direct
   )

   mouse.dest_position = (Coordinate(800), Coordinate(600))
   mouse.move_to_target(
       tick_delay=0,  # No delay
       step_duration=0.01  # Fast transitions
   )

Visualizing the Algorithm
--------------------------

To better understand the algorithm, you can visualize the path:

.. code-block:: python

   import matplotlib.pyplot as plt
   from windmouse.core import wind_mouse, Coordinate

   # Generate path
   path = list(wind_mouse(
       Coordinate(0), Coordinate(0),
       Coordinate(500), Coordinate(500),
       gravity_magnitude=9,
       wind_magnitude=3,
       max_step=15,
       damped_distance=12
   ))

   # Extract x and y coordinates
   xs, ys = zip(*path)

   # Plot
   plt.figure(figsize=(10, 10))
   plt.plot(xs, ys, 'b-', linewidth=1, alpha=0.7)
   plt.plot(xs[0], ys[0], 'go', markersize=10, label='Start')
   plt.plot(xs[-1], ys[-1], 'ro', markersize=10, label='End')
   plt.legend()
   plt.grid(True, alpha=0.3)
   plt.axis('equal')
   plt.title('WindMouse Path Visualization')
   plt.show()

Further Reading
---------------

For more information on human-computer interaction and mouse movement patterns:

* `Fitts's Law <https://en.wikipedia.org/wiki/Fitts%27s_law>`_ - Model of human movement
* `Motor Control Research <https://en.wikipedia.org/wiki/Motor_control>`_ - Neuroscience of movement
* `Bot Detection Techniques <https://en.wikipedia.org/wiki/Bot_detection>`_ - How automation is detected

Related Algorithms:

* Inverse Kinematics (robotics)
* Path smoothing algorithms
* Particle systems in computer graphics

Next Steps
----------

Now that you understand the algorithm, explore:

* The complete :doc:`api` reference
* Practical examples in :doc:`usage`
* Experiment with parameters to find optimal settings for your use case

