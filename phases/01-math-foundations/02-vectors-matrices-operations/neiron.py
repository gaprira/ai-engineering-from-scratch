import random


class Neuron:
    """
    Простой нейрон с функцией активации ReLU.
    """

    def __init__(self, input_size):
        # Инициализируем веса случайными числами
        self.weights = [random.uniform(-1, 1) for _ in range(input_size)]
        # Смещение (bias)
        self.bias = random.uniform(-1, 1)

    def forward(self, inputs):
        """
        Прямой проход: вычисляет выход нейрона.

        inputs: список чисел (входные данные)
        return: одно число (выход нейрона)
        """

        # Шаг 1: Умножаем каждый вход на свой вес и складываем
        z = sum(w * x for w, x in zip(self.weights, inputs)) + self.bias

        # Шаг 2: Применяем функцию активации ReLU
        output = max(0, z)  # Если z > 0, возвращаем z, иначе 0

        return output


# === Пример использования ===

# Создаём нейрон с 3 входами
neuron = Neuron(input_size=3)

# Входные данные
inputs = [1.0, 0.5, -0.3]

# Прямой проход
output = neuron.forward(inputs)

print(f"Входы: {inputs}")
print(f"Веса: {neuron.weights}")
print(f"Смещение: {neuron.bias:.4f}")
print(f"Выход: {output:.4f}")
