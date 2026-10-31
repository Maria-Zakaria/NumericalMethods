"""Lagrange interpolation method."""


def lagrange(points, x_target):
    """Calculate the interpolated value using Lagrange interpolation."""

    n = len(points)

    if n == 0:
        raise ValueError(
            "No points provided for Lagrange interpolation."
        )

    # التأكد من عدم تكرار قيم x
    x_values = [point[0] for point in points]

    if len(set(x_values)) != len(x_values):
        raise ValueError(
            "Duplicate x values found in interpolation points."
        )

    total_sum = 0.0
    table = []

    for i in range(n):

        xi, yi = points[i]

        li = 1.0

        # حساب L_i(x)
        for j in range(n):

            if i != j:

                xj, _ = points[j]

                li *= (
                    (x_target - xj)
                    / (xi - xj)
                )

        term = yi * li

        total_sum += term

        table.append([
            i + 1,
            xi,
            yi,
            li,
            term
        ])

    return {
        "value": total_sum,
        "table": table
    }