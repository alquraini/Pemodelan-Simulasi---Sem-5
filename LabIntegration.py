"""
Lab Session 1 - Integration (Simulasi Monte Carlo)
Tugas 1-4: Solusi Numerik, Deteksi Min-Max, Metode Monte Carlo, Visualisasi

Fungsi   : f(x) = x^2
Interval : a = 0.0, b = 3.0
Steps/N  : 1,000,000
Seed     : 2
"""

import numpy as np
import matplotlib.pyplot as plt

# TASK 1: Numerical Solution
# 1. Pilih PRNG -> menggunakan numpy.random dengan Generator (PCG64)
# 2. Inisialisasi PRNG dengan seed tertentu
seed = 2
rng = np.random.default_rng(seed)

# 3. Definisikan fungsi dan batas integrasi
def f(x):
    return x ** 2

a = 0.0
b = 3.0
NumSteps = 1_000_000  # jumlah step untuk deteksi min-max

# Inisialisasi list untuk plotting nanti
x_curve = []
y_curve = []

# TASK 2: Min-max Detection
# 1. Set nilai awal ymin dan ymax = f(a)
ymin = f(a)
ymax = f(a)

# 2. Iterasi dari a ke b sebanyak NumSteps langkah, perbarui ymin/ymax
step_size = (b - a) / NumSteps
x = a
for i in range(NumSteps + 1):
    fx = f(x)
    if fx < ymin:
        ymin = fx
    if fx > ymax:
        ymax = fx
    x += step_size

print(f"[Task 2] ymin = {ymin:.6f}, ymax = {ymax:.6f}")

# TASK 3: Monte Carlo Method
# 1. Hitung luas persegi panjang pembatas (bounding box)
A = (b - a) * (ymax - ymin)

# 2. Inisialisasi jumlah titik acak N dan counter M
N = 1_000_000
M = 0

# 3 & 4. Bangkitkan titik acak (x, y) lalu cek apakah berada di bawah kurva
# Digunakan cara vektorisasi (numpy) agar 1 juta titik tetap cepat diproses,
# namun logikanya identik dengan pengecekan satu per satu di dalam loop.

x_rand = rng.uniform(a, b, N)
y_rand = rng.uniform(ymin, ymax, N)
under_curve_mask = y_rand <= f(x_rand)
M = int(np.sum(under_curve_mask))

# 5. Hitung integral numerik
numerical_integral = (M / N) * A

# Solusi analitik sebagai pembanding: integral x^2 dari 0 ke 3 = [x^3/3] = 9
exact_integral = (b ** 3 - a ** 3) / 3
error = abs(numerical_integral - exact_integral)
error_percent = (error / exact_integral) * 100

print(f"[Task 3] Luas bounding box (A)      = {A:.6f}")
print(f"[Task 3] Titik di bawah kurva (M)   = {M}")
print(f"[Task 3] Total titik (N)            = {N}")
print(f"[Task 3] Integral numerik (Monte Carlo) = {numerical_integral:.6f}")
print(f"[Task 3] Integral eksak (analitik)      = {exact_integral:.6f}")
print(f"[Task 3] Selisih absolut                = {error:.6f}")
print(f"[Task 3] Persentase error               = {error_percent:.4f}%")

# TASK 4: Visualization
# 1. Buat data untuk kurva fungsi menggunakan numpy.linspace
x_curve = np.linspace(a, b, 500)
y_curve = f(x_curve)

# Untuk menjaga plot tetap ringan/mudah dibaca, hanya sebagian titik acak
# (subset) yang ditampilkan -- perilaku Monte Carlo-nya tetap dihitung dari 1 juta titik.
plot_sample_size = 5000
sample_idx = rng.choice(N, size=plot_sample_size, replace=False)
x_sample = x_rand[sample_idx]
y_sample = y_rand[sample_idx]
under_sample = under_curve_mask[sample_idx]

plt.figure(figsize=(8, 6))

# 2. Plot kurva fungsi (merah)
plt.plot(x_curve, y_curve, color="red", linewidth=2, label="f(x) = x^2")

# Plot titik di bawah kurva (biru) dan di luar kurva (kuning)
plt.scatter(x_sample[under_sample], y_sample[under_sample],
            color="blue", s=3, label="Titik di bawah kurva")
plt.scatter(x_sample[~under_sample], y_sample[~under_sample],
            color="gold", s=3, label="Titik di luar kurva")

plt.title("Simulasi Monte Carlo untuk Integral Numerik f(x) = x^2")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.tight_layout()
plt.savefig("monte_carlo_plot.png", dpi=150)
plt.show()

print("\n[Task 4] Plot disimpan sebagai 'monte_carlo_plot.png'")