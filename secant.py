"""Secant method for solving f(x) = 0."""


def secant(function, x0, x1, tolerance, max_iterations):
    """Return the approximate root and the real iteration data for Secant method."""
    rows = []
    error = abs(x1 - x0)

    for iteration in range(1, max_iterations + 1):
        f_x0 = function(x0)
        f_x1 = function(x1)

        if f_x1 - f_x0 == 0:
            raise ValueError("Secant Method produced a zero denominator.")

        # قانون طريقة القاطع
        x2 = x1 - (f_x1 * (x1 - x0)) / (f_x1 - f_x0)
        f_x2 = function(x2)
        error = abs(x2 - x1)

        rows.append((iteration, x0, x1, x2, f_x2, error))

        if abs(f_x2) < tolerance or error < tolerance:
            return {
                "root": x2,
                "iterations": iteration,
                "error": error,
                "status": "Converged",
                "table": rows
            }

        x0, x1 = x1, x2

    return {
        "root": x1,
        "iterations": max_iterations,
        "error": error,
        "status": "Maximum iterations reached",
        "table": rows
    }