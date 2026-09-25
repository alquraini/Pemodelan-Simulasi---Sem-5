import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# 1. Simulasi dua dadu 
n_trials = 1_000_000
die1 = np.random.randint(1, 7, n_trials)
die2 = np.random.randint(1, 7, n_trials)
sums = die1 + die2

sim_probs = {s: np.mean(sums == s) for s in range(2, 13)}
combo_counts = {2:1,3:2,4:3,5:4,6:5,7:6,8:5,9:4,10:3,11:2,12:1}
theo_probs = {s: c/36 for s, c in combo_counts.items()}

print(f"--- Probabilitas sum dua dadu ({n_trials:,} trial) ---")
print(f"{'Sum':>4} | {'Simulasi':>10} | {'Teoretis':>10} | {'Selisih':>8}")
for s in range(2, 13):
    print(f"{s:>4} | {sim_probs[s]*100:9.3f}% | {theo_probs[s]*100:9.3f}% | {(sim_probs[s]-theo_probs[s])*100:+7.3f}%")

# 2. Simulasi craps
def play_craps():
    d = np.random.randint(1, 7, 2)
    point_roll = d[0] + d[1]
    if point_roll in (7, 11):
        return True
    if point_roll in (2, 3, 12):
        return False
    point = point_roll
    while True:
        d = np.random.randint(1, 7, 2)
        roll = d[0] + d[1]
        if roll == point:
            return True
        if roll == 7:
            return False

n_games = 200_000
results = np.array([play_craps() for _ in range(n_games)])
win_rate = results.mean()

print(f"\n--- Simulasi Craps ({n_games:,} game) ---")
print(f"Win rate simulasi: {win_rate*100:.3f}%")
print(f"Win rate teoretis:  {244/495*100:.3f}% (= 244/495)")

# 3. Visualisasi
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

sums_range = list(range(2, 13))
x = np.arange(len(sums_range))
width = 0.35
axes[0].bar(x - width/2, [sim_probs[s]*100 for s in sums_range], width, label="Simulasi", color="steelblue")
axes[0].bar(x + width/2, [theo_probs[s]*100 for s in sums_range], width, label="Teoretis", color="orange", alpha=0.8)
axes[0].set_xticks(x); axes[0].set_xticklabels(sums_range)
axes[0].set_xlabel("Sum dua dadu"); axes[0].set_ylabel("Probabilitas (%)")
axes[0].set_title(f"Sum Dua Dadu: Simulasi vs Teoretis\n({n_trials:,} trial)")
axes[0].legend()

axes[1].bar(["Menang", "Kalah"], [win_rate*100, (1-win_rate)*100], color=["seagreen", "indianred"])
axes[1].axhline(244/495*100, color="black", linestyle="--", label=f"Teoretis = {244/495*100:.2f}%")
axes[1].set_ylabel("Probabilitas (%)")
axes[1].set_title(f"Craps: Hasil Shooter\n({n_games:,} game)")
axes[1].legend()

plt.tight_layout()
plt.savefig("case4_dice_mc.png", dpi=130)
plt.show()