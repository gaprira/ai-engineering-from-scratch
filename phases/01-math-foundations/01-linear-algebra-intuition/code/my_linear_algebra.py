class Vector:
    """
    Вектор — это упорядоченный список чисел, представляющий точку
    или направление в n-мерном пространстве.
    """

    def __init__(self, components):
        self.components = list(components)
        self.dim = len(self.components)

    def __add__(self, other):
        """Сложение векторов: a + b"""
        if self.dim != other.dim:
            raise ValueError(
                f"Cannot add vectors of different dimensions: {self.dim} vs {other.dim}"
            )
        return Vector([a + b for a, b in zip(self.components, other.components)])

    def __sub__(self, other):
        """Вычитание векторов: a - b"""
        if self.dim != other.dim:
            raise ValueError(
                f"Cannot subtract vectors of different dimensions: {self.dim} vs {other.dim}"
            )
        return Vector([a - b for a, b in zip(self.components, other.components)])

    def __mul__(self, scalar):
        """Умножение на скаляр: c * v"""
        return Vector([scalar * x for x in self.components])

    def __rmul__(self, scalar):
        """Умножение на скаляр (справа): v * c"""
        return self.__mul__(scalar)

    def dot(self, other):
        """
        Скалярное произведение: a · b

        Геометрический смысл: мера похожести двух векторов.
        a · b = |a| × |b| × cos(θ)

        Где θ — угол между векторами.
        """
        if self.dim != other.dim:
            raise ValueError(
                f"Cannot compute dot product of vectors with different dimensions: {self.dim} vs {other.dim}"
            )
        return sum(a * b for a, b in zip(self.components, other.components))

    def magnitude(self):
        """
        Длина вектора (L2 норма).

        Формула: |v| = √(v₁² + v₂² + ... + vₙ²)
        """
        return sum(x**2 for x in self.components) ** 0.5

    def normalize(self):
        """
        Нормализация: превращает вектор в единичный (длины 1),
        сохраняя направление.

        Формула: v_normalized = v / |v|
        """
        mag = self.magnitude()
        if mag < 1e-10:
            raise ValueError("Cannot normalize zero vector")
        return Vector([x / mag for x in self.components])

    def cosine_similarity(self, other):
        """
        Косинусное сходство: нормализованная мера похожести.

        Диапазон: от -1 до 1
        - 1: векторы сонаправлены
        - 0: векторы перпендикулярны
        - -1: векторы противоположны

        Это основа векторного поиска в RAG!
        """
        mag_product = self.magnitude() * other.magnitude()
        if mag_product < 1e-10:
            raise ValueError("Cannot compute cosine similarity with zero vector")
        return self.dot(other) / mag_product

    def __repr__(self):
        return f"Vector({self.components})"


class Matrix:
    """
    Матрица — это прямоугольная таблица чисел, представляющая
    линейную трансформацию пространства.
    """

    def __init__(self, rows):
        self.rows = [list(row) for row in rows]
        self.shape = (len(self.rows), len(self.rows[0]))

    def __matmul__(self, other):
        """
        Матричное умножение: A @ B

        Правило: (строки A) × (столбцы B)
        Результат[i, j] = Σ(A[i, k] × B[k, j])
        """
        if isinstance(other, Vector):
            # Матрица × Вектор
            if self.shape[1] != other.dim:
                raise ValueError(
                    f"Incompatible shapes: matrix {self.shape} and vector dim {other.dim}"
                )

            return Vector(
                [
                    sum(
                        self.rows[i][j] * other.components[j]
                        for j in range(self.shape[1])
                    )
                    for i in range(self.shape[0])
                ]
            )

        elif isinstance(other, Matrix):
            # Матрица × Матрица
            if self.shape[1] != other.shape[0]:
                raise ValueError(
                    f"Incompatible shapes for matrix multiplication: {self.shape} and {other.shape}"
                )

            result_rows = []
            for i in range(self.shape[0]):
                row = []
                for j in range(other.shape[1]):
                    value = sum(
                        self.rows[i][k] * other.rows[k][j] for k in range(self.shape[1])
                    )
                    row.append(value)
                result_rows.append(row)

            return Matrix(result_rows)

        else:
            raise TypeError(f"Cannot multiply Matrix with {type(other)}")

    def transpose(self):
        """
        Транспонирование: строки становятся столбцами.

        A[i, j] → Aᵀ[j, i]
        """
        return Matrix(
            [
                [self.rows[j][i] for j in range(self.shape[0])]
                for i in range(self.shape[1])
            ]
        )

    def __repr__(self):
        rows_str = "\n  ".join(str(row) for row in self.rows)
        return f"Matrix(\n  {rows_str}\n)"


# ============================================================
# ТЕСТЫ И ПРИМЕРЫ
# ============================================================


