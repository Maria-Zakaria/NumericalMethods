"""Bisection method for solving f(x) = 0."""


def bisection(function, a, b, tolerance, max_iterations):
	"""Return the approximate root and the real iteration data."""
	fa = function(a)
	fb = function(b)

	if fa == 0:
		return {"root": a, "iterations": 0, "error": 0.0,
				"status": "Converged", "table": []}
	if fb == 0:
		return {"root": b, "iterations": 0, "error": 0.0,
				"status": "Converged", "table": []}
	if fa * fb > 0:
		raise ValueError("Bisection Method requires opposite signs at a and b.")

	rows = []
	previous_c = None
	c = a
	error = abs(b - a)

	for iteration in range(1, max_iterations + 1):
		c = (a + b) / 2
		fc = function(c)
		error = abs(c - previous_c) if previous_c is not None else abs(b - a)
		rows.append((iteration, a, b, c, fc, error))

		if fc == 0 or abs(b - a) < tolerance or error < tolerance:
			return {"root": c, "iterations": iteration, "error": error,
					"status": "Converged", "table": rows}

		if fa * fc < 0:
			b, fb = c, fc
		else:
			a, fa = c, fc
		previous_c = c

	return {"root": c, "iterations": max_iterations, "error": error,
			"status": "Maximum iterations reached", "table": rows}
