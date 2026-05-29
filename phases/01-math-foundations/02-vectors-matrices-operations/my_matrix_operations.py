import random


class Vector:
    """Вектор — упорядоченный список чисел."""

    def __init__(self, data):
        self.data = list(data)
        self.size = len(self.data)

    def __repr__(self):
        return f"Vector({self.data})"

    def __add__(self, other):
        """Сложение векторов."""
        if self.size != other.size:
            raise ValueError(f"Size mismatch: {self.size} vs {other.size}")
        return Vector([a + b for a, b in zip(self.data, other.data)])

    def __sub__(self, other):
        """Вычитание векторов."""
        if self.size != other.size:
            raise ValueError(f"Size mismatch: {self.size} vs {other.size}")
        return Vector([a - b for a, b in zip(self.data, other.data)])

    def __mul__(self, scalar):
        """Умножение на скаляр."""
        return Vector([x * scalar for x in self.data])

    def dot(self, other):
        """Скалярное произведение."""
        if self.size != other.size:
            raise ValueError(f"Size mismatch: {self.size} vs {other.size}")
        return sum(a * b for a, b in zip(self.data, other.data))

    def magnitude(self):
        """Длина вектора (L2 норма)."""
        return sum(x**2 for x in self.data) ** 0.5


class Matrix:

    def __init__(self, data):
        self.data = [list(row) for row in data]
        self.rows = len(self.data)
        self.cols = len(self.data[0]) if self.rows > 0 else 0
        self.shape = (self.rows, self.cols)

        # Проверка: все строки должны иметь одинаковую длину
        for i, row in enumerate(self.data):
            if len(row) != self.cols:
                raise ValueError(
                    f"Inconsistent row lengths: row 0 has {self.cols}, "
                    f"row {i} has {len(row)}"
                )

    def __repr__(self):
        rows_str = "\n  ".join(str(row) for row in self.data)
        return f"Matrix {self.shape}:\n  {rows_str}"

    def __add__(self, other):
        """Поэлементное сложение матриц."""
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
        return Matrix(
            [
                [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
                for i in range(self.rows)
            ]
        )

    def __sub__(self, other):
        """Поэлементное вычитание матриц."""
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
        return Matrix(
            [
                [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
                for i in range(self.rows)
            ]
        )

    def scalar_multiply(self, scalar):
        """Умножение матрицы на скаляр."""
        return Matrix(
            [
                [self.data[i][j] * scalar for j in range(self.cols)]
                for i in range(self.rows)
            ]
        )

    def element_wise_multiply(self, other):
        """
        Поэлементное умножение (Hadamard product).
        Требование: одинаковые формы.
        """
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
        return Matrix(
            [
                [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
                for i in range(self.rows)
            ]
        )

    def matmul(self, other):
        """
        Матричное умножение: self @ other.
        Требование: self.cols == other.rows
        """
        if self.cols != other.rows:
            raise ValueError(
                f"Inner dimensions must match for matmul: "
                f"{self.cols} vs {other.rows}"
            )

        result_data = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                # Скалярное произведение i-й строки self на j-й столбец other
                value = sum(
                    self.data[i][k] * other.data[k][j] for k in range(self.cols)
                )
                row.append(value)
            result_data.append(row)

        return Matrix(result_data)

    def transpose(self):
        """Транспонирование: строки ↔ столбцы."""
        return Matrix(
            [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        )

    def determinant(self):
        """
        Вычисление детерминанта (только для квадратных матриц).
        Использует рекурсивное разложение по первой строке.
        """
        if self.rows != self.cols:
            raise ValueError(
                f"Determinant only defined for square matrices, " f"got {self.shape}"
            )

        # Базовые случаи
        if self.shape == (1, 1):
            return self.data[0][0]

        if self.shape == (2, 2):
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]

        # Рекурсивное разложение по первой строке
        det = 0
        for j in range(self.cols):
            # Создаём минор (матрица без 0-й строки и j-го столбца)
            minor_data = [
                [self.data[i][k] for k in range(self.cols) if k != j]
                for i in range(1, self.rows)
            ]
            minor = Matrix(minor_data)

            # Чередуем знаки: +, -, +, -, ...
            sign = (-1) ** j
            det += sign * self.data[0][j] * minor.determinant()

        return det

    def inverse_2x2(self):
        """
        Обратная матрица для 2×2.
        Формула: (1/det) × [[d, -b], [-c, a]]
        """
        if self.shape != (2, 2):
            raise ValueError(
                f"inverse_2x2 only works for 2x2 matrices, got {self.shape}"
            )

        det = self.determinant()
        if abs(det) < 1e-10:
            raise ValueError(f"Matrix is singular (det={det:.2e}), no inverse exists")

        a, b = self.data[0][0], self.data[0][1]
        c, d = self.data[1][0], self.data[1][1]

        return Matrix([[d / det, -b / det], [-c / det, a / det]])

    @staticmethod
    def identity(n):
        """
        Создаёт единичную матрицу n×n.
        Использование: I = Matrix.identity(3)
        """
        return Matrix([[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)])

    import random


class DenseLayer:
    """
    Полносвязный слой нейросети.
    Forward pass: y = ReLU(W @ x + b)
    """

    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size

        # Xavier initialization
        std = (2 / (input_size + output_size)) ** 0.5
        self.weights = Matrix(
            [
                [random.gauss(0, std) for _ in range(input_size)]
                for _ in range(output_size)
            ]
        )

        # Bias = нули
        self.bias = Matrix([[0.0] for _ in range(output_size)])

    def forward(self, x):
        """
        Forward pass.
        x: Matrix shape (input_size, 1)
        return: Matrix shape (output_size, 1)
        """
        # Линейная трансформация: z = Wx + b
        z = self.weights.matmul(x) + self.bias

        # ReLU activation
        output = Matrix([[max(0.0, val) for val in row] for row in z.data])

        return output


class TwoLayerNet:
    """
    Двухслойная нейросеть:
    Input (3) → Hidden (4) → Output (2)
    """

    def __init__(self):
        self.layer1 = DenseLayer(input_size=3, output_size=4)
        self.layer2 = DenseLayer(input_size=4, output_size=2)

    def forward(self, x):
        h = self.layer1.forward(x)
        y = self.layer2.forward(h)
        return y


def run_tests():
    """Запуск всех тестов."""

    print("=" * 70)
    print("ТЕСТ 1: Основные операции с матрицами")
    print("=" * 70)

    A = Matrix([[1, 2], [3, 4]])
    B = Matrix([[5, 6], [7, 8]])

    print(f"A =\n{A}")
    print(f"\nB =\n{B}")
    print(f"\nA + B =\n{A + B}")
    print(f"\nA @ B (matrix multiply) =\n{A.matmul(B)}")
    print(f"\nA * B (element-wise) =\n{A.element_wise_multiply(B)}")
    print(f"\nAᵀ (transpose) =\n{A.transpose()}")
    print(f"\ndet(A) = {A.determinant()}")
    print(f"\nA⁻¹ (inverse) =\n{A.inverse_2x2()}")

    # Проверка: A @ A⁻¹ = I
    I_computed = A.matmul(A.inverse_2x2())
    print(f"\nA @ A⁻¹ (должно быть identity):\n{I_computed}")

    I_expected = Matrix.identity(2)
    print(f"\nI (expected):\n{I_expected}")

    print("\n" + "=" * 70)
    print("ТЕСТ 2: Dense Layer нейросети")
    print("=" * 70)

    layer = DenseLayer(input_size=3, output_size=2)
    x = Matrix([[0.5], [0.8], [-0.3]])

    print(f"Input: {x.data}")
    print(f"Weights shape: {layer.weights.shape}")
    print(f"Weights:\n{layer.weights}")
    print(f"Bias: {layer.bias.data}")

    y = layer.forward(x)
    print(f"\nOutput: {y.data}")
    print(f"Output shape: {y.shape}")

    print("\n" + "=" * 70)
    print("ТЕСТ 3: Двухслойная нейросеть")
    print("=" * 70)

    model = TwoLayerNet()
    x = Matrix([[1.0], [0.5], [-0.3]])
    y = model.forward(x)

    print(f"Input: {x.data}")
    print(f"Output after 2 layers: {y.data}")
    print(f"Shapes: {x.shape} → (4,) → {y.shape}")

    print("\n" + "=" * 70)
    print("ТЕСТ 4: Проверка детерминанта и обратной")
    print("=" * 70)

    # Тестируем 3 разные матрицы
    test_matrices = [
        Matrix([[1, 2], [3, 4]]),
        Matrix([[2, 1], [1, 3]]),
        Matrix([[0.5, -0.5], [0.5, 0.5]]),
    ]

    for i, M in enumerate(test_matrices):
        det = M.determinant()
        print(f"\nМатрица {i+1}:")
        print(f"M =\n{M}")
        print(f"det(M) = {det:.4f}")

        if abs(det) > 1e-10:
            M_inv = M.inverse_2x2()
            product = M.matmul(M_inv)
            print(f"M @ M⁻¹ =\n{product}")
            print("(должно быть близко к identity)")
        else:
            print("Матрица сингулярна, обратной не существует")

    print("\n" + "=" * 70)
    print("TEST 5: Сингулярная матрица (det = 0)")
    print("=" * 70)

    singular = Matrix([[1, 2], [2, 4]])
    print(f"Singular matrix:\n{singular}")
    print(f"det = {singular.determinant()}")

    try:
        singular.inverse_2x2()
        print("ОШИБКА: обратная не должна была вычислиться!")
    except ValueError as e:
        print(f"✓ Корректно выброшено исключение: {e}")


if __name__ == "__main__":
    run_tests()
