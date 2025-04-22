#include <iostream>
#include <vector>
#include <Eigen/Dense>
#include <Eigen/Sparse>
#include <Eigen/SparseLU>
#include <Eigen/Eigenvalues>

using namespace Eigen;
using namespace std;

int main() {
    // Исходные параметры
    double E = 200e9;     // Модуль упругости, Па
    double v = 0.3;       // Коэффициент Пуассона
    double rho = 7800;    // Плотность материала, кг/м³
    double delta = 0.01;  // Толщина пластины, м
    double a = 1;         // Длина пластины, м
    double b = 1;         // Ширина пластины, м
    int n = 100;          // Количество точек разбиения

    // Расчет цилиндрической жесткости
    double D = E * pow(delta, 3) / (12 * (1 - pow(v, 2)));

    // Создание векторов координат
    VectorXd x = VectorXd::LinSpaced(n, 0, a);
    VectorXd y = VectorXd::LinSpaced(n, 0, b);
    double dx = x(1) - x(0);
    double dy = y(1) - y(0);

    // Создание разреженных матриц жесткости и масс
    SparseMatrix<double> K(n * n, n * n);
    SparseMatrix<double> M(n * n, n * n);

    // Заполнение матрицы жесткости
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            int idx = i * n + j;

            if (i > 0) K.insert(idx, idx - n) = D / (dx * dx);
            if (i < n - 1) K.insert(idx, idx + n) = D / (dx * dx);
            if (j > 0) K.insert(idx, idx - 1) = D / (dy * dy);
            if (j < n - 1) K.insert(idx, idx + 1) = D / (dy * dy);

            K.insert(idx, idx) = -2 * D * (1 / (dx * dx) + 1 / (dy * dy));
        }
    }

    // Заполнение матрицы масс
    for (int i = 0; i < n * n; i++) {
        M.insert(i, i) = rho * delta * dx * dy;
    }

    // Решение задачи на собственные значения
    GeneralizedSelfAdjointEigenSolver<SparseMatrix<double>> eigSolver(K, M);
    VectorXd omega2 = eigSolver.eigenvalues();
    MatrixXcd W = eigSolver.eigenvectors();

    // Сортировка частот по возрастанию
    VectorXd omega = omega2.cwiseSqrt().real();
    VectorXi indices = VectorXi::LinSpaced(omega.size(), 0, omega.size() - 1);
    std::sort(indices.data(), indices.data() + indices.size(),
        [&omega](int i1, int i2) { return omega(i1) < omega(i2); });

    // Переупорядочивание частот и векторов
    VectorXd omega_sorted(omega.size());
    MatrixXcd W_sorted(W.rows(), W.cols());

    for (int i = 0; i < omega.size(); i++) {
        omega_sorted(i) = omega(indices(i));
        W_sorted.col(i) = W.col(indices(i));
    }

    // Вывод первой собственной частоты
    cout << "Первая собственная частота: " << omega_sorted(0) << " рад/с" << endl;

    // Вывод первой формы колебаний
    MatrixXd W1 = W_sorted.block(0, 0, n, n).real();
    cout << "Первая форма колебаний:" << endl;
    cout << W1 << endl;

    return 0;
}
