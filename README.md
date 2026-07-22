===============================================================================
PROJECT: Plastic Ratio Computation Engine
===============================================================================

OVERVIEW:
Calculates the Plastic Ratio (rho ≈ 1.32471795724474602596...) to arbitrary 
precision (N digits). The Plastic ratio is the 3D analogue of the Golden ratio, 
representing the limiting ratio of Padovan and Perrin sequence terms.

ALGORITHM & MATHEMATICS:
- Newton-Raphson Cubic Root Solving:
    f(x) = x^3 - x - 1 = 0
    f'(x) = 3*x^2 - 1
- Dynamic Precision Doubling: Quadruples execution speed by doubling mpmath working 
  precision each iteration step.
