"""
Linear Algebra from Scratch
Фаза 1, Урок 1: Пишем векторы и матрицы своими руками
"""


class Vector:
    """Вектор — это просто список чисел (координаты точки в пространстве)"""

    def __init__(self, components):
        self.components = list(components)
        self.dim = len(self.components)  # Размерность (2D, 3D, 768D и т.д.)

    def __add__(self, other):
        """Сложение векторов: складываем соответствующие координаты"""
        return Vector([a + b for a, b in zip(self.components, other.components)])

    def dot(self, other):
        """Скалярное произведение: мера похожести двух векторов"""
        # Умножаем соответствующие координаты и суммируем
        return sum(a * b for a, b in zip(self.components, other.components))

    def magnitude(self):
        """Длина вектора (по теореме Пифагора)"""
        return sum(x**2 for x in self.components) ** 0.5

    def cosine_similarity(self, other):
        """Косинусное сходство: нормализованная мера похожести (от -1 до 1)"""
        return self.dot(other) / (self.magnitude() * other.magnitude())

    def __repr__(self):
        return f"Vector({self.components})"


# === ТЕСТ 1: Векторы ===
print("=" * 60)
print("ТЕСТ 1: Векторы и скалярное произведение")
print("=" * 60)

a = Vector([1, 2, 3])
b = Vector([4, 5, 6])

print(f"Вектор a: {a}")
print(f"Вектор b: {b}")
print(f"Сумма a + b: {a + b}")
print(f"Скалярное произведение a · b: {a.dot(b)}")
print(f"Длина |a|: {a.magnitude():.4f}")
print(f"Косинусное сходство: {a.cosine_similarity(b):.4f}")
print()

# === ТЕСТ 2: Похожие и непохожие векторы ===
print("=" * 60)
print("ТЕСТ 2: Поиск похожих векторов (как в RAG!)")
print("=" * 60)

query = Vector([1, 0, 0])  # Запрос
doc1 = Vector([0.9, 0.1, 0])  # Документ 1 (похож)
doc2 = Vector([0, 1, 0])  # Документ 2 (не похож)
doc3 = Vector([-1, 0, 0])  # Документ 3 (противоположен)

print(f"Запрос: {query}")
print(f"Сходство с doc1: {query.cosine_similarity(doc1):.4f} (высокое)")
print(f"Сходство с doc2: {query.cosine_similarity(doc2):.4f} (низкое)")
print(f"Сходство с doc3: {query.cosine_similarity(doc3):.4f} (отрицательное)")
print("Это основа векторного поиска в RAG!")
