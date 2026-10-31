"""Jacobi iterative method for solving A*x = b."""


def jacobi(matrix, vector, initial_guess, tolerance, max_iterations):
    """Return the solution, status, error, and iteration table."""

    size = len(matrix)

    if size == 0 or len(vector) != size:
        raise ValueError("Matrix and vector dimensions do not match.")

    if len(initial_guess) != size:
        raise ValueError(
            "Initial guess dimensions do not match the matrix."
        )

    # التأكد من أن القطر الرئيسي ليس صفرًا
    for i in range(size):
        if abs(matrix[i][i]) < 1e-12:
            raise ValueError(
                "Jacobi cannot divide by a zero diagonal value."
            )

    x = [float(value) for value in initial_guess]

    rows = []

    for iteration in range(1, max_iterations + 1):

        x_new = [0.0] * size

        # حساب القيم الجديدة
        for i in range(size):

            sigma = sum(
                matrix[i][j] * x[j]
                for j in range(size)
                if j != i
            )

            x_new[i] = (
                vector[i] - sigma
            ) / matrix[i][i]

        # حساب أكبر خطأ
        error = max(
            abs(x_new[i] - x[i])
            for i in range(size)
        )

        # حفظ بيانات التكرار
        rows.append(
            [iteration] + x_new[:] + [error]
        )

        # التحقق من التقارب
        if error < tolerance:
            return {
                "solution": x_new,
                "iterations": iteration,
                "error": error,
                "status": "Converged",
                "table": rows
            }

        x = x_new

    return {
        "solution": x,
        "iterations": max_iterations,
        "error": error,
        "status": "Maximum iterations reached",
        "table": rows
    }