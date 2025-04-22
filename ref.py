import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eig

# Исходные параметры
E = 200e9     # Модуль упругости, Па
J = 1e-8      # Момент инерции, м^4
m0 = 7800     # Масса на единицу длины, кг/м
L = 1         # Длина стержня, м
n = 100       # Количество точек разбиения

# Создание сетки координат
x = np.linspace(0, L, n)
dx = x[1] - x[0]

# Матрицы жесткости и масс
K = np.zeros((n, n))
M = np.zeros((n, n))

# Заполнение матрицы жесткости
for i in range(1, n-1):
    K[i, i-1] = 2*E*J/dx**4
    K[i, i] = -4*E*J/dx**4
    K[i, i+1] = 2*E*J/dx**4
K[0, 0] = K[n-1, n-1] = 0  # Учитываем граничные условия

# Заполнение матрицы масс
for i in range(n):
    M[i, i] = m0*dx

# Решение задачи на собственные значения
omega2, W = eig(K, M)
omega = np.sqrt(omega2)  # Собственные частоты

# Сортировка частот по возрастанию
idx = omega.argsort()
omega = omega[idx]
W = W[:, idx]

# Построение первых трех форм колебаний
plt.figure(figsize=(10, 6))
for i in range(3):
    plt.plot(x, W[:, i], label=f'Форма {i+1}, частота = {omega[i]:.2f} рад/с')
plt.title('Собственные формы колебаний стержня')
plt.xlabel('Положение по длине стержня, м')
plt.ylabel('Амплитуда')
plt.legend()
plt.grid()
plt.show()

# Вывод первых трех частот
print("Первые три собственные частоты:")
for i in range(3):
    print(f"Частота {i+1}: {omega[i]:.2f} рад/с")
