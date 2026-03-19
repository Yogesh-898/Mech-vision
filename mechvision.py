import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle as MplCircle
import pandas as pd

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mech Vision",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=Inter:wght@300;400;500;600&family=DM+Mono:wght@400;500&family=Rajdhani:wght@500;600;700&family=Cinzel+Decorative:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
  background-color: #080d14;
  background-image:
    radial-gradient(circle, rgba(180,198,220,0.09) 1px, transparent 1px),
    linear-gradient(rgba(180,198,220,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(180,198,220,0.025) 1px, transparent 1px),
    radial-gradient(ellipse 85% 55% at 50% 20%,  rgba(20,90,200,0.22)  0%, rgba(10,50,130,0.10) 45%, transparent 75%),
    radial-gradient(ellipse 40% 70% at 0%   50%,  rgba(10,40,120,0.14)  0%, transparent 65%),
    radial-gradient(ellipse 40% 70% at 100% 50%,  rgba(10,40,120,0.12)  0%, transparent 65%),
    radial-gradient(ellipse 100% 40% at 50% 100%, rgba(4,12,30,0.6)     0%, transparent 70%);
  background-size: 28px 28px, 112px 112px, 112px 112px, 100% 100%, 100% 100%, 100% 100%, 100% 100%;
}

section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #050a10 0%, #070c16 100%);
  border-right: 1px solid rgba(180,198,220,0.10);
  box-shadow: 4px 0 24px rgba(0,0,0,0.5);
}
section[data-testid="stSidebar"] * { color: #8aa0ba !important; }

.metric-card {
  background: linear-gradient(135deg, rgba(13,20,32,0.85), rgba(8,13,20,0.92));
  backdrop-filter: blur(10px);
  border: 1px solid rgba(180,198,220,0.08);
  border-top: 2px solid rgba(180,198,220,0.22);
  border-radius: 3px; padding: 20px 16px 16px;
  text-align: center; position: relative;
  transition: all 0.3s ease; box-shadow: 0 4px 16px rgba(0,0,0,0.25);
}
.metric-card:hover {
  background: linear-gradient(135deg, rgba(17,26,44,0.9), rgba(11,18,30,0.95));
  border-top-color: rgba(180,198,220,0.5);
  box-shadow: 0 8px 28px rgba(0,0,0,0.4); transform: translateY(-2px);
}
.metric-card-safe  { border-top-color: rgba(90,184,160,0.6) !important; }
.metric-card-warn  { border-top-color: rgba(180,160,100,0.6) !important; }
.metric-card-fail  { border-top-color: rgba(176,96,112,0.7) !important; box-shadow: 0 0 20px rgba(176,96,112,0.1) !important; }

.metric-label {
  font-size: 8.5px; letter-spacing: 0.22em; text-transform: uppercase;
  color: rgba(140,165,190,0.55); margin-bottom: 10px;
  font-family: 'DM Mono', monospace; font-weight: 500;
}
.metric-value {
  font-size: 30px; font-weight: 600; color: #dce8f5;
  font-family: 'Rajdhani', sans-serif; line-height: 1; letter-spacing: 0.02em;
}
.metric-unit {
  font-size: 9.5px; color: rgba(120,145,170,0.45);
  font-family: 'DM Mono', monospace; margin-top: 6px; letter-spacing: 0.08em;
}

.check-row { display: flex; gap: 10px; margin: 16px 0 10px 0; flex-wrap: wrap; }
.check-chip {
  background: rgba(13,20,32,0.80);
  border: 1px solid rgba(180,198,220,0.08);
  border-radius: 3px; padding: 10px 14px; flex: 1; min-width: 160px;
}
.check-chip-label {
  font-size: 8px; letter-spacing: 0.22em; text-transform: uppercase;
  color: rgba(140,165,190,0.45); font-family: 'DM Mono', monospace; margin-bottom: 5px;
}
.check-chip-val {
  font-size: 20px; font-weight: 600; font-family: 'Rajdhani', sans-serif;
  color: #dce8f5; line-height: 1;
}
.check-chip-sub {
  font-size: 8px; color: rgba(120,145,170,0.45);
  font-family: 'DM Mono', monospace; margin-top: 3px;
}

.lf-badge-char {
  display:inline-flex;align-items:center;gap:5px;
  background:rgba(90,184,160,0.06); color:#5ab8a0;
  border:1px solid rgba(80,180,160,0.28); border-radius:2px;
  padding:4px 12px; font-size:9px; font-weight:600;
  font-family:'DM Mono',monospace; letter-spacing:0.14em; text-transform:uppercase;
}
.lf-badge-design {
  display:inline-flex;align-items:center;gap:5px;
  background:rgba(180,160,100,0.06); color:#d4a040;
  border:1px solid rgba(180,160,100,0.28); border-radius:2px;
  padding:4px 12px; font-size:9px; font-weight:600;
  font-family:'DM Mono',monospace; letter-spacing:0.14em; text-transform:uppercase;
}

.safe-badge {
  display:inline-flex;align-items:center;gap:5px;
  background:rgba(90,184,160,0.06); color:#5ab8a0;
  border:1px solid rgba(80,180,160,0.28); border-radius:2px; padding:5px 14px;
  font-size:9.5px; font-weight:600; font-family:'DM Mono',monospace;
  letter-spacing:0.14em; text-transform:uppercase;
}
.warn-badge {
  display:inline-flex;align-items:center;gap:5px;
  background:rgba(180,160,100,0.06); color:#b4a060;
  border:1px solid rgba(180,160,100,0.28); border-radius:2px; padding:5px 14px;
  font-size:9.5px; font-weight:600; font-family:'DM Mono',monospace;
  letter-spacing:0.14em; text-transform:uppercase;
}
.fail-badge {
  display:inline-flex;align-items:center;gap:5px;
  background:rgba(176,96,112,0.08); color:#b06070;
  border:1px solid rgba(176,96,112,0.3); border-radius:2px; padding:5px 14px;
  font-size:9.5px; font-weight:600; font-family:'DM Mono',monospace;
  letter-spacing:0.14em; text-transform:uppercase;
  animation:failPulse 2.5s ease infinite;
}
@keyframes failPulse {
  0%,100%{ box-shadow: 0 0 0 rgba(176,96,112,0); }
  50%    { box-shadow: 0 0 12px rgba(176,96,112,0.18); }
}

.stTabs [data-baseweb="tab-list"] {
  background:transparent; border-bottom:1px solid rgba(180,198,220,0.08);
  border-radius:0; padding:0; gap:0;
}
.stTabs [data-baseweb="tab"] {
  border-radius:0 !important; color:rgba(140,165,190,0.45) !important;
  font-family:'DM Mono',monospace !important; font-size:10px !important;
  font-weight:500 !important; padding:10px 20px !important;
  letter-spacing:0.14em !important; text-transform:uppercase !important;
  transition:all 0.2s !important; border-bottom:2px solid transparent !important;
}
.stTabs [data-baseweb="tab"]:hover {
  color:rgba(220,232,245,0.7) !important; background:rgba(180,198,220,0.03) !important;
}
.stTabs [aria-selected="true"] {
  background:transparent !important; color:#dce8f5 !important;
  border-bottom:2px solid rgba(180,198,220,0.65) !important; font-weight:600 !important;
}

div[data-testid="stExpander"] {
  background:linear-gradient(135deg,rgba(8,13,20,0.9),rgba(12,18,26,0.85)) !important;
  backdrop-filter:blur(8px) !important; border:1px solid rgba(180,198,220,0.06) !important;
  border-left:2px solid rgba(180,198,220,0.18) !important; border-radius:3px !important;
  transition:border-left-color 0.3s !important;
}
div[data-testid="stExpander"]:hover { border-left-color:rgba(180,198,220,0.42) !important; }
div[data-testid="stExpander"] summary {
  font-family:'DM Mono',monospace !important; font-size:10px !important;
  letter-spacing:0.15em !important; color:rgba(140,165,190,0.6) !important;
  text-transform:uppercase !important; font-weight:500 !important;
}

.stSlider [data-baseweb="slider"] [role="slider"] {
  background:#b4c6dc !important; box-shadow:0 0 6px rgba(180,198,220,0.4) !important;
  border:2px solid rgba(180,198,220,0.45) !important;
  width:14px !important; height:14px !important; transition:box-shadow 0.2s !important;
}
.stSlider [data-baseweb="slider"] [data-testid="stSliderTrackFill"] {
  background:rgba(180,198,220,0.45) !important;
}
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
  background:rgba(8,13,20,0.8) !important; backdrop-filter:blur(6px) !important;
  border:1px solid rgba(180,198,220,0.08) !important; border-radius:3px !important;
  transition:border-color 0.2s,box-shadow 0.2s !important;
}
div[data-baseweb="select"] > div:hover, div[data-baseweb="input"] > div:focus-within {
  border-color:rgba(180,198,220,0.28) !important;
  box-shadow:0 0 0 3px rgba(180,198,220,0.05) !important;
}
div[data-baseweb="select"] * {
  font-family:'Inter',sans-serif !important; font-size:13px !important; color:#8aa0ba !important;
}

