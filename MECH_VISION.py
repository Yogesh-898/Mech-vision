import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle as MplCircle
import pandas as pd

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MECH VISION — Beam Stress Analyzer",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: #0d1117;
}
section[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #30363d;
}
section[data-testid="stSidebar"] * {
    color: #e6edf3 !important;
}
.metric-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #388bfd; }
.metric-label {
    font-size: 11px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8b949e;
    margin-bottom: 4px;
    font-family: 'DM Mono', monospace;
}
.metric-value {
    font-size: 22px;
    font-weight: 600;
    color: #e6edf3;
    font-family: 'DM Mono', monospace;
}
.metric-unit {
    font-size: 12px;
    color: #8b949e;
    font-family: 'DM Mono', monospace;
}
.safe-badge {
    display:inline-block;
    background: #1a3b2a;
    color: #3fb950;
    border: 1px solid #238636;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 13px;
    font-weight: 600;
    font-family: 'DM Mono', monospace;
}
.warn-badge {
    display:inline-block;
    background: #3b2a1a;
    color: #d29922;
    border: 1px solid #9e6a03;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 13px;
    font-weight: 600;
    font-family: 'DM Mono', monospace;
}
.fail-badge {
    display:inline-block;
    background: #3b1a1a;
    color: #f85149;
    border: 1px solid #da3633;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 13px;
    font-weight: 600;
    font-family: 'DM Mono', monospace;
}
.header-title {
    font-size: 28px;
    font-weight: 600;
    color: #e6edf3;
    letter-spacing: -0.5px;
}
.header-sub {
    font-size: 13px;
    color: #8b949e;
    font-family: 'DM Mono', monospace;
}
h1, h2, h3, h4 { color: #e6edf3 !important; }
p, label { color: #c9d1d9 !important; }
hr { border-color: #30363d !important; }
.stSelectbox label, .stSlider label, .stNumberInput label,
.stTextInput label, .stRadio label { color: #8b949e !important; font-size: 12px !important; }
div[data-testid="stExpander"] {
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    background: #161b22 !important;
}
.stDataFrame { background: #161b22; }
</style>
""", unsafe_allow_html=True)

# ─── Color palette ─────────────────────────────────────────────────────────
STRESS_CMAP = LinearSegmentedColormap.from_list(
    "stress", ["#388bfd", "#3fb950", "#e3b341", "#f85149"], N=256
)
BG   = "#0d1117"
SURF = "#161b22"
BORD = "#30363d"
TEXT = "#e6edf3"
MUTE = "#8b949e"
ACC  = "#388bfd"
GRN  = "#3fb950"
RED  = "#f85149"
YEL  = "#e3b341"

# Module-level lookup tables (single source of truth)
FY_MAP = {
    "Structural Steel (Fe250)": 250,
    "High-Strength Steel (Fe415)": 415,
    "Aluminium Alloy": 270,
    "Timber (Grade M30)": 30,
    "Concrete M25 (compression)": 25,
}
Z_MAP = {
    "Rectangle 100×200mm":  666.7,
    "I-Section (IPE 200)":  194.0,
    "I-Section (IPE 300)":  557.0,
    "Circular 150mm dia":   331.0,
    "T-Section 200×200mm":  214.0,
}

# ─── Engineering solver ────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def solve_beam(span, loads, support_a, support_b, udl=0, udl_start=0, udl_end=None):
    """
    Solve a statically determinate beam using statics (equilibrium equations).

    Supports:
        Pinned-Roller : simply supported (Ra, Rb vertical reactions)
        Fixed-Free    : cantilever (Ra vertical + Ma_moment fixed-end moment)

    Args:
        span        : beam length (m)
        loads       : tuple of (position_m, force_kN) point loads
        support_a   : "Pinned" or "Fixed"
        support_b   : "Roller" or "Free"  (auto-determined, not user-selectable)
        udl         : uniformly distributed load intensity (kN/m)
        udl_start   : UDL start position (m)
        udl_end     : UDL end position (m), defaults to span

    Returns:
        dict with Ra, Rb, Ma_moment, xs, sfd, bmd, stress, max_sfd, max_bmd
    """
    if udl_end is None:
        udl_end = span

    # Guard: UDL start > end — swap INSIDE solver so equilibrium check uses same values
    if udl_end < udl_start:
        udl_start, udl_end = udl_end, udl_start

    # --- Reactions (moment equilibrium) ---
    total_point = sum(P for _, P in loads)
    udl_len     = udl_end - udl_start
    udl_total   = udl * udl_len
    udl_arm     = udl_start + udl_len / 2.0

    if support_a == "Pinned" and support_b == "Roller":
        # ΣM_A = 0 → Rb × span = Σ(Pi × xi) + udl_total × udl_arm
        Ma        = sum(P * x for x, P in loads) + udl_total * udl_arm
        Rb        = Ma / span
        Ra        = total_point + udl_total - Rb
        Ma_moment = 0
    else:
        # Fixed-Free cantilever: ΣFy = 0,  ΣM_A = 0
        Ra        = total_point + udl_total
        Rb        = 0
        Ma_moment = -(sum(P * x for x, P in loads) + udl_total * udl_arm)

    # --- Arrays along beam ---
    n   = 1000
    xs  = np.linspace(0, span, n)
    sfd = np.zeros(n)
    bmd = np.zeros(n)

    # Proportional zero-clamp: avoids masking real shear on lightly loaded beams
    total_load_solver = total_point + udl_total
    sfd_tol = max(1e-6 * abs(total_load_solver), 1e-9)

    for i, x in enumerate(xs):
        # Both SFD and BMD use strict < — step discontinuity placed AFTER load
        # coordinate, consistent with FBD left-of-cut convention.
        V = Ra
        for xi, Pi in loads:
            if xi < x:           # was xi <= x (Error 1 fix)
                V -= Pi
        if x > udl_start:        # was x >= udl_start (Error 4 fix — consistent with BMD)
            covered = min(x, udl_end) - udl_start
            if covered > 0:
                V -= udl * covered
        sfd[i] = 0.0 if abs(V) < sfd_tol else V   # proportional clamp (Error 6 fix)

        M = Ra * x + Ma_moment
        for xi, Pi in loads:
            if xi < x:
                M -= Pi * (x - xi)
        if x > udl_start:
            cov = min(x, udl_end) - udl_start
            if cov > 0:
                M -= udl * cov * (x - udl_start - cov / 2.0)
        bmd[i] = M

    # bmd_norm: normalised moment [0,1] used for beam colour map.
    # Named explicitly to avoid confusion with actual bending stress (σ = M/Z, in MPa).
    max_bmd_abs = max(abs(bmd)) if max(abs(bmd)) > 0 else 1
    bmd_norm    = np.abs(bmd) / max_bmd_abs

    return {
        "Ra": Ra, "Rb": Rb,
        "Ma_moment": Ma_moment,
        "xs": xs, "sfd": sfd, "bmd": bmd, "bmd_norm": bmd_norm,
        "max_sfd": float(np.max(np.abs(sfd))),
        "max_bmd": float(np.max(np.abs(bmd))),
        "udl_start": udl_start, "udl_end": udl_end   # return sorted values for equilibrium check
    }


def safety_factor(max_stress_kNm, section, material):
    """
    Compute bending stress and safety factor for the given section and material.

    Formula: sigma = M / Z,  SF = fy / sigma

    Args:
        max_stress_kNm : maximum bending moment (kN·m)
        section        : cross-section profile name (key in Z_MAP)
        material       : material name (key in FY_MAP)

    Returns:
        (safety_factor, bending_stress_MPa)
    """
    Z    = Z_MAP.get(section, 200.0)
    fy   = FY_MAP.get(material, 250)
    Z_mm3 = Z * 1000
    M_Nmm = max_stress_kNm * 1e6
    sigma = M_Nmm / Z_mm3 if Z_mm3 > 0 else 0
    sf    = min(fy / sigma, 999.0) if sigma > 0 else 999.0
    return round(sf, 2), round(sigma, 1)


# ─── Plot functions ────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor":   SURF,
    "axes.edgecolor":   BORD,
    "axes.labelcolor":  MUTE,
    "xtick.color":      MUTE,
    "ytick.color":      MUTE,
    "grid.color":       BORD,
    "text.color":       TEXT,
    "font.family":      "monospace",
    "font.size":        9,
})


def plot_beam(span, loads, support_a, support_b, res, udl=0, udl_start=0, udl_end=None, udl_arrows=8):
    if udl_end is None:
        udl_end = span
    xs       = res["xs"]
    bmd_norm = res["bmd_norm"]
    Ra, Rb   = res["Ra"], res["Rb"]

    fig, ax = plt.subplots(figsize=(11, 3.2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(SURF)

    beam_y  = 0.0
    beam_h  = 0.22
    beam_hi = beam_y + beam_h

    # Stress-colored beam
    for i in range(len(xs) - 1):
        c = STRESS_CMAP(bmd_norm[i])
        ax.fill_betweenx([beam_y, beam_hi], xs[i], xs[i+1], color=c, linewidth=0)

    ax.plot([0, span], [beam_y, beam_y],       color=BORD, lw=1)
    ax.plot([0, span], [beam_hi, beam_hi],     color=BORD, lw=1)
    ax.plot([0, 0],    [beam_y, beam_hi],      color=BORD, lw=1)
    ax.plot([span, span], [beam_y, beam_hi],   color=BORD, lw=1)

    # UDL
    if udl > 0:
        udl_max_possible = 50.0
        udl_sc = (udl / udl_max_possible) * 0.4
        ax.fill_between(
            [udl_start, udl_end], beam_hi, beam_hi + udl_sc * 0.7,
            color=ACC, alpha=0.25, linewidth=0
        )
        ax.plot([udl_start, udl_end], [beam_hi + udl_sc * 0.7]*2,
                color=ACC, lw=1.2, linestyle="--")
        for wx in np.linspace(udl_start, udl_end, udl_arrows):
            ax.annotate("", xy=(wx, beam_hi),
                        xytext=(wx, beam_hi + udl_sc * 0.7),
                        arrowprops=dict(arrowstyle="-|>", color=ACC, lw=0.8))
        ax.text((udl_start+udl_end)/2, beam_hi + udl_sc*0.7 + 0.05,
                f"w = {udl} kN/m", ha="center", fontsize=8, color=ACC, style="italic")

    # Point loads
    arrow_h = 0.5
    for xi, Pi in loads:
        ax.annotate("", xy=(xi, beam_hi),
                    xytext=(xi, beam_hi + arrow_h),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.5))
        ax.text(xi, beam_hi + arrow_h + 0.06, f"{Pi} kN",
                ha="center", fontsize=8.5, color=RED, fontweight="bold")

    # Support symbols
    def draw_support(x_pos, label, reaction, sup_type):
        """Draw the correct engineering symbol for each support type."""
        if sup_type == "Pinned":
            tri_x = [x_pos - 0.22, x_pos + 0.22, x_pos, x_pos - 0.22]
            tri_y = [beam_y - 0.27, beam_y - 0.27, beam_y, beam_y - 0.27]
            ax.fill(tri_x, tri_y, color="#388bfd", alpha=0.25)
            ax.plot(tri_x, tri_y, color=ACC, lw=1)
            for hx in np.linspace(x_pos - 0.28, x_pos + 0.28, 6):
                ax.plot([hx, hx - 0.1], [beam_y - 0.30, beam_y - 0.40],
                        color=ACC, lw=0.8, alpha=0.6)
            ax.plot([x_pos - 0.32, x_pos + 0.32], [beam_y - 0.30, beam_y - 0.30],
                    color=ACC, lw=1.2)

        elif sup_type == "Roller":
            tri_x = [x_pos - 0.22, x_pos + 0.22, x_pos, x_pos - 0.22]
            tri_y = [beam_y - 0.27, beam_y - 0.27, beam_y, beam_y - 0.27]
            ax.fill(tri_x, tri_y, color="#3fb950", alpha=0.20)
            ax.plot(tri_x, tri_y, color=GRN, lw=1)
            for cx in [x_pos - 0.14, x_pos, x_pos + 0.14]:
                circle = MplCircle((cx, beam_y - 0.33), 0.045,
                                   color=GRN, fill=False, lw=0.9)
                ax.add_patch(circle)
            ax.plot([x_pos - 0.32, x_pos + 0.32], [beam_y - 0.38, beam_y - 0.38],
                    color=GRN, lw=1.2)

        elif sup_type == "Fixed":
            wall_w, wall_h = 0.18, 0.55
            ax.fill([x_pos - wall_w, x_pos, x_pos, x_pos - wall_w],
                    [beam_y - wall_h, beam_y - wall_h, beam_hi, beam_hi],
                    color="#388bfd", alpha=0.18)
            ax.plot([x_pos, x_pos], [beam_y - wall_h, beam_hi],
                    color=ACC, lw=2.5)
            for hy in np.linspace(beam_y - wall_h + 0.06, beam_hi - 0.06, 7):
                ax.plot([x_pos - wall_w, x_pos - wall_w + 0.12],
                        [hy, hy - 0.10], color=ACC, lw=0.8, alpha=0.55)

        elif sup_type == "Free":
            # Dashed line only — no constraint, no reaction label
            ax.plot([x_pos, x_pos], [beam_y - 0.45, beam_hi],
                    color=MUTE, lw=1.0, linestyle="--", alpha=0.6)

        # Reaction label (skip Free end — Rb = 0)
        if sup_type != "Free":
            label_y     = beam_y - 0.52
            label_color = GRN if sup_type == "Roller" else ACC
            if sup_type == "Fixed":
                sign_label = "hogging" if res["Ma_moment"] < 0 else "sagging"
                txt = f"{label}\nM={abs(res['Ma_moment']):.1f} kN·m\n({sign_label})"
            else:
                txt = f"{label}\n{reaction:.1f} kN"
            ax.text(x_pos, label_y, txt,
                    ha="center", fontsize=8, color=label_color, linespacing=1.4)

    draw_support(0,    "A", Ra, support_a)
    draw_support(span, "B", Rb, support_b)

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap=STRESS_CMAP, norm=plt.Normalize(0, 1))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation="vertical", pad=0.01, fraction=0.02)
    cbar.set_label("Stress intensity", color=MUTE, fontsize=8)
    cbar.ax.yaxis.set_tick_params(color=MUTE)
    cbar.set_ticks([0, 0.5, 1])
    cbar.set_ticklabels(["Low", "Med", "High"])
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=MUTE, fontsize=7)

    # Max moment marker
    idx_mmax = int(np.argmax(np.abs(res["bmd"])))
    mmax_x   = res["xs"][idx_mmax]
    mmax_val = res["bmd"][idx_mmax]
    if abs(mmax_val) > 0:
        sign_str = "+" if mmax_val >= 0 else ""
        ax.scatter([mmax_x], [beam_hi + 0.05], color=YEL, s=28, zorder=5)
        ax.text(mmax_x, beam_hi + 0.12,
                f"M={sign_str}{mmax_val:.1f} kN·m",
                ha="center", fontsize=7.5, color=YEL, fontweight="bold")

    ax.set_xlim(-0.5, span + 0.5)
    ax.set_ylim(-0.75, 1.2)
    ax.set_xlabel("Position along beam (m)", fontsize=9, color=MUTE)
    ax.set_title("BEAM — Stress Distribution", fontsize=10, color=TEXT,
                 fontweight="bold", pad=8, loc="left")
    ax.set_yticks([])
    ax.grid(axis="x", alpha=0.2, lw=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor(BORD)
    plt.tight_layout(pad=0.5)
    return fig


def plot_sfd(xs, sfd, span):
    fig, ax = plt.subplots(figsize=(11, 2.8))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(SURF)
    ax.fill_between(xs, 0, sfd, where=(sfd >= 0), color=ACC, alpha=0.4, linewidth=0)
    ax.fill_between(xs, 0, sfd, where=(sfd <  0), color=RED, alpha=0.4, linewidth=0)
    ax.plot(xs, sfd, color=ACC, lw=1.5)
    ax.axhline(0, color=BORD, lw=0.8)
    ax.set_xlim(0, span)
    ax.set_xlabel("Position (m)", fontsize=9, color=MUTE)
    ax.set_ylabel("Shear (kN)", fontsize=9, color=MUTE)
    ax.set_title("SHEAR FORCE DIAGRAM", fontsize=10, color=TEXT,
                 fontweight="bold", pad=8, loc="left")
    ax.grid(alpha=0.2, lw=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor(BORD)
    idx_max = np.argmax(np.abs(sfd))
    ax.annotate(f"  {sfd[idx_max]:.1f} kN", xy=(xs[idx_max], sfd[idx_max]),
                fontsize=8, color=YEL)
    plt.tight_layout(pad=0.5)
    return fig


def plot_bmd(xs, bmd, span):
    fig, ax = plt.subplots(figsize=(11, 2.8))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(SURF)
    ax.fill_between(xs, 0, bmd, where=(bmd >= 0), color=GRN, alpha=0.4, linewidth=0)
    ax.fill_between(xs, 0, bmd, where=(bmd <  0), color=RED, alpha=0.4, linewidth=0)
    ax.plot(xs, bmd, color=GRN, lw=1.5)
    ax.axhline(0, color=BORD, lw=0.8)
    ax.set_xlim(0, span)
    ax.set_xlabel("Position (m)", fontsize=9, color=MUTE)
    ax.set_ylabel("Moment (kN·m)", fontsize=9, color=MUTE)
    ax.set_title("BENDING MOMENT DIAGRAM", fontsize=10, color=TEXT,
                 fontweight="bold", pad=8, loc="left")
    ax.grid(alpha=0.2, lw=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor(BORD)
    idx_max = np.argmax(np.abs(bmd))
    ax.annotate(f"  {bmd[idx_max]:.1f} kN·m", xy=(xs[idx_max], bmd[idx_max]),
                fontsize=8, color=YEL)
    plt.tight_layout(pad=0.5)
    return fig


def plot_deflection(xs, bmd, span, E_GPa=200, I_cm4=5000, support_type="simply_supported"):
    """
    Compute and plot beam deflection via double numerical integration of M/EI.

    Method: Trapezoidal integration — EI·d²y/dx² = M(x)

    Boundary conditions:
        simply_supported : y(0) = 0,  y(L) = 0
        cantilever       : y(0) = 0,  θ(0) = 0  (at fixed wall)

    Args:
        xs           : position array (m)
        bmd          : bending moment array (kN·m)
        span         : beam length (m)
        E_GPa        : elastic modulus (GPa)
        I_cm4        : second moment of area (cm⁴)
        support_type : "simply_supported" or "cantilever"

    Returns:
        (fig, defl_max_mm)
    """
    E   = E_GPa * 1e9
    I   = I_cm4 * 1e-8
    EI  = E * I
    M   = -bmd * 1e3   # kN·m → N·m, sign: sagging → downward
    dx  = xs[1] - xs[0]

    slope = np.zeros(len(xs))
    defl  = np.zeros(len(xs))
    for i in range(1, len(xs)):
        slope[i] = slope[i-1] + 0.5 * (M[i-1]/EI + M[i]/EI) * dx
        defl[i]  = defl[i-1]  + 0.5 * (slope[i-1] + slope[i]) * dx

    if support_type == "cantilever":
        # BC: slope[0]=0 and defl[0]=0 are already satisfied by zero-initialisation.
        # The only correction needed is a sign flip: downward gravity load produces
        # negative bmd → after integration the curve grows upward → flip to downward.
        defl *= -1
    else:
        # Simply supported: y=0 at both ends
        corr  = np.interp(xs, [xs[0], xs[-1]], [defl[0], defl[-1]])
        defl -= corr

    defl_mm = defl * 1000

    fig, ax = plt.subplots(figsize=(11, 2.8))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(SURF)
    ax.fill_between(xs, 0, defl_mm, color="#d2a8ff", alpha=0.35, linewidth=0)
    ax.plot(xs, defl_mm, color="#d2a8ff", lw=1.5)
    ax.axhline(0, color=BORD, lw=0.8, linestyle="--")
    ax.set_xlim(0, span)
    ax.set_xlabel("Position (m)", fontsize=9, color=MUTE)
    ax.set_ylabel("Deflection (mm)", fontsize=9, color=MUTE)
    ax.set_title("DEFLECTION CURVE (approximate)", fontsize=10, color=TEXT,
                 fontweight="bold", pad=8, loc="left")
    ax.grid(alpha=0.2, lw=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor(BORD)
    idx = np.argmax(np.abs(defl_mm))
    ax.annotate(f"  δ_max = {defl_mm[idx]:.2f} mm",
                xy=(xs[idx], defl_mm[idx]), fontsize=8, color=YEL)
    plt.tight_layout(pad=0.5)
    return fig, float(defl_mm[np.argmax(np.abs(defl_mm))])


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Beam Setup")
    st.markdown("---")

    span = st.slider("Beam Span (m)", min_value=1.0, max_value=20.0, value=6.0, step=0.5)

    # ── Support A ──
    # Support B is NOT a dropdown — it is auto-determined from Support A:
    #   Pinned → Roller  (only valid simply-supported pairing)
    #   Fixed  → Free    (cantilever — free end has no reaction)
    support_a = st.selectbox("Support A (left end)", ["Pinned", "Fixed"], index=0)

    if support_a == "Pinned":
        support_b = st.selectbox("Support B (right end)", ["Roller"], index=0, key="sb_pinned")
    else:  # Fixed
        support_b = st.selectbox("Support B (right end)", ["Free"], index=0, key="sb_fixed")

    st.markdown("---")
    st.markdown("**Cross-Section**")
    section = st.selectbox("Section Profile", [
        "Rectangle 100×200mm",
        "I-Section (IPE 200)",
        "I-Section (IPE 300)",
        "Circular 150mm dia",
        "T-Section 200×200mm",
    ])
    material = st.selectbox("Material", [
        "Structural Steel (Fe250)",
        "High-Strength Steel (Fe415)",
        "Aluminium Alloy",
        "Timber (Grade M30)",
        "Concrete M25 (compression)",
    ])

    E_GPa = st.number_input("E — Elastic Modulus (GPa)", value=200, min_value=1, max_value=400)
    I_cm4 = st.number_input("I — Moment of Inertia (cm⁴)", value=5000, min_value=10, max_value=500000)

    st.markdown("---")
    st.markdown("**Distributed Load (UDL)**")
    udl       = st.slider("UDL Intensity (kN/m)", 0.0, 50.0, 0.0, 1.0)
    udl_start = st.slider("UDL Start (m)", 0.0, span, 0.0, 0.5)
    # Allow zero-length UDL (udl_start == udl_end → no load, no crash)
    udl_end_min = udl_start if udl_start < span else max(0.0, span - 0.5)
    udl_end     = st.slider("UDL End (m)", udl_end_min, span, float(span), 0.5)
    udl_arrows  = st.slider("Number of load arrows", 2, 20, 8, 1)

    st.markdown("---")
    st.markdown("**Point Loads**")
    n_loads = st.number_input("Number of point loads", 0, 6, 1)

    # ── Cantilever load-position hint ──────────────────────────────────────
    # For Fixed–Free (cantilever): default load snaps to the free tip (x = span).
    # For Pinned–Roller (simply supported): spread loads evenly along the span.
    is_cantilever_sidebar = (support_a == "Fixed")
    if is_cantilever_sidebar and int(n_loads) > 0:
        st.markdown(
            "<div style='font-size:11px;color:#e3b341;padding:2px 0 6px 0'>"
            "💡 Tip load defaults to the free end (x = span).</div>",
            unsafe_allow_html=True
        )

    loads = []
    for i in range(int(n_loads)):
        c1, c2 = st.columns(2)
        with c1:
            # Cantilever: default position = free tip (span)
            # Simply supported: space loads evenly
            if is_cantilever_sidebar:
                default_x = float(span)
            else:
                default_x = round(span / (int(n_loads) + 1) * (i + 1), 1)

            xi = st.number_input(
                f"x{i+1} (m)", 0.0, float(span),
                min(default_x, float(span)),   # clamp so it never exceeds span
                step=0.1, key=f"x{i}"
            )
        with c2:
            Pi = st.number_input(f"P{i+1} (kN)", 0.1, 500.0, 10.0, step=1.0, key=f"p{i}")
        loads.append((float(xi), float(Pi)))

    st.markdown("---")
    st.info("Results update live as you change inputs above.", icon="⚡")


# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding: 32px 0 12px 0; text-align: center;'>
  <span style='font-size: 38px; font-weight: 700; color: #e6edf3; letter-spacing: -0.5px;'>
    🏗️ Mech Vision
  </span><br>
  <span style='font-size: 16px; color: #8b949e; font-family: DM Mono, monospace; letter-spacing: 0.04em;'>
    Beam Load &amp; Stress Analyzer — v1.0
  </span><br><br>
  <span style='font-size: 13px; color: #3fb950; font-family: DM Mono, monospace; letter-spacing: 0.1em;'>
    ✦ Made by YOGESH S ✦
  </span>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ─── Main analysis block ──────────────────────────────────────────────────────
sup_type = "cantilever" if (support_a == "Fixed" and support_b == "Free") else "simply_supported"

try:
    res = solve_beam(span, tuple(loads), support_a, support_b, udl, udl_start, udl_end)
    sf, sigma = safety_factor(res["max_bmd"], section, material)

    # Equilibrium check — use the UDL start/end AFTER the solver's swap guard
    # so total_load matches exactly what the solver used internally.
    udl_start_used = res["udl_start"]
    udl_end_used   = res["udl_end"]
    total_load     = sum(P for _, P in loads) + udl * (udl_end_used - udl_start_used)
    reaction_sum   = res["Ra"] + res["Rb"]
    equil_tol      = max(0.01 * total_load, 0.1)
    if total_load > 0 and abs(reaction_sum - total_load) > equil_tol:
        st.error(
            f"⚠️ Equilibrium error: Ra + Rb = {reaction_sum:.2f} kN "
            f"but total load = {total_load:.2f} kN. Check inputs."
        )

    # ── Metric cards ─────────────────────────────────────────────────────────
    is_cantilever = (support_a == "Fixed" and support_b == "Free")
    col_count     = 6 if is_cantilever else 5
    cols          = st.columns(col_count)

    with cols[0]:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-label'>Reaction A</div>
            <div class='metric-value'>{res['Ra']:.2f}</div>
            <div class='metric-unit'>kN</div></div>""", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-label'>Reaction B</div>
            <div class='metric-value'>{res['Rb']:.2f}</div>
            <div class='metric-unit'>kN</div></div>""", unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-label'>Max Shear</div>
            <div class='metric-value'>{res['max_sfd']:.2f}</div>
            <div class='metric-unit'>kN</div></div>""", unsafe_allow_html=True)
    with cols[3]:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-label'>Max Moment</div>
            <div class='metric-value'>{res['max_bmd']:.2f}</div>
            <div class='metric-unit'>kN·m</div></div>""", unsafe_allow_html=True)
    with cols[4]:
        if sf >= 2.5:
            badge = f"<span class='safe-badge'>✓ SAFE  SF={sf}</span>"
        elif sf >= 1.5:
            badge = f"<span class='warn-badge'>⚠ MARGINAL  SF={sf}</span>"
        else:
            badge = f"<span class='fail-badge'>✗ FAILURE  SF={sf}</span>"
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-label'>Safety Factor</div>
            <div style='margin-top:6px'>{badge}</div>
            <div class='metric-unit' style='margin-top:4px'>σ = {sigma} MPa</div>
            </div>""", unsafe_allow_html=True)
    if is_cantilever:
        with cols[5]:
            sign_label = "hogging" if res["Ma_moment"] < 0 else "sagging"
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-label'>Fixed-End Moment</div>
                <div class='metric-value'>{abs(res['Ma_moment']):.2f}</div>
                <div class='metric-unit'>kN·m ({sign_label})</div></div>""",
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Diagrams ──────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Beam & Stress", "⚡ Shear Force", "🌀 Bending Moment", "📉 Deflection"]
    )

    with tab1:
        fig1 = plot_beam(span, loads, support_a, support_b, res, udl, udl_start, udl_end, udl_arrows)
        st.pyplot(fig1, use_container_width=True)
        plt.close(fig1)

    with tab2:
        fig2 = plot_sfd(res["xs"], res["sfd"], span)
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)

    with tab3:
        fig3 = plot_bmd(res["xs"], res["bmd"], span)
        st.pyplot(fig3, use_container_width=True)
        plt.close(fig3)

    with tab4:
        fig4, defl_max = plot_deflection(
            res["xs"], res["bmd"], span, E_GPa, I_cm4, support_type=sup_type
        )
        st.pyplot(fig4, use_container_width=True)
        plt.close(fig4)

        defl_limit     = (span * 1000) / (180 if is_cantilever else 250)
        limit_label    = "L/180 (cantilever)" if is_cantilever else "L/250"
        defl_limit_max = (span * 1000) / 10
        if abs(defl_max) > defl_limit_max:
            st.warning(
                f"⚠️ Deflection {abs(defl_max):.1f} mm exceeds L/10 = {defl_limit_max:.0f} mm "
                f"— result may be unrealistic. Check E and I values."
            )
        elif abs(defl_max) <= defl_limit:
            st.success(
                f"✅ Deflection OK — δ_max = {abs(defl_max):.2f} mm  ≤  {limit_label} = {defl_limit:.1f} mm"
            )
        else:
            st.error(
                f"❌ Deflection EXCEEDS limit — δ_max = {abs(defl_max):.2f} mm  >  {limit_label} = {defl_limit:.1f} mm"
            )

    # ── Raw data table ────────────────────────────────────────────────────────
    with st.expander("📋 View Raw Data Table (SFD & BMD)"):
        step = 50
        df = pd.DataFrame({
            "Position (m)":           np.round(res["xs"][::step], 3),
            "Shear Force (kN)":       np.round(res["sfd"][::step], 3),
            "Bending Moment (kN·m)":  np.round(res["bmd"][::step], 3),
            "BMD Normalised [0–1]":   np.round(res["bmd_norm"][::step], 3),
        })
        st.dataframe(df, use_container_width=True, height=280)

    # ── Engineering summary ───────────────────────────────────────────────────
    with st.expander("📝 Engineering Summary"):
        fy_val      = FY_MAP.get(material, 250)
        defl_lim_val = (span * 1000) / (180 if is_cantilever else 250)
        defl_lim_lbl = "L/180 (cantilever)" if is_cantilever else "L/250"
        defl_status = "PASS ✅" if abs(defl_max) <= defl_lim_val else "FAIL ❌"
        concrete_note = "\n> ⚠️ *Plain concrete cannot resist bending tension. Safety factor is indicative only — not valid for unreinforced concrete design.*" if "Concrete" in material else ""
        st.markdown(f"""
| Parameter | Value |
|---|---|
| Beam Span | {span} m |
| Support Configuration | {support_a} – {support_b} |
| Total Applied Load | {total_load:.2f} kN |
| Support A (Reaction) | {res['Ra']:.2f} kN |
| Support B (Reaction) | {res['Rb']:.2f} kN |
| Max Shear Force | {res['max_sfd']:.2f} kN |
| Max Bending Moment | {res['max_bmd']:.2f} kN·m |
| Max Bending Stress | {sigma} MPa |
| Material Yield Strength | {fy_val} MPa |
| Safety Factor | {sf} |
| Max Deflection | {abs(defl_max):.2f} mm |
| Deflection Limit ({defl_lim_lbl}) | {defl_lim_val:.1f} mm |
| Deflection Check | {defl_status} |
| Section | {section} |
| Material | {material} |
{concrete_note}
""")

except Exception as e:
    st.error(f"⚠️ Solver error: {e}")
    st.info("Tip: Make sure point load positions are within the beam span.")
