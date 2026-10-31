"""Newton-Raphson method."""


def newton_raphson(function, derivative, x0, tolerance, max_iterations):
	"""Return the approximate root and the real iteration data."""
	rows = []
	x = x0
	error = float("inf")

	for iteration in range(1, max_iterations + 1):
		fx = function(x)
		dfx = derivative(x)
		if dfx == 0:
			raise ZeroDivisionError("Newton-Raphson derivative is zero.")

		next_x = x - fx / dfx
		error = abs(next_x - x)
		rows.append((iteration, x, fx, dfx, error))

		if error < tolerance or abs(function(next_x)) < tolerance:
			return {"root": next_x, "iterations": iteration, "error": error,
					"status": "Converged", "table": rows}
		x = next_x

	return {"root": x, "iterations": max_iterations, "error": error,
			"status": "Maximum iterations reached", "table": rows}
