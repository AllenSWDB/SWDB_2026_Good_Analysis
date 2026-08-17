"""
generate_data.py
Generate simulated neural data for Mini-Workshop 4: Co-modulation or coincidental drift?

Run this script once to create the data/ folder and save the simulation outputs.
The notebook then loads from data/ rather than regenerating on every run.

Usage:
    python generate_data.py
"""

import numpy as np
from scipy.ndimage import gaussian_filter1d
from pathlib import Path

# ── Parameters ────────────────────────────────────────────────────────────────
SEED        = 7            # master random seed — keep fixed to reproduce figures

N_NEURONS   = 100
N_BLOCKS    = 10           # task blocks in the session
BLOCK_LEN   = (30, 70)     # trials per block, drawn uniformly (inclusive)
TRIAL_DUR   = 1.0          # s, duration of one trial
DT          = 0.005        # s, bin width for spike generation (5 ms)

FLUCT_TAU   = 25.0         # s, timescale of each neuron's slow rate fluctuation
PUPIL_TAU   = 20.0         # s, timescale of the pupil fluctuation
RATE_BASE   = (2.0, 9.0)   # spikes/s, each neuron's mean rate (drawn uniformly)
RATE_AMP    = 2.5          # spikes/s, SD of slow fluctuation around that mean
TP_NOISE_SD = 0.0          # extra independent noise (0 = Poisson only)

# ── Helper functions ───────────────────────────────────────────────────────────

def slow_traces(rng, n_rows, n_pts, tau_pts):
    """n_rows independent smooth random traces, length n_pts, timescale tau_pts.
    White noise low-pass filtered with a Gaussian, then z-scored row-wise.
    mode='wrap' makes each trace periodic so a circular shift is a valid sample
    from the same generative process."""
    z = gaussian_filter1d(rng.normal(0, 1, (n_rows, n_pts)), tau_pts, axis=1, mode='wrap')
    return z / z.std(axis=1, keepdims=True)


def make_blocks(rng, n_blocks=N_BLOCKS, lo=BLOCK_LEN[0], hi=BLOCK_LEN[1], n_trials=None):
    """Sequence of alternating +1/-1 blocks with random lengths in [lo, hi].
    Pass n_trials to draw exactly that many trials (used for pseudosessions)."""
    sign = rng.choice([-1, 1])
    values, ids, i = [], [], 0
    while (len(values) < n_trials) if n_trials else (i < n_blocks):
        L = int(rng.integers(lo, hi + 1))
        values += [sign * (-1) ** i] * L
        ids    += [i] * L
        i += 1
    values, ids = np.array(values), np.array(ids)
    return (values[:n_trials], ids[:n_trials]) if n_trials else (values, ids)


# ── Generate simulation ────────────────────────────────────────────────────────

rng = np.random.default_rng(SEED)

# Task variable: alternating +/-1 blocks
block_values, block_ids = make_blocks(rng)
n_trials  = len(block_values)
per_trial = int(round(TRIAL_DUR / DT))    # timepoints per trial
n_pts     = n_trials * per_trial          # total timepoints in session

# Each neuron's firing rate: mean rate + slow fluctuation
# Nothing here depends on block_values or the pupil — no true correlation
rate_trial = (rng.uniform(*RATE_BASE, size=N_NEURONS)[:, None]
              + RATE_AMP * slow_traces(rng, N_NEURONS, n_trials, FLUCT_TAU / TRIAL_DUR))
rate_trial = rate_trial + rng.normal(0, TP_NOISE_SD, rate_trial.shape)
rate_trial = np.clip(rate_trial, 0, None)

# Interpolate to fine time grid and draw Poisson spikes
t_trial = (np.arange(n_trials) + 0.5) * TRIAL_DUR    # trial centres (s)
t_pts   = np.arange(n_pts) * DT                       # fine time grid (s)
rate    = np.array([np.interp(t_pts, t_trial, r) for r in rate_trial])
spikes  = rng.poisson(rate * DT)    # shape: (n_neurons, n_pts)

# Pupil: independent slow trace
pupil = 0.5 + 0.15 * slow_traces(rng, 1, n_trials, PUPIL_TAU / TRIAL_DUR)[0]

# Trial-binned firing rates
counts = spikes.reshape(N_NEURONS, n_trials, per_trial).sum(axis=2)  # (neurons, trials)
fr     = counts / TRIAL_DUR                                          # spikes/s

print(f'{N_NEURONS} neurons, {n_trials} trials ({n_trials * TRIAL_DUR / 60:.1f} min), {N_BLOCKS} blocks')
print(f'Firing rates: {fr.min():.1f} - {fr.max():.1f} spikes/s (mean {fr.mean():.1f})')
print(f'{spikes.sum():,} spikes total')

# ── Save ───────────────────────────────────────────────────────────────────────

out_dir = Path(__file__).parent / 'data'
out_dir.mkdir(exist_ok=True)

np.savez(
    out_dir / 'simulation.npz',
    fr           = fr,            # (n_neurons, n_trials)  firing rate per trial
    spikes       = spikes,        # (n_neurons, n_pts)     raw spike counts at DT resolution
    block_values = block_values,  # (n_trials,)            +1/-1 block label per trial
    block_ids    = block_ids,     # (n_trials,)            block index per trial
    pupil        = pupil,         # (n_trials,)            pupil diameter trace
    t_pts        = t_pts,         # (n_pts,)               time axis for spikes
    t_trial      = t_trial,       # (n_trials,)            trial centre times (s)
    # scalar metadata stored as 0-d arrays
    DT           = DT,
    TRIAL_DUR    = TRIAL_DUR,
    per_trial    = per_trial,
)

print(f'Saved to {out_dir / "simulation.npz"}')