def test_vectors():
    """Тест 1: Векторы и скалярное произведение"""
    print("=" * 70)
    print("ТЕСТ 1: Векторы и скалярное произведение")
    print("=" * 70)

    a = Vector([1, 2, 3])
    b = Vector([4, 5, 6])

    print(f"Вектор a: {a}")
    print(f"Вектор b: {b}")
    print(f"Сумма a + b: {a + b}")
    print(f"Разность a - b: {a - b}")
    print(f"Умножение на скаляр 2 * a: {2 * a}")
    print(f"Скалярное произведение a · b: {a.dot(b)}")
    print(f"Длина |a|: {a.magnitude():.4f}")
    print(f"Нормализованный a: {a.normalize()}")
    print(f"Косинусное сходство: {a.cosine_similarity(b):.4f}")
    print()


def test_similarity_search():
    """Тест 2: Векторный поиск (как в RAG!)"""
    print("=" * 70)
    print("ТЕСТ 2: Векторный поиск (основа RAG-систем)")
    print("=" * 70)

    # Запрос пользователя
    query = Vector([1, 0, 0])

    # База документов (эмбеддинги)
    doc1 = Vector([0.9, 0.1, 0.0])  # Похож на запрос
    doc2 = Vector([0.0, 1.0, 0.0])  # Перпендикулярен
    doc3 = Vector([-1.0, 0.0, 0.0])  # Противоположен

    documents = [("Документ 1", doc1), ("Документ 2", doc2), ("Документ 3", doc3)]

    print(f"Запрос: {query}")
    print("\nРанжирование документов по косинусному сходству:")

    # Вычисляем сходство и сортируем
    similarities = []
    for name, doc in documents:
        sim = query.cosine_similarity(doc)
        similarities.append((name, sim))

    # Сортируем по убыванию сходства
    similarities.sort(key=lambda x: x[1], reverse=True)

    for rank, (name, sim) in enumerate(similarities, 1):
        print(f"  {rank}. {name}: сходство = {sim:.4f}")

    print("\nЭто буквально то, как работает поиск в RAG!")
    print("Вектор запроса сравнивается с векторами документов.")
    print()


def test_matrix_transformations():
    """Тест 3: Матрицы как трансформации пространства"""
    print("=" * 70)
    print("ТЕСТ 3: Матрицы как трансформации пространства")
    print("=" * 70)

    # Матрица поворота на 90° против часовой стрелки
    rotation_90 = Matrix([[0, -1], [1, 0]])

    point = Vector([3, 1])
    rotated = rotation_90 @ point

    print(f"Исходная точка: {point}")
    print(f"Матрица поворота на 90°:\n{rotation_90}")
    print(f"После поворота: {rotated}")
    print()

    # Матрица масштабирования
    scale = Matrix([[2, 0], [0, 3]])

    scaled = scale @ point
    print(f"Матрица масштабирования (x×2, y×3):\n{scale}")
    print(f"После масштабирования: {scaled}")
    print()


def test_neural_network_layer():
    """Тест 4: Слой нейросети — это матричное умножение"""
    print("=" * 70)
    print("ТЕСТ 4: Слой нейросети = матричное умножение")
    print("=" * 70)

    import random

    random.seed(42)

    # Входной вектор (3 признака)
    x = Vector([1.0, 0.5, -0.3])

    # Матрица весов (2 нейрона, каждый принимает 3 входа)
    W = Matrix(
        [
            [random.gauss(0, 0.1) for _ in range(3)],  # Нейрон 1
            [random.gauss(0, 0.1) for _ in range(3)],  # Нейрон 2
        ]
    )

    # Вектор смещения
    b = Vector([0.0, 0.0])

    # Прямой проход: y = W @ x + b
    z = W @ x
    y = z + b  # type: ignore

    print(f"Входной вектор (3D): {x}")
    print(f"Матрица весов (2×3):\n{W}")
    print(f"Вектор смещения: {b}")
    print(f"Выходной вектор (2D): {y}")
    print("\nЭто то, что делает каждый полносвязный слой нейросети!")
    print("Обучение = подбор правильной матрицы W.")
    print()


def test_linear_independence():
    """Тест 5: Проверка линейной независимости"""
    print("=" * 70)
    print("ТЕСТ 5: Линейная независимость векторов")
    print("=" * 70)

    # Линейно независимые векторы (стандартный базис)
    v1 = Vector([1, 0, 0])
    v2 = Vector([0, 1, 0])
    v3 = Vector([0, 0, 1])

    print("Векторы:")
    print(f"  v1 = {v1}")
    print(f"  v2 = {v2}")
    print(f"  v3 = {v3}")
    print(f"Линейно независимы: {is_linearly_independent([v1, v2, v3])}")
    print()

    # Линейно зависимые векторы
    v4 = Vector([1, 1, 0])  # v4 = v1 + v2

    print("Добавляем v4 = v1 + v2:")
    print(f"  v4 = {v4}")
    print(f"Линейно независимы: {is_linearly_independent([v1, v2, v4])}")
    print("(v4 можно выразить через v1 и v2, поэтому зависимость)")
    print()


