"""Numerical differentiation method (Forward difference)."""


def differentiation(function, x0, h):
    """Calculate the first derivative numerically using forward difference formula."""
    if h == 0:
        raise ValueError("Step size h cannot be zero.")
    
    derivative_value = (function(x0 + h) - function(x0)) / h
    
    return {"derivative": derivative_value}