.stDownloadButton > button {
  background:rgba(90,184,160,0.08) !important; color:#5ab8a0 !important;
  border:1px solid rgba(80,180,160,0.25) !important; border-radius:2px !important;
  font-family:'DM Mono',monospace !important; font-size:10px !important;
  font-weight:600 !important; letter-spacing:0.16em !important;
  text-transform:uppercase !important; padding:12px 28px !important;
  transition:all 0.25s ease !important;
}
.stDownloadButton > button:hover {
  background:rgba(90,184,160,0.14) !important; border-color:rgba(90,184,160,0.45) !important;
  transform:translateY(-1px) !important;
  box-shadow:0 6px 24px rgba(0,0,0,0.3),0 0 12px rgba(90,184,160,0.1) !important;
}

div[data-testid="stAlert"] { border-radius:2px !important; font-family:'DM Mono',monospace !important; font-size:11px !important; }
div[data-testid="stInfo"] {
  background:rgba(180,198,220,0.03) !important; border:1px solid rgba(180,198,220,0.10) !important;
  border-left:2px solid rgba(180,198,220,0.38) !important; border-radius:2px !important;
}

.stDataFrame { border-radius:3px !important; border:1px solid rgba(180,198,220,0.06) !important; }
.stDataFrame th {
  background:rgba(180,198,220,0.03) !important; font-family:'DM Mono',monospace !important;
  font-size:9px !important; letter-spacing:0.16em !important;
  text-transform:uppercase !important; color:rgba(140,165,190,0.5) !important; font-weight:500 !important;
}
.stDataFrame td { font-family:'Inter',sans-serif !important; font-size:12.5px !important; color:#8aa0ba !important; }

.sidebar-section {
  font-size:8.5px; letter-spacing:0.24em; text-transform:uppercase;
  color:rgba(180,198,220,0.48); font-family:'DM Mono',monospace; font-weight:500;
  padding:4px 0 3px 10px; border-left:3px solid rgba(180,198,220,0.25); margin-bottom:10px;
}

h1,h2,h3,h4 { font-family:'Cormorant Garamond',serif !important; color:#dce8f5 !important; font-weight:400 !important; letter-spacing:-0.01em !important; }
p, label { color:rgba(120,145,170,0.7) !important; }
hr { border-color:rgba(180,198,220,0.06) !important; }
.stSelectbox label,.stSlider label,.stNumberInput label,.stTextInput label,.stRadio label {
  color:rgba(140,165,190,0.5) !important; font-size:9px !important; letter-spacing:0.2em !important;
  text-transform:uppercase !important; font-family:'DM Mono',monospace !important; font-weight:500 !important;
}

::-webkit-scrollbar { width:3px; height:3px; }
::-webkit-scrollbar-track { background:#080d14; }
::-webkit-scrollbar-thumb { background:rgba(180,198,220,0.18); border-radius:2px; }
::-webkit-scrollbar-thumb:hover { background:rgba(180,198,220,0.32); }
</style>
""", unsafe_allow_html=True)

# ─── Color palette ─────────────────────────────────────────────────────────
STRESS_CMAP = LinearSegmentedColormap.from_list(
    "navy", ["#080d14", "#0d2a5a", "#4a80c0", "#b4c6dc"], N=256
)
BG   = "#080d14"
SURF = "#0d1420"
BORD = "#142030"
TEXT = "#dce8f5"
MUTE = "#3a4e68"
ACC  = "#b4c6dc"
GRN  = "#5ab8a0"
RED  = "#b06070"
YEL  = "#7a9ec0"
PURP = "#d2a8ff"

# ─── Section Properties Database ──────────────────────────────────────────────
SECTION_PROPS = {
    "Rectangle 100×200mm": {
        "A_cm2": 200.0, "I_cm4": 6666.7, "Z_cm3": 666.7,
        "r_cm": 5.77, "y_top_mm": 100.0, "y_bot_mm": 100.0,
        "A_web_mm2": 100.0 * 200.0, "shape": "rect",
        "dims": {"b": 100, "h": 200}, "desc": "b=100mm, h=200mm",
    },
    "I-Section (IPE 200)": {
        "A_cm2": 28.5, "I_cm4": 1943.0, "Z_cm3": 194.0,
        "r_cm": 8.26, "y_top_mm": 100.0, "y_bot_mm": 100.0,
        "A_web_mm2": 5.6 * (200 - 2*8.5), "shape": "ipe",
        "dims": {"h": 200, "b": 100, "tf": 8.5, "tw": 5.6},
        "desc": "h=200mm, b=100mm, tf=8.5mm, tw=5.6mm",
    },
    "I-Section (IPE 300)": {
        "A_cm2": 53.8, "I_cm4": 8356.0, "Z_cm3": 557.0,
        "r_cm": 12.46, "y_top_mm": 150.0, "y_bot_mm": 150.0,
        "A_web_mm2": 7.1 * (300 - 2*10.7), "shape": "ipe",
        "dims": {"h": 300, "b": 150, "tf": 10.7, "tw": 7.1},
        "desc": "h=300mm, b=150mm, tf=10.7mm, tw=7.1mm",
    },
    "Circular 150mm dia": {
        "A_cm2": 176.7, "I_cm4": 2485.0, "Z_cm3": 331.0,
        "r_cm": 3.75, "y_top_mm": 75.0, "y_bot_mm": 75.0,
        "A_web_mm2": 0.9 * 176.7 * 100, "shape": "circle",
        "dims": {"d": 150}, "desc": "dia=150mm",
    },
    "T-Section 200×200mm": {
        "A_cm2": 76.0, "I_cm4": 1712.0, "Z_cm3": 214.0,
        "r_cm": 4.74, "y_top_mm": 57.4, "y_bot_mm": 142.6,
        "A_web_mm2": 20.0 * (200 - 20), "shape": "tee",
        "dims": {"h": 200, "b": 200, "tf": 20, "tw": 20},
        "desc": "h=200mm, b=200mm, tf=20mm, tw=20mm",
    },
}

# ─── Material lookups ─────────────────────────────────────────────────────────
FY_MAP = {
    "Structural Steel (Fe250)":       250,
    "High-Strength Steel (Fe415)":    415,
    "Aluminium Alloy":                270,
    "Timber (Grade M30)":              30,
    "Concrete M25 (compression)":      25,
}
Z_MAP = {k: v["Z_cm3"] for k, v in SECTION_PROPS.items()}

E_DEFAULT_MAP = {
    "Structural Steel (Fe250)":      200,
    "High-Strength Steel (Fe415)":   200,
    "Aluminium Alloy":                70,
    "Timber (Grade M30)":             12,
    "Concrete M25 (compression)":     25,
}
RHO_MAP = {
    "Structural Steel (Fe250)":     7850,
    "High-Strength Steel (Fe415)":  7850,
    "Aluminium Alloy":              2700,
    "Timber (Grade M30)":            600,
    "Concrete M25 (compression)":   2400,
}

# ─── Engineering solver ────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def solve_beam(span, loads, support_a, support_b, udl=0, udl_start=0, udl_end=None):
    if udl_end is None:
        udl_end = span
    if udl_end < udl_start:
        udl_start, udl_end = udl_end, udl_start

    total_point = sum(P for _, P in loads)
    udl_len     = udl_end - udl_start
    udl_total   = udl * udl_len
    udl_arm     = udl_start + udl_len / 2.0

    if support_a == "Pinned" and support_b == "Roller":
        Ma        = sum(P * x for x, P in loads) + udl_total * udl_arm
        Rb        = Ma / span
        Ra        = total_point + udl_total - Rb
        Ma_moment = 0
    else:
        Ra        = total_point + udl_total
        Rb        = 0
        Ma_moment = -(sum(P * x for x, P in loads) + udl_total * udl_arm)

    n   = 400
    xs  = np.linspace(0, span, n)
    total_load_solver = total_point + udl_total
    sfd_tol = max(1e-6 * abs(total_load_solver), 1e-9)

    sfd = np.full(n, Ra)
    bmd = Ra * xs + Ma_moment

    for xi, Pi in loads:
        mask = xs > xi
        sfd  = np.where(mask, sfd - Pi, sfd)
        bmd  = np.where(mask, bmd - Pi * (xs - xi), bmd)

    if udl > 0 and udl_end > udl_start:
        in_udl  = xs > udl_start
        covered = np.where(in_udl, np.minimum(xs, udl_end) - udl_start, 0.0)
        sfd    -= udl * covered
        cov_bmd = np.where(in_udl, np.minimum(xs, udl_end) - udl_start, 0.0)
        bmd    -= udl * cov_bmd * (xs - udl_start - cov_bmd / 2.0)

    sfd = np.where(np.abs(sfd) < sfd_tol, 0.0, sfd)

    max_bmd_abs = max(abs(bmd)) if max(abs(bmd)) > 0 else 1
    bmd_norm    = np.abs(bmd) / max_bmd_abs

    return {
        "Ra": Ra, "Rb": Rb, "Ma_moment": Ma_moment,
        "xs": xs, "sfd": sfd, "bmd": bmd, "bmd_norm": bmd_norm,
        "max_sfd": float(np.max(np.abs(sfd))),
        "max_bmd": float(np.max(np.abs(bmd))),
        "udl_start": udl_start, "udl_end": udl_end,
    }


def safety_factor(max_stress_kNm, section, material):
    Z      = Z_MAP.get(section, 200.0)
    fy     = FY_MAP.get(material, 250)
    Z_mm3  = Z * 1000
    M_Nmm  = max_stress_kNm * 1e6
    sigma  = M_Nmm / Z_mm3 if Z_mm3 > 0 else 0
    sf     = min(fy / sigma, 999.0) if sigma > 0 else 999.0
    return round(sf, 2), round(sigma, 1)


# ─── New engineering functions ────────────────────────────────────────────────

def moment_capacity_is800(section, material, gamma_m0=1.10):
    Z_cm3  = Z_MAP.get(section, 200.0)
    fy     = FY_MAP.get(material, 250)
    Md_Nmm = fy * Z_cm3 * 1000 / gamma_m0
    return Md_Nmm / 1e6  # kN·m


def shear_capacity_is800(section, material, gamma_m0=1.10):
    props = SECTION_PROPS.get(section, SECTION_PROPS["Rectangle 100×200mm"])
    A_web = props.get("A_web_mm2", 20000.0)
    fy    = FY_MAP.get(material, 250)
    Vd_N  = 0.6 * fy * A_web / (np.sqrt(3) * gamma_m0)
    return Vd_N / 1000  # kN


def natural_frequency(span, E_GPa, I_cm4, section, material, sup_type):
    E     = E_GPa * 1e9
    I     = I_cm4 * 1e-8
    rho   = RHO_MAP.get(material, 7850)
    A_m2  = SECTION_PROPS.get(section, {}).get("A_cm2", 20.0) * 1e-4
    m_bar = rho * A_m2
    if m_bar <= 0 or span <= 0:
        return 0.0
    EI    = E * I
    coeff = (np.pi / (2 * span**2)) if sup_type == "simply_supported" \
            else (1.8751**2 / (2 * np.pi * span**2))
    return round(coeff * np.sqrt(EI / m_bar), 3)


def compute_deflection_data(xs, bmd, span, E_GPa, I_cm4, support_type="simply_supported"):
    E   = E_GPa * 1e9
    I   = I_cm4 * 1e-8
    EI  = E * I
    M   = -bmd * 1e3
    dx  = xs[1] - xs[0]

    curvature = M / EI
    slope = np.concatenate([[0.0], np.cumsum(0.5 * (curvature[:-1] + curvature[1:]) * dx)])
    defl  = np.concatenate([[0.0], np.cumsum(0.5 * (slope[:-1]     + slope[1:])     * dx)])

    if support_type == "cantilever":
        defl *= -1
    else:
        corr  = np.interp(xs, [xs[0], xs[-1]], [defl[0], defl[-1]])
        defl -= corr

    defl_mm = defl * 1000
    return defl_mm, float(defl_mm[np.argmax(np.abs(defl_mm))])


# ─── Plot configuration ───────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": SURF,
    "axes.edgecolor": BORD, "axes.labelcolor": MUTE,
    "xtick.color": MUTE, "ytick.color": MUTE,
    "grid.color": BORD, "text.color": TEXT,
    "font.family": "monospace", "font.size": 9,
})


def plot_beam(span, loads, support_a, support_b, res, udl=0, udl_start=0, udl_end=None, udl_arrows=8):
    if udl_end is None:
        udl_end = span
    xs       = res["xs"]
    bmd_norm = res["bmd_norm"]
    Ra, Rb   = res["Ra"], res["Rb"]

    fig, ax = plt.subplots(figsize=(12, 4.0))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(SURF)

    beam_y  = 0.0
    beam_h  = 0.22
    beam_hi = beam_y + beam_h

    img = STRESS_CMAP(bmd_norm).reshape(1, len(bmd_norm), 4)
    ax.imshow(img, aspect='auto', extent=[xs[0], xs[-1], beam_y, beam_hi],
              origin='lower', zorder=1)

    ax.plot([0, span], [beam_y, beam_y],     color=BORD, lw=1)
    ax.plot([0, span], [beam_hi, beam_hi],   color=BORD, lw=1)
    ax.plot([0, 0],    [beam_y, beam_hi],    color=BORD, lw=1)
    ax.plot([span, span], [beam_y, beam_hi], color=BORD, lw=1)

    if udl > 0:
        udl_sc = max((udl / 50.0) * 0.4, 0.12)
        ax.fill_between([udl_start, udl_end], beam_hi, beam_hi + udl_sc * 0.7,
                        color=ACC, alpha=0.25, linewidth=0)
        ax.plot([udl_start, udl_end], [beam_hi + udl_sc * 0.7]*2,
                color=ACC, lw=1.2, linestyle="--")
        for wx in np.linspace(udl_start, udl_end, udl_arrows):
            ax.annotate("", xy=(wx, beam_hi), xytext=(wx, beam_hi + udl_sc * 0.7),
                        arrowprops=dict(arrowstyle="-|>", color=ACC, lw=0.8))
        ax.text((udl_start+udl_end)/2, beam_hi + udl_sc*0.7 + 0.05,
                f"w = {udl} kN/m", ha="center", fontsize=8, color=ACC, style="italic")

    arrow_h = 0.6
    for xi, Pi in loads:
        ax.plot([xi, xi], [beam_hi, beam_hi + arrow_h], color=RED, lw=1.8, solid_capstyle='round')
        ax.annotate("", xy=(xi, beam_hi + 0.02), xytext=(xi, beam_hi + arrow_h),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8, mutation_scale=14))
        ax.text(xi, beam_hi + arrow_h + 0.07, f"{Pi} kN",
                ha="center", fontsize=8.5, color=RED, fontweight="bold")

    def draw_support(x_pos, label, reaction, sup_type):
        if sup_type == "Pinned":
            tri_x = [x_pos - 0.22, x_pos + 0.22, x_pos, x_pos - 0.22]
            tri_y = [beam_y - 0.27, beam_y - 0.27, beam_y, beam_y - 0.27]
            ax.fill(tri_x, tri_y, color="#388bfd", alpha=0.25)
            ax.plot(tri_x, tri_y, color=ACC, lw=1)
            for hx in np.linspace(x_pos - 0.28, x_pos + 0.28, 6):
                ax.plot([hx, hx - 0.1], [beam_y - 0.30, beam_y - 0.40], color=ACC, lw=0.8, alpha=0.6)
            ax.plot([x_pos - 0.32, x_pos + 0.32], [beam_y - 0.30, beam_y - 0.30], color=ACC, lw=1.2)
        elif sup_type == "Roller":
            tri_x = [x_pos - 0.22, x_pos + 0.22, x_pos, x_pos - 0.22]
            tri_y = [beam_y - 0.27, beam_y - 0.27, beam_y, beam_y - 0.27]
            ax.fill(tri_x, tri_y, color="#3fb950", alpha=0.20)
            ax.plot(tri_x, tri_y, color=GRN, lw=1)
            for cx in [x_pos - 0.14, x_pos, x_pos + 0.14]:
                circle = MplCircle((cx, beam_y - 0.33), 0.045, color=GRN, fill=False, lw=0.9)
                ax.add_patch(circle)
            ax.plot([x_pos - 0.32, x_pos + 0.32], [beam_y - 0.38, beam_y - 0.38], color=GRN, lw=1.2)
        elif sup_type == "Fixed":
            wall_w, wall_h = 0.18, 0.55
            ax.fill([x_pos - wall_w, x_pos, x_pos, x_pos - wall_w],
                    [beam_y - wall_h, beam_y - wall_h, beam_hi, beam_hi], color="#388bfd", alpha=0.18)
            ax.plot([x_pos, x_pos], [beam_y - wall_h, beam_hi], color=ACC, lw=2.5)
            for hy in np.linspace(beam_y - wall_h + 0.06, beam_hi - 0.06, 7):
                ax.plot([x_pos - wall_w, x_pos - wall_w + 0.12], [hy, hy - 0.10],
                        color=ACC, lw=0.8, alpha=0.55)
        elif sup_type == "Free":
            ax.plot([x_pos, x_pos], [beam_y - 0.45, beam_hi],
                    color=MUTE, lw=1.0, linestyle="--", alpha=0.6)

        if sup_type != "Free":
            label_y     = beam_y - 0.52
            label_color = GRN if sup_type == "Roller" else ACC
            if sup_type == "Fixed":
                sign_label = "hogging" if res["Ma_moment"] < 0 else "sagging"
                txt = f"{label}\nM={abs(res['Ma_moment']):.1f} kN·m\n({sign_label})"
            else:
                txt = f"{label}\n{reaction:.1f} kN"
            ax.text(x_pos, label_y, txt, ha="center", fontsize=8, color=label_color, linespacing=1.4)

    draw_support(0,    "A", Ra, support_a)
    draw_support(span, "B", Rb, support_b)

    sm = plt.cm.ScalarMappable(cmap=STRESS_CMAP, norm=plt.Normalize(0, 1))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation="vertical", pad=0.01, fraction=0.02)
    cbar.set_label("Stress intensity", color=MUTE, fontsize=8)
    cbar.ax.yaxis.set_tick_params(color=MUTE)
    cbar.set_ticks([0, 0.5, 1])
    cbar.set_ticklabels(["Low", "Med", "High"])
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=MUTE, fontsize=7)

    idx_mmax = int(np.argmax(np.abs(res["bmd"])))
    mmax_x   = res["xs"][idx_mmax]
    mmax_val = res["bmd"][idx_mmax]
    if abs(mmax_val) > 0:
        sign_str = "+" if mmax_val >= 0 else ""
        ax.scatter([mmax_x], [beam_hi + 0.05], color=YEL, s=28, zorder=5)
        ax.text(mmax_x, beam_hi + 0.12, f"M={sign_str}{mmax_val:.1f} kN·m",
                ha="center", fontsize=7.5, color=YEL, fontweight="bold")

    ax.set_xlim(-0.5, span + 0.5)
    ax.set_ylim(-0.75, 1.4)
    ax.set_xlabel("Position along beam (m)", fontsize=9, color=MUTE)
    ax.set_title("BEAM — Stress Distribution", fontsize=10, color=TEXT,
                 fontweight="bold", pad=8, loc="left")
    ax.set_yticks([])
    ax.grid(axis="x", alpha=0.15, lw=0.4, linestyle=":")
    for spine in ax.spines.values():
        spine.set_edgecolor(BORD)
    plt.tight_layout(pad=0.5)
    return fig


def plot_sfd(xs, sfd, span):
    """SFD with V=0 zero-crossing markers (indicates M_max locations)."""
    fig, ax = plt.subplots(figsize=(12, 3.2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(SURF)
    ax.fill_between(xs, 0, sfd, where=(sfd >= 0), color=ACC, alpha=0.4, linewidth=0)
    ax.fill_between(xs, 0, sfd, where=(sfd <  0), color=RED, alpha=0.4, linewidth=0)
    ax.plot(xs, sfd, color=ACC, lw=1.5)
    ax.axhline(0, color=BORD, lw=0.8)

    sign_changes = np.where(np.diff(np.sign(sfd)))[0]
    for idx in sign_changes:
        x0, x1 = xs[idx], xs[idx + 1]
        v0, v1 = sfd[idx], sfd[idx + 1]
        x_zero = x0 - v0 * (x1 - x0) / (v1 - v0) if abs(v1 - v0) > 1e-12 else (x0 + x1) / 2
        ax.axvline(x_zero, color=YEL, lw=1.0, linestyle=":", alpha=0.7)
        ax.scatter([x_zero], [0], color=YEL, s=30, zorder=5)
        v_range = max(abs(sfd)) if max(abs(sfd)) > 0 else 1.0
        ax.text(x_zero + span * 0.01, v_range * 0.06,
                f"V=0\nx={x_zero:.2f}m", fontsize=7, color=YEL, va="bottom")

    ax.set_xlim(0, span)
    ax.set_xlabel("Position (m)", fontsize=9, color=MUTE)
    ax.set_ylabel("Shear (kN)", fontsize=9, color=MUTE)
    ax.set_title("SHEAR FORCE DIAGRAM", fontsize=10, color=TEXT,
                 fontweight="bold", pad=8, loc="left")
    ax.grid(alpha=0.15, lw=0.4, linestyle=":")
    for spine in ax.spines.values():
        spine.set_edgecolor(BORD)
    idx_max = np.argmax(np.abs(sfd))
    ax.annotate(f"  {sfd[idx_max]:.1f} kN", xy=(xs[idx_max], sfd[idx_max]),
                fontsize=8, color=YEL)
    plt.tight_layout(pad=0.5)
    return fig


def plot_bmd(xs, bmd, span):
    """BMD with inflection point markers (M=0 sign changes)."""
    fig, ax = plt.subplots(figsize=(12, 3.2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(SURF)
    ax.fill_between(xs, 0, bmd, where=(bmd >= 0), color=GRN, alpha=0.4, linewidth=0)
    ax.fill_between(xs, 0, bmd, where=(bmd <  0), color=RED, alpha=0.4, linewidth=0)
    ax.plot(xs, bmd, color=GRN, lw=1.5)
    ax.axhline(0, color=BORD, lw=0.8)

    sign_changes = np.where(np.diff(np.sign(bmd)))[0]
    m_range = max(abs(bmd)) if max(abs(bmd)) > 0 else 1.0
    for idx in sign_changes:
        x0, x1 = xs[idx], xs[idx + 1]
        m0, m1 = bmd[idx], bmd[idx + 1]
        x_infl = x0 - m0 * (x1 - x0) / (m1 - m0) if abs(m1 - m0) > 1e-12 else (x0 + x1) / 2
        ax.scatter([x_infl], [0], color=RED, s=40, zorder=6, marker="D")
        ax.text(x_infl + span * 0.01, m_range * 0.04,
                f"IP\n{x_infl:.2f}m", fontsize=7, color=RED, va="bottom")

    ax.set_xlim(0, span)
    ax.set_xlabel("Position (m)", fontsize=9, color=MUTE)
    ax.set_ylabel("Moment (kN·m)", fontsize=9, color=MUTE)
    ax.set_title("BENDING MOMENT DIAGRAM", fontsize=10, color=TEXT,
                 fontweight="bold", pad=8, loc="left")
    ax.grid(alpha=0.15, lw=0.4, linestyle=":")
    for spine in ax.spines.values():
        spine.set_edgecolor(BORD)
    idx_max = np.argmax(np.abs(bmd))
    ax.annotate(f"  {bmd[idx_max]:.1f} kN·m", xy=(xs[idx_max], bmd[idx_max]),
                fontsize=8, color=YEL)
    plt.tight_layout(pad=0.5)
    return fig


def plot_deflection(xs, defl_mm, span):
    """Plot pre-computed deflection array."""
    fig, ax = plt.subplots(figsize=(12, 3.2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(SURF)
    ax.fill_between(xs, 0, defl_mm, color=PURP, alpha=0.35, linewidth=0)
    ax.plot(xs, defl_mm, color=PURP, lw=1.5)
    ax.axhline(0, color=BORD, lw=0.8, linestyle="--")
    ax.set_xlim(0, span)
    ax.set_xlabel("Position (m)", fontsize=9, color=MUTE)
    ax.set_ylabel("Deflection (mm)", fontsize=9, color=MUTE)
    ax.set_title("DEFLECTION CURVE (approximate)", fontsize=10, color=TEXT,
                 fontweight="bold", pad=8, loc="left")
    ax.grid(alpha=0.15, lw=0.4, linestyle=":")
    for spine in ax.spines.values():
        spine.set_edgecolor(BORD)
    idx = np.argmax(np.abs(defl_mm))
    ax.annotate(f"  δ_max = {defl_mm[idx]:.2f} mm", xy=(xs[idx], defl_mm[idx]),
                fontsize=8, color=YEL)
    plt.tight_layout(pad=0.5)
    return fig


def plot_position_query(xs, sfd, bmd, defl_mm, span, x_q):
    """3-panel figure with vertical query marker at x_q."""
    fig, axes = plt.subplots(3, 1, figsize=(12, 7.5), sharex=True)
    fig.patch.set_facecolor(BG)
    fig.subplots_adjust(hspace=0.06)

    v_q = float(np.interp(x_q, xs, sfd))
    m_q = float(np.interp(x_q, xs, bmd))
    d_q = float(np.interp(x_q, xs, defl_mm))

    datasets = [
        (sfd,     "Shear Force (kN)",   ACC,  "SHEAR FORCE"),
        (bmd,     "Moment (kN·m)",      GRN,  "BENDING MOMENT"),
        (defl_mm, "Deflection (mm)",    PURP, "DEFLECTION"),
    ]
    vals = [v_q, m_q, d_q]

    for ax, (data, ylabel, color, title), val in zip(axes, datasets, vals):
        ax.set_facecolor(SURF)
        ax.fill_between(xs, 0, data, color=color, alpha=0.25, linewidth=0)
        ax.plot(xs, data, color=color, lw=1.5)
        ax.axhline(0, color=BORD, lw=0.8, linestyle="--", alpha=0.6)
        ax.axvline(x_q, color=YEL, lw=1.2, linestyle="--", alpha=0.85, zorder=4)
        ax.scatter([x_q], [val], color=YEL, s=55, zorder=6)
        ax.text(x_q + span * 0.02, val, f"  {val:.2f}", fontsize=8.5,
                color=YEL, va="center", fontweight="bold")
        ax.set_ylabel(ylabel, fontsize=8, color=MUTE)
        ax.set_title(title, fontsize=8.5, color=TEXT, fontweight="bold", loc="left", pad=4)
        ax.grid(alpha=0.12, lw=0.4, linestyle=":")
        ax.set_xlim(0, span)
        for spine in ax.spines.values():
            spine.set_edgecolor(BORD)

    axes[-1].set_xlabel("Position (m)", fontsize=9, color=MUTE)
    plt.tight_layout(pad=0.4)
    return fig, v_q, m_q, d_q


def plot_cross_section(section, M_kNm):
    """Cross-section with bending stress gradient + profile diagram."""
    props  = SECTION_PROPS.get(section, SECTION_PROPS["Rectangle 100×200mm"])
    shape  = props["shape"]
    dims   = props["dims"]
    I_cm4  = props["I_cm4"]
    y_top  = props["y_top_mm"]
    y_bot  = props["y_bot_mm"]
    I_mm4  = I_cm4 * 1e4
    M_Nmm  = M_kNm * 1e6

    sigma_top = -M_Nmm * y_top / I_mm4 if I_mm4 > 0 else 0.0
    sigma_bot =  M_Nmm * y_bot / I_mm4 if I_mm4 > 0 else 0.0

    STRESS_SECTION_CMAP = LinearSegmentedColormap.from_list(
        "stress_sec", ["#4a80c0", "#dce8f5", "#b06070"], N=512
    )

    fig, (ax_sec, ax_str) = plt.subplots(1, 2, figsize=(10, 5.5),
                                          gridspec_kw={"width_ratios": [1.6, 1]})
    fig.patch.set_facecolor(BG)
    for ax in (ax_sec, ax_str):
        ax.set_facecolor(SURF)
        for sp in ax.spines.values():
            sp.set_edgecolor(BORD)

    extremes = max(abs(sigma_top), abs(sigma_bot), 1e-9)

    def strip_color(y_from_na):
        s = -M_Nmm * y_from_na / I_mm4 if I_mm4 > 0 else 0.0
        return STRESS_SECTION_CMAP(np.clip((s / extremes + 1) / 2, 0, 1))

    N_STRIPS = 60

    def fill_rect_strips(x_l, x_r, y_b_na, y_t_na):
        ys = np.linspace(y_b_na, y_t_na, N_STRIPS + 1)
        for j in range(N_STRIPS):
            y_mid = (ys[j] + ys[j+1]) / 2
            col   = strip_color(y_mid)
            rect  = mpatches.Rectangle(
                (x_l, ys[j]), x_r - x_l, ys[j+1] - ys[j],
                facecolor=col, edgecolor="none"
            )
            ax_sec.add_patch(rect)
        ax_sec.plot([x_l, x_r, x_r, x_l, x_l],
                    [y_b_na, y_b_na, y_t_na, y_t_na, y_b_na], color=BORD, lw=1.0)

    if shape == "rect":
        b, h = dims["b"], dims["h"]
        fill_rect_strips(-b/2, b/2, -y_bot, y_top)
        ax_sec.set_xlim(-b * 0.85, b * 0.85)

    elif shape == "ipe":
        b, tf, tw = dims["b"], dims["tf"], dims["tw"]
        fill_rect_strips(-b/2,  b/2,   y_top - tf, y_top)
        fill_rect_strips(-tw/2, tw/2, -y_bot + tf, y_top - tf)
        fill_rect_strips(-b/2,  b/2,  -y_bot,     -y_bot + tf)
        ax_sec.set_xlim(-b * 0.85, b * 0.85)

    elif shape == "circle":
        d = dims["d"]
        r = d / 2
        ys = np.linspace(-r, r, N_STRIPS + 1)
        for j in range(N_STRIPS):
            y_mid  = (ys[j] + ys[j+1]) / 2
            chord  = np.sqrt(max(r**2 - y_mid**2, 0))
            col    = strip_color(y_mid)
            rect   = mpatches.Rectangle((-chord, ys[j]), 2 * chord, ys[j+1] - ys[j],
                                        facecolor=col, edgecolor="none")
            ax_sec.add_patch(rect)
        theta = np.linspace(0, 2*np.pi, 200)
        ax_sec.plot(r * np.cos(theta), r * np.sin(theta), color=BORD, lw=1.2)
        ax_sec.set_xlim(-r * 1.6, r * 1.6)

    elif shape == "tee":
        b, tf, tw = dims["b"], dims["tf"], dims["tw"]
        fill_rect_strips(-b/2,  b/2,   y_top - tf,  y_top)
        fill_rect_strips(-tw/2, tw/2, -y_bot,        y_top - tf)
        ax_sec.set_xlim(-b * 0.75, b * 0.75)

    # Neutral axis
    ax_sec.axhline(0, color=YEL, lw=1.0, linestyle="--", alpha=0.8)
    xlim = ax_sec.get_xlim()
    ax_sec.text(xlim[0] * 0.80, y_top * 0.08, "N.A.", fontsize=7.5, color=YEL)

    # Zone labels
    if y_top > 2:
        ax_sec.text(0, y_top * 0.55, "COMPRESSION", ha="center",
                    fontsize=7, color="#4a80c0", fontstyle="italic", alpha=0.8)
    if y_bot > 2:
        ax_sec.text(0, -y_bot * 0.55, "TENSION", ha="center",
                    fontsize=7, color=RED, fontstyle="italic", alpha=0.8)

    ax_sec.set_xlabel("Width (mm)", fontsize=8, color=MUTE)
    ax_sec.set_ylabel("Height from N.A. (mm)", fontsize=8, color=MUTE)
    ax_sec.set_title(f"CROSS-SECTION  |  {section}", fontsize=9, color=TEXT,
                     fontweight="bold", pad=6, loc="left")
    ax_sec.set_aspect("equal", adjustable="datalim")
    ax_sec.grid(alpha=0.10, lw=0.4)

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap=STRESS_SECTION_CMAP, norm=plt.Normalize(-1, 1))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax_sec, orientation="vertical", pad=0.02, fraction=0.035)
    cbar.set_label("σ  comp → tens", color=MUTE, fontsize=7)
    cbar.set_ticks([-1, 0, 1])
    cbar.set_ticklabels(["Comp.", "0", "Tens."])
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=MUTE, fontsize=7)

    # ── Stress profile panel ──────────────────────────────────────────────
    total_h = y_top + y_bot
    y_range = np.linspace(-y_bot, y_top, 300)
    sigma_arr = -M_Nmm * y_range / I_mm4 if I_mm4 > 0 else np.zeros(300)

    ax_str.plot(sigma_arr, y_range, color=ACC, lw=1.8)
    ax_str.fill_betweenx(y_range, 0, sigma_arr, where=(sigma_arr < 0),
                         color="#4a80c0", alpha=0.35, linewidth=0)
    ax_str.fill_betweenx(y_range, 0, sigma_arr, where=(sigma_arr >= 0),
                         color=RED, alpha=0.35, linewidth=0)
    ax_str.axhline(0, color=YEL, lw=1.0, linestyle="--", alpha=0.8)
    ax_str.axvline(0, color=BORD, lw=0.8)

    ax_str.scatter([sigma_top], [y_top],  color="#4a80c0", s=40, zorder=5)
    ax_str.scatter([sigma_bot], [-y_bot], color=RED,       s=40, zorder=5)
    ax_str.text(sigma_top,  y_top  + total_h * 0.04,
                f"{sigma_top:.1f} MPa", fontsize=7.5, color="#4a80c0",
                ha="center", fontweight="bold")
    ax_str.text(sigma_bot, -y_bot  - total_h * 0.06,
                f"+{sigma_bot:.1f} MPa", fontsize=7.5, color=RED,
                ha="center", fontweight="bold")

    ax_str.set_xlabel("Bending Stress σ (MPa)", fontsize=8, color=MUTE)
    ax_str.set_ylabel("Height from N.A. (mm)", fontsize=8, color=MUTE)
    ax_str.set_title("STRESS PROFILE", fontsize=9, color=TEXT,
                     fontweight="bold", pad=6, loc="left")
    ax_str.grid(alpha=0.12, lw=0.4)

    plt.tight_layout(pad=0.6)
    return fig


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 0 4px 0;'>
      <div style='font-size:18px;font-weight:700;color:#e6edf3;
        font-family:Space Grotesk,sans-serif;letter-spacing:-0.3px;'>⚙️ Beam Setup</div>
      <div style='height:1px;background:linear-gradient(90deg,rgba(56,139,253,0.5),transparent);
        margin-top:8px;'></div>
    </div>
    """, unsafe_allow_html=True)

    span = st.slider("Beam Span (m)", min_value=1.0, max_value=20.0, value=6.0, step=0.5)

    support_a = st.selectbox("Support A (left end)", ["Pinned", "Fixed"], index=0)
    if support_a == "Pinned":
        support_b = st.selectbox("Support B (right end)", ["Roller"], index=0, key="sb_pinned")
    else:
        support_b = st.selectbox("Support B (right end)", ["Free"], index=0, key="sb_fixed")

    st.markdown(
        "<div style='height:1px;background:linear-gradient(90deg,rgba(180,198,220,0.15),transparent);"
        "margin:12px 0 10px 0;'></div><div class='sidebar-section'>📐 Cross-Section</div>",
        unsafe_allow_html=True
    )
    section  = st.selectbox("Section Profile", list(SECTION_PROPS.keys()))
    material = st.selectbox("Material", list(FY_MAP.keys()))

    # Section properties display
    with st.expander("📊  Section Properties"):
        sp = SECTION_PROPS[section]
        st.markdown(f"""
        <table style='width:100%;font-family:DM Mono,monospace;font-size:10.5px;
                      color:#8aa0ba;border-collapse:collapse;'>
          <tr><td style='padding:3px 6px;opacity:.55;'>A</td>
              <td style='padding:3px 0;text-align:right;color:#dce8f5;'>{sp['A_cm2']} cm²</td></tr>
          <tr><td style='padding:3px 6px;opacity:.55;'>I</td>
              <td style='padding:3px 0;text-align:right;color:#dce8f5;'>{sp['I_cm4']} cm⁴</td></tr>
          <tr><td style='padding:3px 6px;opacity:.55;'>Ze</td>
              <td style='padding:3px 0;text-align:right;color:#dce8f5;'>{sp['Z_cm3']} cm³</td></tr>
          <tr><td style='padding:3px 6px;opacity:.55;'>r</td>
              <td style='padding:3px 0;text-align:right;color:#dce8f5;'>{sp['r_cm']} cm</td></tr>
          <tr><td style='padding:3px 6px;opacity:.55;'>y_top</td>
              <td style='padding:3px 0;text-align:right;color:#dce8f5;'>{sp['y_top_mm']} mm</td></tr>
          <tr><td style='padding:3px 6px;opacity:.55;'>y_bot</td>
              <td style='padding:3px 0;text-align:right;color:#dce8f5;'>{sp['y_bot_mm']} mm</td></tr>
          <tr><td style='padding:3px 6px;opacity:.55;font-size:9px;' colspan=2>{sp['desc']}</td></tr>
        </table>
        """, unsafe_allow_html=True)

    # Auto-populated advanced parameters
    with st.expander("⚙️  Advanced Parameters"):
        E_GPa = st.number_input(
            "E — Elastic Modulus (GPa)",
            value=E_DEFAULT_MAP.get(material, 200),
            min_value=1, max_value=400,
            key=f"E_{material}"
        )
        I_cm4 = st.number_input(
            "I — Moment of Inertia (cm⁴)",
            value=int(SECTION_PROPS[section]["I_cm4"]),
            min_value=10, max_value=500000,
            key=f"I_{section}"
        )

    # Load factor
    st.markdown(
        "<div style='height:1px;background:linear-gradient(90deg,rgba(180,198,220,0.15),transparent);"
        "margin:12px 0 10px 0;'></div><div class='sidebar-section'>⚖️ Load Factor γ_f</div>",
        unsafe_allow_html=True
    )
    gamma_f = st.radio(
        "Apply load factor",
        options=[1.0, 1.2, 1.5],
        format_func=lambda x: f"γ_f = {x}  {'(Characteristic)' if x == 1.0 else '(Design)'}",
        index=0,
    )

    st.markdown(
        "<div style='height:1px;background:linear-gradient(90deg,rgba(180,198,220,0.15),transparent);"
        "margin:12px 0 10px 0;'></div><div class='sidebar-section'>🌊 Distributed Load (UDL)</div>",
        unsafe_allow_html=True
    )
    udl        = st.slider("UDL Intensity (kN/m)", 0.0, 50.0, 0.0, 1.0)
    udl_start  = st.slider("UDL Start (m)", 0.0, span, 0.0, 0.5)
    udl_end_min = udl_start if udl_start < span else max(0.0, span - 0.5)
    udl_end    = st.slider("UDL End (m)", udl_end_min, span, float(span), 0.5)
    udl_arrows = st.slider("Number of load arrows", 2, 20, 8, 1)

    st.markdown(
        "<div style='height:1px;background:linear-gradient(90deg,rgba(180,198,220,0.15),transparent);"
        "margin:12px 0 10px 0;'></div><div class='sidebar-section'>🎯 Point Loads</div>",
        unsafe_allow_html=True
    )
    n_loads = st.number_input("Number of point loads", 0, 6, 1)

    is_cantilever_sidebar = (support_a == "Fixed")
    if is_cantilever_sidebar and int(n_loads) > 0:
        st.markdown(
            "<div style='font-size:11px;color:#e3b341;padding:2px 0 6px 0;"
            "font-family:JetBrains Mono,monospace;'>💡 Tip load defaults to the free end (x = span).</div>",
            unsafe_allow_html=True
        )

    loads = []
    for i in range(int(n_loads)):
        c1, c2 = st.columns(2)
        with c1:
            default_x = float(span) if is_cantilever_sidebar \
                        else round(span / (int(n_loads) + 1) * (i + 1), 1)
            xi = st.number_input(
                f"x{i+1} (m)", 0.0, float(span),
                min(default_x, float(span)), step=0.1, key=f"x{i}"
            )
        with c2:
            Pi = st.number_input(f"P{i+1} (kN)", 0.1, 500.0, 10.0, step=1.0, key=f"p{i}")
        loads.append((float(xi), float(Pi)))

    st.markdown(
        "<div style='height:1px;background:linear-gradient(90deg,rgba(180,198,220,0.15),transparent);"
        "margin:12px 0 10px 0;'></div>",
        unsafe_allow_html=True
    )
    st.info("⚡ Results update live as you change inputs above.")


# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding:36px 0 20px 0; text-align:center;'>
  <div style='font-size:12px; letter-spacing:0.32em; text-transform:uppercase;
    color:rgba(180,198,220,0.5); font-family:DM Mono,monospace;
    font-weight:500; margin-bottom:16px;'>Structural Engineering Suite</div>
  <div style='font-size:72px; font-weight:300; font-family:Cormorant Garamond,serif;
    color:#dce8f5; line-height:1; letter-spacing:-0.02em; margin-bottom:6px;'>Mech Vision</div>
  <div style='font-size:24px; font-weight:300; font-style:italic;
    font-family:Cormorant Garamond,serif; color:rgba(180,198,220,0.55);
    letter-spacing:0.04em; margin-bottom:24px;'>Beam Load &amp; Stress Analyzer</div>
  <div style='display:flex; align-items:center; justify-content:center;
    gap:14px; margin-bottom:12px;'>
    <div style='height:1px; width:100px; background:rgba(180,198,220,0.20);'></div>
    <div style='width:5px; height:5px; border-radius:50%; background:rgba(180,198,220,0.50);'></div>
    <div style='height:1px; width:100px; background:rgba(180,198,220,0.20);'></div>
  </div>
</div>
<div style='height:1px; background:linear-gradient(90deg,transparent,rgba(180,198,220,0.25),transparent);
  margin-bottom:28px;'></div>
""", unsafe_allow_html=True)


# ─── Main analysis block ──────────────────────────────────────────────────────
sup_type = "cantilever" if (support_a == "Fixed" and support_b == "Free") else "simply_supported"

# Apply load factor to all loads before solve
factored_loads = tuple((x, P * gamma_f) for x, P in loads)
factored_udl   = udl * gamma_f

try:
    res = solve_beam(span, factored_loads, support_a, support_b,
                     factored_udl, udl_start, udl_end)
    sf, sigma = safety_factor(res["max_bmd"], section, material)

    udl_start_used = res["udl_start"]
    udl_end_used   = res["udl_end"]
    total_load     = (sum(P for _, P in factored_loads)
                      + factored_udl * (udl_end_used - udl_start_used))
    reaction_sum   = res["Ra"] + res["Rb"]
    equil_tol      = max(0.01 * total_load, 0.1)
    if total_load > 0 and abs(reaction_sum - total_load) > equil_tol:
        st.error(
            f"⚠️ Equilibrium error: Ra + Rb = {reaction_sum:.2f} kN "
            f"but total load = {total_load:.2f} kN. Check inputs."
        )

    # ── Load factor badge (only shown when loads are factored) ───────────
    if gamma_f > 1.0:
        badge_col, _ = st.columns([1, 5])
        with badge_col:
            st.markdown(
                f"<span class='lf-badge-design'>DESIGN  γ_f = {gamma_f}</span>",
                unsafe_allow_html=True
            )
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Metric cards ──────────────────────────────────────────────────────
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
            sf_cls = "metric-card-safe"
        elif sf >= 1.5:
            badge = f"<span class='warn-badge'>⚠ MARGINAL  SF={sf}</span>"
            sf_cls = "metric-card-warn"
        else:
            badge = f"<span class='fail-badge'>✗ FAILURE  SF={sf}</span>"
            sf_cls = "metric-card-fail"
        st.markdown(f"""<div class='metric-card {sf_cls}'>
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

    # ── IS 800 Design Check Row ───────────────────────────────────────────
    Md   = moment_capacity_is800(section, material)
    Vd   = shear_capacity_is800(section, material)
    mu_m = min(res["max_bmd"] / Md, 9.99) if Md > 0 else 0.0
    mu_v = min(res["max_sfd"] / Vd, 9.99) if Vd > 0 else 0.0
    f1   = natural_frequency(span, E_GPa, I_cm4, section, material, sup_type)

    # Pre-compute deflection (shared by Deflection tab and Query tab)
    defl_mm_arr, defl_max = compute_deflection_data(
        res["xs"], res["bmd"], span, E_GPa, I_cm4, sup_type
    )
    defl_limit  = (span * 1000) / (180 if is_cantilever else 250)
    defl_ratio  = abs(defl_max) / defl_limit if defl_limit > 0 else 0.0

    def mu_color(mu):
        if mu < 0.75: return GRN
        if mu < 1.00: return "#d4a040"
        return RED

    mc = mu_color(mu_m)
    vc = mu_color(mu_v)
    dc = mu_color(defl_ratio)

    st.markdown(f"""
    <div class='check-row'>
      <div class='check-chip'>
        <div class='check-chip-label'>IS 800 · Moment Capacity</div>
        <div class='check-chip-val' style='color:{mc};'>{mu_m*100:.1f}%</div>
        <div class='check-chip-sub'>M_Ed={res['max_bmd']:.1f} / Md={Md:.1f} kN·m</div>
      </div>
      <div class='check-chip'>
        <div class='check-chip-label'>IS 800 · Shear Capacity</div>
        <div class='check-chip-val' style='color:{vc};'>{mu_v*100:.1f}%</div>
        <div class='check-chip-sub'>V_Ed={res['max_sfd']:.1f} / Vd={Vd:.1f} kN</div>
      </div>
      <div class='check-chip'>
        <div class='check-chip-label'>Deflection Check (δ / limit)</div>
        <div class='check-chip-val' style='color:{dc};'>{defl_ratio*100:.1f}%</div>
        <div class='check-chip-sub'>δ={abs(defl_max):.2f}mm / {defl_limit:.1f}mm</div>
      </div>
      <div class='check-chip'>
        <div class='check-chip-label'>Natural Frequency f₁</div>
        <div class='check-chip-val' style='color:{ACC};'>{f1} Hz</div>
        <div class='check-chip-sub'>{'SS' if sup_type == 'simply_supported' else 'Cantilever'} mode · Euler–Bernoulli</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📐  Model",
        "⚡  Shear Force",
        "🌀  Bending Moment",
        "📉  Deflection",
        "🔍  Query Point",
        "⬡  Cross-Section",
    ])

    with tab1:
        fig1 = plot_beam(span, loads, support_a, support_b, res,
                         udl, udl_start, udl_end, udl_arrows)
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
        fig4 = plot_deflection(res["xs"], defl_mm_arr, span)
        st.pyplot(fig4, use_container_width=True)
        plt.close(fig4)

        defl_limit_max = (span * 1000) / 10
        limit_label    = "L/180 (cantilever)" if is_cantilever else "L/250"
        if abs(defl_max) > defl_limit_max:
            st.warning(
                f"⚠️ Deflection {abs(defl_max):.1f} mm exceeds L/10 = {defl_limit_max:.0f} mm "
                "— result may be unrealistic. Check E and I values."
            )
        elif abs(defl_max) <= defl_limit:
            st.success(
                f"✅ Deflection OK — δ_max = {abs(defl_max):.2f} mm  ≤  "
                f"{limit_label} = {defl_limit:.1f} mm"
            )
        else:
            st.error(
                f"❌ Deflection EXCEEDS limit — δ_max = {abs(defl_max):.2f} mm  >  "
                f"{limit_label} = {defl_limit:.1f} mm"
            )

    # ── Query Point tab ───────────────────────────────────────────────────
    with tab5:
        st.markdown("""
        <div style='font-family:DM Mono,monospace;font-size:9.5px;letter-spacing:0.16em;
             text-transform:uppercase;color:rgba(180,198,220,0.45);margin-bottom:12px;'>
        Query internal forces &amp; deflection at any position along the beam</div>
        """, unsafe_allow_html=True)

        x_query = st.slider(
            "Query position x (m)", 0.0, float(span),
            float(span) / 2, 0.01, key="x_query_slider"
        )

        fig_q, v_q, m_q, d_q = plot_position_query(
            res["xs"], res["sfd"], res["bmd"], defl_mm_arr, span, x_query
        )
        st.pyplot(fig_q, use_container_width=True)
        plt.close(fig_q)

        qc1, qc2, qc3 = st.columns(3)
        for col, label, val, unit in [
            (qc1, "Shear V(x)",      v_q, "kN"),
            (qc2, "Moment M(x)",     m_q, "kN·m"),
            (qc3, "Deflection δ(x)", d_q, "mm"),
        ]:
            with col:
                st.markdown(f"""
                <div class='metric-card' style='border-top-color:rgba(122,158,192,0.5);'>
                  <div class='metric-label'>{label}</div>
                  <div class='metric-value'>{val:.3f}</div>
                  <div class='metric-unit'>{unit}</div>
                </div>""", unsafe_allow_html=True)

    # ── Cross-Section tab ─────────────────────────────────────────────────
    with tab6:
        st.markdown("""
        <div style='font-family:DM Mono,monospace;font-size:9.5px;letter-spacing:0.16em;
             text-transform:uppercase;color:rgba(180,198,220,0.45);margin-bottom:12px;'>
        Bending stress distribution at any queried position along the beam</div>
        """, unsafe_allow_html=True)

        # Query position slider — moment at this x drives the stress diagram
        x_cs = st.slider(
            "Query position x (m)", 0.0, float(span),
            float(span) / 2, 0.01, key="x_cs_slider"
        )
        M_at_x = float(np.interp(x_cs, res["xs"], res["bmd"]))

        # Small info line showing which moment is being used
        idx_mmax = int(np.argmax(np.abs(res["bmd"])))
        x_mmax   = float(res["xs"][idx_mmax])
        st.markdown(
            f"<div style='font-family:DM Mono,monospace;font-size:9px;"
            f"color:rgba(140,165,190,0.45);margin-bottom:10px;letter-spacing:0.12em;'>"
            f"M at x = {x_cs:.2f} m → "
            f"<span style='color:#dce8f5;font-weight:600;'>{M_at_x:.2f} kN·m</span>"
            f" &nbsp;|&nbsp; M_max = {res['max_bmd']:.2f} kN·m at x = {x_mmax:.2f} m"
            f"</div>",
            unsafe_allow_html=True
        )

        fig_cs = plot_cross_section(section, M_at_x)
        st.pyplot(fig_cs, use_container_width=True)
        plt.close(fig_cs)

        _p     = SECTION_PROPS[section]
        _I_mm4 = _p["I_cm4"] * 1e4
        _M_Nmm = M_at_x * 1e6
        s_top  = -_M_Nmm * _p["y_top_mm"] / _I_mm4 if _I_mm4 > 0 else 0
        s_bot  =  _M_Nmm * _p["y_bot_mm"] / _I_mm4 if _I_mm4 > 0 else 0
        st.markdown(
            f"<div style='font-family:DM Mono,monospace;font-size:9px;"
            f"color:rgba(140,165,190,0.5);margin-top:8px;letter-spacing:0.12em;'>"
            f"σ_top = <span style='color:#4a80c0;'>{s_top:.1f} MPa (compression)</span>"
            f" &nbsp;|&nbsp; "
            f"σ_bot = <span style='color:#b06070;'>+{s_bot:.1f} MPa (tension)</span>"
            f" &nbsp;|&nbsp; M(x) = {M_at_x:.2f} kN·m &nbsp;|&nbsp; I = {_p['I_cm4']} cm⁴"
            f"</div>",
            unsafe_allow_html=True
        )

    # ── Raw data table ────────────────────────────────────────────────────
    with st.expander("📋 View Raw Data Table (SFD, BMD & Deflection)"):
        step = 50
        df = pd.DataFrame({
            "Position (m)":           np.round(res["xs"][::step], 3),
            "Shear Force (kN)":       np.round(res["sfd"][::step], 3),
            "Bending Moment (kN·m)":  np.round(res["bmd"][::step], 3),
            "Deflection (mm)":        np.round(defl_mm_arr[::step], 3),
            "BMD Normalised [0–1]":   np.round(res["bmd_norm"][::step], 3),
        })
        st.dataframe(df, use_container_width=True, height=280)

    # ── Engineering summary ───────────────────────────────────────────────
    with st.expander("📝 Engineering Summary"):
        fy_val        = FY_MAP.get(material, 250)
        defl_lim_lbl  = "L/180 (cantilever)" if is_cantilever else "L/250"
        defl_status   = "PASS" if abs(defl_max) <= defl_limit else "FAIL"
        moment_status = "PASS" if mu_m < 1.0 else "FAIL"
        shear_status  = "PASS" if mu_v < 1.0 else "FAIL"

        summary_df = pd.DataFrame({
            "Parameter": [
                "Beam Span", "Support Configuration", "Load Factor γ_f",
                "Total Applied Load (factored)",
                "Support A (Reaction)", "Support B (Reaction)",
                "Max Shear Force", "Max Bending Moment",
                "Max Bending Stress", "Material Yield Strength",
                "Safety Factor (classical)", "Safety Status",
                "IS 800 · Moment Utilisation", "IS 800 · Moment Check",
                "IS 800 · Shear Utilisation",  "IS 800 · Shear Check",
                "Max Deflection", f"Deflection Limit ({defl_lim_lbl})",
                "Deflection Check", "Natural Frequency f₁",
                "Section Profile", "Material",
            ],
            "Value": [
                f"{span} m", f"{support_a} – {support_b}", str(gamma_f),
                f"{total_load:.2f} kN",
                f"{res['Ra']:.2f} kN", f"{res['Rb']:.2f} kN",
                f"{res['max_sfd']:.2f} kN", f"{res['max_bmd']:.2f} kN·m",
                f"{sigma} MPa", f"{fy_val} MPa",
                str(sf),
                "SAFE" if sf >= 2.5 else ("MARGINAL" if sf >= 1.5 else "FAILURE"),
                f"{mu_m*100:.1f}%", moment_status,
                f"{mu_v*100:.1f}%", shear_status,
                f"{abs(defl_max):.2f} mm", f"{defl_limit:.1f} mm",
                defl_status, f"{f1} Hz",
                section, material,
            ]
        })

        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        if "Concrete" in material:
            st.warning(
                "Plain concrete cannot resist bending tension. "
                "Safety factor is indicative only — not valid for unreinforced concrete design."
            )

        st.markdown("<br>", unsafe_allow_html=True)
        csv_bytes = summary_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Engineering Summary (CSV)",
            data=csv_bytes, file_name="mech_vision_summary.csv",
            mime="text/csv", use_container_width=True,
        )

except Exception as e:
    st.error(f"⚠️ Solver error: {e}")
    st.info("Tip: Make sure point load positions are within the beam span.")
    import traceback
    st.code(traceback.format_exc(), language="python")

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:44px 0 32px 0; margin-top:36px;
  border-top:1px solid rgba(180,198,220,0.07);'>
  <div style='display:flex; align-items:center; justify-content:center;
    gap:18px; margin-bottom:20px;'>
    <div style='height:1px; width:60px;
      background:linear-gradient(90deg,transparent,rgba(180,198,220,0.2));'></div>
    <span style='color:rgba(180,198,220,0.25); font-size:10px;'>◆</span>
    <div style='height:1px; width:60px;
      background:linear-gradient(90deg,rgba(180,198,220,0.2),transparent);'></div>
  </div>
  <div style='display:inline-flex; align-items:center; gap:16px;
    font-family:Cinzel Decorative,serif; font-size:13px; font-weight:400;
    letter-spacing:0.18em; color:rgba(190,210,235,0.6);'>
    <span style='font-size:18px; color:rgba(180,198,220,0.55); line-height:1;'>✦</span>
    <span>Engineered by Yogesh S</span>
    <span style='font-size:18px; color:rgba(180,198,220,0.55); line-height:1;'>✦</span>
  </div>
</div>
""", unsafe_allow_html=True)