def is_linearly_independent(vectors):
    """
    Проверка линейной независимости набора векторов.

    Алгоритм: Гауссово исключение (приведение к ступенчатому виду).
    Если ранг матрицы = количеству векторов → независимы.
    """
    n = len(vectors)
    dim = len(vectors[0].components)

    # Создаем матрицу из векторов (каждый вектор = строка)
    mat = [v.components[:] for v in vectors]

    # Гауссово исключение
    rank = 0
    for col in range(dim):
        # Ищем опорный элемент (pivot)
        pivot = None
        for row in range(rank, len(mat)):
            if abs(mat[row][col]) > 1e-10:
                pivot = row
                break

        if pivot is None:
            continue  # В этом столбце нет ненулевых элементов

        # Меняем строки местами
        mat[rank], mat[pivot] = mat[pivot], mat[rank]

        # Нормализуем опорную строку
        scale = mat[rank][col]
        mat[rank] = [x / scale for x in mat[rank]]

        # Обнуляем элементы во всех других строках
        for row in range(len(mat)):
            if row != rank and abs(mat[row][col]) > 1e-10:
                factor = mat[row][col]
                mat[row] = [mat[row][j] - factor * mat[rank][j] for j in range(dim)]

        rank += 1

    # Независимы ⟺ ранг равен количеству векторов
    return rank == n


def project(a, b):
    """
    Проекция вектора a на вектор b.

    Геометрически: "тень" вектора a на направлении b.

    Формула: proj_b(a) = (a · b / b · b) × b
    """
    scalar = a.dot(b) / b.dot(b)
    return Vector([scalar * x for x in b.components])


def test_projection():
    """Тест 6: Проекция вектора на вектор"""
    print("=" * 70)
    print("ТЕСТ 6: Проекция вектора на вектор")
    print("=" * 70)

    a = Vector([3, 4])
    b = Vector([1, 0])  # Ось X

    proj = project(a, b)
    residual = a - proj

    print(f"Вектор a: {a}")
    print(f"Вектор b (направление): {b}")
    print(f"Проекция a на b: {proj}")
    print(f"Остаток (перпендикулярно b): {residual}")
    print(f"Проверка ортогональности: proj · residual = {proj.dot(residual):.6f}")
    print("\nПроекция — это основа линейной регрессии и PCA!")
    print()


def gram_schmidt(vectors):
    """
    Процесс Грама-Шмидта: превращает набор линейно независимых векторов
    в ортонормированный базис.

    Алгоритм:
    1. Берем первый вектор, нормализуем.
    2. Берем второй вектор, вычитаем проекцию на первый, нормализуем.
    3. Берем третий вектор, вычитаем проекции на все предыдущие, нормализуем.
    4. Повторяем.

    Результат: все векторы попарно ортогональны и имеют длину 1.
    """
    orthonormal = []

    for v in vectors:
        w = v

        # Вычитаем проекции на все уже найденные ортонормированные векторы
        for u in orthonormal:
            proj = project(w, u)
            w = w - proj

        # Проверяем, что вектор не нулевой
        if w.magnitude() < 1e-10:
            continue

        # Нормализуем
        orthonormal.append(w.normalize())

    return orthonormal


def test_gram_schmidt():
    """Тест 7: Процесс Грама-Шмидта"""
    print("=" * 70)
    print("ТЕСТ 7: Процесс Грама-Шмидта (ортонормализация)")
    print("=" * 70)

    v1 = Vector([1, 0, 0])
    v2 = Vector([1, 1, 0])
    v3 = Vector([1, 1, 1])

    print("Исходные векторы:")
    print(f"  v1 = {v1}")
    print(f"  v2 = {v2}")
    print(f"  v3 = {v3}")
    print()

    basis = gram_schmidt([v1, v2, v3])

    print("Ортонормированный базис:")
    for i, u in enumerate(basis):
        print(f"  u{i+1} = {u}")
        print(f"    |u{i+1}| = {u.magnitude():.6f}")

    print("\nПроверка ортогональности (все скалярные произведения должны быть 0):")
    print(f"  u1 · u2 = {basis[0].dot(basis[1]):.6f}")
    print(f"  u1 · u3 = {basis[0].dot(basis[2]):.6f}")
    print(f"  u2 · u3 = {basis[1].dot(basis[2]):.6f}")
    print("\nЭто основа QR-разложения и устойчивых численных методов!")
    print()


def main():
    """Запуск всех тестов"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "ЛИНЕЙНАЯ АЛГЕБРА С НУЛЯ" + " " * 31 + "║")
    print("║" + " " * 10 + "Фаза 1, Урок 1: Векторы и Матрицы" + " " * 24 + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    test_vectors()
    test_similarity_search()
    test_matrix_transformations()
    test_neural_network_layer()
    test_linear_independence()
    test_projection()
    test_gram_schmidt()

    print("=" * 70)
    print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    print("=" * 70)
    print("\nВы только что написали линейную алгебру с нуля.")
    print("Теперь вы понимаете, что происходит 'под капотом' NumPy и PyTorch.")
    print()


if __name__ == "__main__":
    main()
