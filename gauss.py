"""Gaussian elimination method for A*x = b."""


def gauss(matrix, vector):
    """Return the solution and readable Gaussian elimination steps."""

    size = len(matrix)

    if size == 0 or len(vector) != size:
        raise ValueError("Matrix and vector dimensions do not match.")

    if any(len(row) != size for row in matrix):
        raise ValueError("Matrix must be square.")

    # إنشاء نسخة حتى لا نغير البيانات الأصلية
    augmented = [
        [float(value) for value in matrix[i]] + [float(vector[i])]
        for i in range(size)
    ]

    operations = []

    # -----------------------------
    # Forward Elimination
    # -----------------------------
    for i in range(size):

        # اختيار أكبر pivot
        pivot_row = max(
            range(i, size),
            key=lambda r: abs(augmented[r][i])
        )

        if abs(augmented[pivot_row][i]) < 1e-12:
            raise ValueError(
                "The matrix is singular and has no unique solution."
            )

        # تبديل الصفوف عند الحاجة
        if pivot_row != i:
            augmented[i], augmented[pivot_row] = (
                augmented[pivot_row],
                augmented[i]
            )

            operations.append({
                "step": len(operations) + 1,
                "operation": f"R{i + 1} <-> R{pivot_row + 1}",
                "matrix": [row[:] for row in augmented]
            })

        # حذف العناصر الموجودة تحت المحور
        for j in range(i + 1, size):

            factor = augmented[j][i] / augmented[i][i]

            if abs(factor) < 1e-12:
                continue

            for k in range(i, size + 1):
                augmented[j][k] -= factor * augmented[i][k]

            operations.append({
                "step": len(operations) + 1,
                "operation": (
                    f"R{j + 1} <- R{j + 1} - "
                    f"({factor:.6g})R{i + 1}"
                ),
                "matrix": [row[:] for row in augmented]
            })

    # -----------------------------
    # Back Substitution
    # -----------------------------
    solution = [0.0] * size

    for i in range(size - 1, -1, -1):

        if abs(augmented[i][i]) < 1e-12:
            raise ValueError(
                "The matrix is singular and has no unique solution."
            )

        total = augmented[i][size]

        for j in range(i + 1, size):
            total -= augmented[i][j] * solution[j]

        solution[i] = total / augmented[i][i]

    return {
        "solution": solution,
        "matrix": augmented,
        "operations": operations
    }