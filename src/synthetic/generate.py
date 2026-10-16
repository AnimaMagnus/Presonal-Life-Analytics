import numpy as np
import pandas as pd

seed = 42
n_days = 180
end_date = "2026-10-15"
rough_start = "2026-09-14"
rough_end = "2026-09-23"

rng = np.random.default_rng(seed)

def make_calendar(n_days, end_date):
    dates = pd.date_range(end = end_date, periods = n_days, freq = "D")
    cal = pd.DataFrame({"date": dates})
    cal["weekly"] = cal["date"].dt.dayofweek
    cal["is_weekend"] = cal["weekly"] >= 5
    cal["is_rough"] = cal["date"].between(rough_start, rough_end)
    return cal

def make_sleep(cal, rng):
    n = len(cal)
    baseline = 7.0
    weekend_bonus = 0.8
    rough_penalty = -1.2
    phi = 0.5
    sigma = 0.7

    ar = np.zeros(n)
    for t in range(1, n):
        ar[t] = phi * ar[t-1] + rng.normal(0, sigma)

    sleep = (
        baseline
        + weekend_bonus * cal["is_weekend"].to_numpy()
        + rough_penalty * cal["is_rough"].to_numpy()
        + ar
    )
    sleep = np.clip(sleep, 3.5, 11.0)
    return np.round(sleep, 1)

if __name__ == "__main__":
    cal = make_calendar(n_days, end_date)
    cal["sleep_hours"] = make_sleep(cal, rng)

    print(cal.head(10))
    print(cal.groupby("is_weekend")["sleep_hours"].mean())
    print(cal.groupby("is_rough")["sleep_hours"].mean())
    print("lag-1 autocorrelation:", cal["sleep_hours"].autocorr(lag=1))