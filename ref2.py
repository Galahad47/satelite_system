import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh

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

# Создание разреженных матриц
data_K = []
rows_K = []
cols_K = []
data_M = []
rows_M = []
cols_M = []

# Заполнение матриц
for i in range(n):
    for j in range(n):
        idx = i * n + j
        
        if i > 0:
            rows_K.append(idx); cols_K.append(idx-n); data_K.append(D / dx**2)
        if i < n-1:
            rows_K.append(idx); cols_K.append(idx+n); data_K.append(D / dx**2)
        if j > 0:
            rows_K.append(idx); cols_K.append(idx-1); data_K.append(D / dy**2)
        if j < n-1:
            rows_K.append(idx); cols_K.append(idx+1); data_K.append(D / dy**2)
            
        rows_K.append(idx); cols_K.append(idx); data_K.append(-2 * D * (1/dx**2 + 1/dy**2))
        
        rows_M.append(idx); cols_M.append(idx); data_M.append(rho * delta * dx * dy)

# Создание разреженных матриц
K = csr_matrix((data_K, (rows_K, cols_K)), shape=(n*n, n*n))
M = csr_matrix((data_M, (rows_M, cols_M)), shape=(n*n, n*n))

# Решение задачи на собственные значения
# Используем только 6 наименьших собственных значений
omega2, W = eigsh(K, 6, M=M, which='SM')
omega = np.sqrt(np.abs(omega2))  # Собственные частоты

# Сортировка частот по возрастанию
idx = omega.argsort()
omega = omega[idx]
W = W[:, idx]

# Построение первой формы колебаний
W1 = W[:, 0].reshape((n, n))
plt.figure(figsize=(10, 6))
plt.imshow(W1, cmap='viridis')
plt.title(f'Первая собственная форма колебаний (частота = {omega[0]:.2f} Гц)')
plt.colorbar()
plt.show()

print(f"Первые собственные частоты: {omega[:5]} Гц")
