import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "Bank Central Asia (BBCA) Historical Data.csv")

# 1. Load & bersihkan data historis
df = pd.read_csv(csv_path)
df.columns = [c.strip() for c in df.columns]
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
df["Price"] = df["Price"].str.replace(",", "").astype(float)
df = df.sort_values("Date").reset_index(drop=True)

print("Data range:", df["Date"].min().date(), "to", df["Date"].max().date())
print("Number of trading days:", len(df))
print(df[["Date","Price"]].to_string(index=False))

# 2. Hitung log-return -> drift & volatilitas 
prices = df["Price"].values
log_returns = np.diff(np.log(prices))

mu_daily = log_returns.mean()
sigma_daily = log_returns.std(ddof=1)

mu_annual = mu_daily * 252
sigma_annual = sigma_daily * np.sqrt(252)

print(f"\nDaily drift (mu):        {mu_daily:.6f}")
print(f"Daily volatility (sigma): {sigma_daily:.6f}")
print(f"Annualized drift:        {mu_annual:.4f}")
print(f"Annualized volatility:   {sigma_annual:.4f}")

# 3. Simulasi Monte Carlo: Geometric Brownian Motion
S0 = prices[-1]
T_days = 30
n_sims = 10000
np.random.seed(42)
dt = 1

drift = (mu_daily - 0.5 * sigma_daily**2) * dt
Z = np.random.standard_normal((n_sims, T_days))
daily_log_returns = drift + sigma_daily * np.sqrt(dt) * Z

log_paths = np.cumsum(daily_log_returns, axis=1)
price_paths = S0 * np.exp(log_paths)
price_paths_full = np.hstack([np.full((n_sims,1), S0), price_paths])

# 4. Hasil hari ke-30
final_prices = price_paths[:, -1]
mean_final = final_prices.mean()
median_final = np.median(final_prices)
p5, p95 = np.percentile(final_prices, [5, 95])
std_final = final_prices.std()

print(f"\n--- Simulation results ({n_sims} paths, {T_days} trading days ahead) ---")
print(f"Starting price (S0):      {S0:,.0f}")
print(f"Mean simulated price:     {mean_final:,.0f}")
print(f"Median simulated price:   {median_final:,.0f}")
print(f"Std dev of final price:   {std_final:,.0f}")
print(f"5th percentile:           {p5:,.0f}")
print(f"95th percentile:          {p95:,.0f}")
print(f"P(price > S0) at day 30:  {(final_prices > S0).mean()*100:.1f}%")

# 5. Visualisasi
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

n_show = 100
for i in range(n_show):
    axes[0].plot(price_paths_full[i], linewidth=0.6, alpha=0.5)
axes[0].plot(price_paths_full[:n_show].mean(axis=0), color="black", linewidth=2, label="Mean path (sampel)")
axes[0].axhline(S0, color="red", linestyle="--", linewidth=1, label=f"S0 = {S0:,.0f}")
axes[0].set_title(f"Simulated BBCA Price Paths (showing {n_show} of {n_sims})")
axes[0].set_xlabel("Trading days ahead"); axes[0].set_ylabel("Price (IDR)")
axes[0].legend()

axes[1].hist(final_prices, bins=60, color="steelblue", edgecolor="white")
axes[1].axvline(S0, color="red", linestyle="--", label=f"S0 = {S0:,.0f}")
axes[1].axvline(mean_final, color="black", linestyle="-", label=f"Mean = {mean_final:,.0f}")
axes[1].axvline(p5, color="orange", linestyle=":", label=f"5th pct = {p5:,.0f}")
axes[1].axvline(p95, color="orange", linestyle=":", label=f"95th pct = {p95:,.0f}")
axes[1].set_title(f"Distribution of Price after {T_days} Trading Days")
axes[1].set_xlabel("Price (IDR)"); axes[1].set_ylabel("Frequency")
axes[1].legend(fontsize=8)

plt.tight_layout()
plt.savefig("case2_bbca_mc.png", dpi=130)
plt.show()
print("\nSaved plot: case2_bbca_mc.png")