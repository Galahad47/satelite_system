import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eig

# Исходные параметры
E = 200e9     # Модуль упругости, Па
v = 0.3       # Коэффициент Пуассона
rho = 7800    # Плотность материала, кг/м³
delta = 0.01  # Толщина пластины, м
a = 1         # Длина пластины, м
b = 1         # Ширина пластины, м
n = 100       # Количество точек разбиения

# Расчет цилиндрической жесткости
D = E * delta**3 / (12 * (1 - v**2))


x = np.linspace(0, a, n)
y = np.linspace(0, b, n)
dx = x[1] - x[0]
dy = y[1] - y[0]

# Матрицы жесткости и масс
K = np.zeros((n*n, n*n))
M = np.zeros((n*n, n*n))

for i in range(n):
    for j in range(n):
        idx = i * n + j

        if i > 0:
            K[idx, idx-n] = D / dx**2
        if i < n-1:
            K[idx, idx+n] = D / dx**2
        if j > 0:
            K[idx, idx-1] = D / dy**2
        if j < n-1:
            K[idx, idx+1] = D / dy**2
            
        K[idx, idx] = -2 * D * (1/dx**2 + 1/dy**2)

# Заполнение матрицы масс
for i in range(n*n):
    M[i, i] = rho * delta * dx * dy

# Решение задачи на собственные значения
omega2, W = eig(K, M)
omega = np.sqrt(omega2)  # Собственные частоты

# Сортировка частот по возрастанию
idx = omega.argsort()
omega = omega[idx]
W = W[:, idx]

# Построение первой формы колебаний
W1 = W[:, 0].reshape((n, n))
plt.figure(figsize=(10, 6))
plt.imshow(W1, cmap='viridis')
plt.title(f'Первая собственная форма колебаний (частота = {omega[0]:.2f} рад/с)')
plt.colorbar()
plt.show()

print(f"Первая собственная частота: {omega[0]:.2f} рад/с")
