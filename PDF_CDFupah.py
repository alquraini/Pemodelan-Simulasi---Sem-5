"""
Analisis PDF & CDF Distribusi Lognormal
Dataset: Rata-Rata Upah Pekerja Per Jam (35 Provinsi, 2015-2022)
Parameter hasil fitting (SciPy): mu = 9.687, sigma = 0.249
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 1. Parameter hasil fitting distribusi Lognormal

mu = 9.687        # parameter lokasi (skala log)
sigma = 0.249      # parameter skala (skala log)

# scipy.stats.lognorm menggunakan parameterisasi: s=sigma, scale=exp(mu)
dist = stats.lognorm(s=sigma, scale=np.exp(mu))

# 2. Titik-titik kritis (verifikasi manual vs scipy)

median_teoretis = np.exp(mu)                 # F(x) = 0.50
p90 = dist.ppf(0.90)                          # F(x) = 0.90

print("=== Titik Kritis Distribusi ===")
print(f"Median teoretis (F=0.50) : Rp {median_teoretis:,.2f}")
print(f"Persentil 90   (F=0.90)  : Rp {p90:,.2f}")
print(f"Mean teoretis            : Rp {dist.mean():,.2f}")
print(f"Std Dev teoretis         : Rp {dist.std():,.2f}")

# Contoh probabilitas kumulatif tambahan
for x_val in [15000, 20000, 25000]:
    print(f"P(X <= {x_val:,}) = {dist.cdf(x_val):.4f}")

# 3. Rentang nilai x untuk plotting

x = np.linspace(1, 35000, 2000)
pdf_vals = dist.pdf(x)
cdf_vals = dist.cdf(x)

# 4. Plot PDF (dengan area shading)

fig1, ax1 = plt.subplots(figsize=(6, 4.2))
ax1.plot(x, pdf_vals, color="#2E86C1", linewidth=2, label="Kurva Kerapatan Peluang (PDF)")
ax1.fill_between(x, pdf_vals, color="#2E86C1", alpha=0.2)
ax1.set_title("Probability Density Function (PDF)\nKerapatan Peluang Upah per Jam")
ax1.set_xlabel("Upah per Jam (Rp)")
ax1.set_ylabel("Kepadatan (Density)")
ax1.legend()
ax1.grid(alpha=0.3)
fig1.tight_layout()
fig1.savefig("pdf_plot.png", dpi=150)

# 5. Plot CDF (S-curve dengan marker median & P90)

fig2, ax2 = plt.subplots(figsize=(6, 4.2))
ax2.plot(x, cdf_vals, color="#C0392B", linewidth=2, label="Probabilitas Kumulatif (CDF)")
ax2.axhline(0.5, color="gray", linestyle="--", linewidth=0.8)
ax2.axhline(0.9, color="gray", linestyle="--", linewidth=0.8)

ax2.plot(median_teoretis, 0.5, "o", color="green", markersize=8,
          label=f"Median: Rp {median_teoretis:,.0f}")
ax2.plot(p90, 0.9, "o", color="orange", markersize=8,
          label=f"Persentil 90: Rp {p90:,.0f}")

ax2.set_title("Cumulative Distribution Function (CDF)\nKurva Probabilitas Kumulatif S-Curve")
ax2.set_xlabel("Upah per Jam (Rp)")
ax2.set_ylabel("Kumulatif P(X <= x)")
ax2.set_ylim(0, 1.05)
ax2.legend(loc="lower right")
ax2.grid(alpha=0.3)
fig2.tight_layout()
fig2.savefig("cdf_plot.png", dpi=150)

print("\nGrafik tersimpan: pdf_plot.png, cdf_plot.png")