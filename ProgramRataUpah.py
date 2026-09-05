"""
Program: Histogram & Uji Kevalidan Distribusi Data Upah Pekerja Per Jam
Dataset: upah.df.csv (Rata-Rata Upah Pekerja Per Jam per Provinsi, 2015-2022)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 1. Load data
df = pd.read_csv('upah.df.csv')
x = df['upah'].values

print("Jumlah data:", len(x))
print("Mean:", x.mean(), "| Std:", x.std(ddof=1), "| Skewness:", stats.skew(x))

# 2. Fit distribusi Normal dan Lognormal
mu_n, sigma_n = stats.norm.fit(x)
shape, loc, scale = stats.lognorm.fit(x, floc=0)
mu_ln, sigma_ln = np.log(scale), shape

# 3. Uji kevalidan (Goodness-of-Fit) pakai Kolmogorov-Smirnov Test
ks_normal = stats.kstest(x, stats.norm(loc=mu_n, scale=sigma_n).cdf)
ks_lognorm = stats.kstest(x, stats.lognorm(shape, loc=loc, scale=scale).cdf)

print("\n--- Uji Kolmogorov-Smirnov ---")
print(f"Normal   : statistic={ks_normal.statistic:.4f}, p-value={ks_normal.pvalue:.4f}")
print(f"Lognormal: statistic={ks_lognorm.statistic:.4f}, p-value={ks_lognorm.pvalue:.4f}")
print("\n(p-value > 0.05 -> gagal tolak H0 -> data konsisten dengan distribusi tsb)")

# 4. Plot histogram + kurva fit
xs = np.linspace(x.min(), x.max(), 500)
plt.figure(figsize=(8,5))
plt.hist(x, bins=20, density=True, color='#4C72B0', alpha=0.7, edgecolor='white', label='Data upah (histogram)')
plt.plot(xs, stats.lognorm.pdf(xs, shape, loc, scale), color='#C44E52', lw=2.5,
         label=f'Lognormal fit (mu={mu_ln:.3f}, sigma={sigma_ln:.3f})')
plt.plot(xs, stats.norm.pdf(xs, mu_n, sigma_n), color='#55A868', lw=2, ls='--',
         label=f'Normal fit (mu={mu_n:.0f}, sigma={sigma_n:.0f})')
plt.title('Distribusi Rata-Rata Upah Pekerja Per Jam (35 Provinsi, 2015-2022)')
plt.xlabel('Upah per jam (Rp)')
plt.ylabel('Densitas')
plt.legend()
plt.tight_layout()
plt.savefig('histogram_upah.png', dpi=150)
plt.show()