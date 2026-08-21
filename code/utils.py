"""Shared helpers for the simulation-driven analysis workshop notebooks.

Each function here is a reusable version of code that is first introduced (and kept
inline) in one of the notebooks.  Downstream notebooks import from this module so that
every notebook can be run on its own, without having to first execute an earlier one.

Ownership of the original inline definitions:

- ``simulate_null_session`` / ``correlate_and_select`` / ``annotate_corr``
  -> Part 1 (``1_simulating-analysis_solutions.ipynb``)
- ``train_test_PRCA`` / ``fwer_cells`` / ``fdr_bh_cells``
  -> Part 2 (``2_refining-analysis_solutions.ipynb``)
- ``simulate_real_effect``
  -> Part 3 (``3_simulating-ground-truth_solutions.ipynb``)
- ``loo_cv_PRCA``
  -> Extension 1 (``extension-LOO-CV-power.ipynb``)
"""

import numpy as np
from scipy import stats


# ---------------------------------------------------------------------------
# Part 1: simulating the null session and the proposed (circular) workflow
# ---------------------------------------------------------------------------
def simulate_null_session(rng, Ngroups=20, Ncells=200, mean_perf=75, sd_perf=8, mean_dff=2, sd_dff=1):
    """Simulate a single null session (no real effect).

    Draws are made in the same order as in Part 1 so that, given the same seeded
    ``rng``, the returned arrays match those produced inline in Part 1.

    Returns
    -------
    Perf : ndarray, shape (Ngroups,)
        Behavioral performance per trial group (rounded to integer percent).
    DA : ndarray, shape (Ngroups, Ncells)
        Average cell activity per trial group (pure noise in the null case).
    CellXY : ndarray, shape (Ncells, 2)
        Random 2D position of each cell on the unit square.
    """
    Perf = np.round(sd_perf * rng.standard_normal(Ngroups) + mean_perf)
    DA = sd_dff * rng.standard_normal(size=(Ngroups, Ncells)) + mean_dff
    CellXY = rng.uniform(0.0, 1.0, size=(Ncells, 2))
    return Perf, DA, CellXY


def correlate_and_select(DA, Perf, r_thresh=0.1, p_thresh=0.05):
    """Correlate every cell's activity with performance and apply the selection rule.

    Returns ``(r, p, SelectedCells)`` where ``SelectedCells`` are the indices of cells
    that are positively correlated (``r > r_thresh``) and significant (``p < p_thresh``).
    """
    res = stats.pearsonr(DA, Perf[:, np.newaxis], axis=0)
    r, p = res.statistic, res.pvalue
    SelectedCells = np.where((r > r_thresh) & (p < p_thresh))[0]
    return r, p, SelectedCells


def annotate_corr(ax, PRCA, Perf, title):
    """Scatter PRCA vs. performance on ``ax``, add a best-fit line and R^2 / p label."""
    ax.plot(PRCA, Perf, "o", color="tab:blue", markerfacecolor="tab:blue")
    fit = stats.linregress(PRCA, Perf)
    xl = np.array(ax.get_xlim())
    ax.plot(xl, fit.slope * xl + fit.intercept, "-", color="tab:orange")
    ax.set_xlim(xl)
    ax.set_xlabel("Performance-Related Cell Activity")
    ax.set_ylabel("Behavioral Performance")
    ax.set_title(title)
    Rsquared = fit.rvalue ** 2
    xlims, ylims = ax.get_xlim(), ax.get_ylim()
    xpos = xlims[0] + 0.05 * (xlims[1] - xlims[0])
    ypos = ylims[1] - 0.05 * (ylims[1] - ylims[0])
    ax.text(xpos, ypos, f"$R^2$={Rsquared:.4f}  P={fit.pvalue:.2e}")


# ---------------------------------------------------------------------------
# Part 2: valid workflows (train/test split and multiple-comparison correction)
# ---------------------------------------------------------------------------
def train_test_PRCA(DA, Perf, train_frac=0.5, rng=None):
    """Single train/test split: select cells on the training trial groups, then compute
    and return PRCA on the held-out test trial groups (which played no part in selection).

    Returns ``(PRCA_test, Perf_test, selected_cells)``, or ``None`` if no cells selected.
    """
    if rng is None:
        rng = np.random.default_rng()
    Ng = DA.shape[0]
    idx = np.arange(Ng)
    idx = rng.permutation(idx)  # randomize which groups are train vs test
    n_train = int(round(train_frac * Ng))
    train_idx, test_idx = idx[:n_train], idx[n_train:]

    res = stats.pearsonr(DA[train_idx], Perf[train_idx][:, np.newaxis], axis=0)
    sel = np.where((res.statistic > 0.1) & (res.pvalue < 0.05))[0]
    if sel.size == 0:
        return None
    PRCA_test = DA[test_idx][:, sel].mean(axis=1)
    return PRCA_test, Perf[test_idx], sel


def fwer_cells(DA, Perf, q=0.05):
    """Select cells whose correlation with Perf survives Bonferroni (FWER) at level q."""
    res = stats.pearsonr(DA, Perf[:, np.newaxis], axis=0)
    adj_p = res.pvalue * res.pvalue.size  # Bonferroni correction
    return np.where(adj_p <= q)[0]


def fdr_bh_cells(DA, Perf, q=0.05):
    """Select cells whose correlation with Perf survives Benjamini-Hochberg FDR at level q."""
    res = stats.pearsonr(DA, Perf[:, np.newaxis], axis=0)
    adj_p = stats.false_discovery_control(res.pvalue, method="bh")
    return np.where(adj_p <= q)[0]


# ---------------------------------------------------------------------------
# Part 3: simulating a genuine effect
# ---------------------------------------------------------------------------
def simulate_real_effect(rng, Perf, Ncells, CorrelatedCells, k, sd_dff=1):
    """Simulate cell activity in which ``CorrelatedCells`` are genuinely modulated by Perf.

    A scaled, mean-zero function of performance is added on top of the noise for the
    correlated cells.  ``k`` sets the effect size relative to the noise.
    """
    Ngroups = Perf.shape[0]
    Pscaled = (k * sd_dff / np.std(Perf, ddof=1)) * (Perf - np.mean(Perf))
    DA_real = sd_dff * rng.standard_normal((Ngroups, Ncells))
    DA_real[:, CorrelatedCells] += Pscaled[:, np.newaxis]
    return DA_real


# ---------------------------------------------------------------------------
# Extension 1: leave-one-out cross-validation
# ---------------------------------------------------------------------------
def loo_cv_PRCA(DA, Perf):
    """Leave-one-out cross-validated PRCA.

    For each held-out trial group i, cells are selected on the other N-1 trial groups
    (r > 0.1, p < 0.05), then PRCA is computed for trial group i on those cells.

    Returns
    -------
    PRCA_cv : ndarray, shape (Ngroups,)
        Cross-validated PRCA; NaN where no cells were selected in that fold.
    n_cells : list of int
        Number of cells selected in each fold (diagnostic).
    """
    Ngroups = DA.shape[0]
    PRCA_cv = np.full(Ngroups, np.nan)
    n_cells = []
    for i in range(Ngroups):
        train_idx = np.delete(np.arange(Ngroups), i)
        res = stats.pearsonr(DA[train_idx], Perf[train_idx][:, np.newaxis], axis=0)
        sel_cells = np.where((res.statistic > 0.1) & (res.pvalue < 0.05))[0]
        n_cells.append(sel_cells.size)
        if sel_cells.size > 0:
            PRCA_cv[i] = DA[i, sel_cells].mean()
    return PRCA_cv, n_cells
