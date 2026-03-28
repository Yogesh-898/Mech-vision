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

# ─── Custom CSS  ── Aurora Prism theme ───────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400;500&family=Rajdhani:wght@500;600;700&family=Cinzel+Decorative:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

/* ── Page background: single unified aurora glow ── */
.stApp {
  background-color: #060c1a;
  background-image:
    linear-gradient(rgba(56,189,248,0.028) 1px, transparent 1px),
    linear-gradient(90deg, rgba(56,189,248,0.028) 1px, transparent 1px),
    radial-gradient(ellipse 130% 90% at 50% 20%,
      rgba(99,102,241,0.30) 0%,
      rgba(56,189,248,0.18) 28%,
      rgba(139,92,246,0.10) 52%,
      transparent 72%);
  background-size:
    52px 52px, 52px 52px,
    100% 100%;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: linear-gradient(175deg, #060b18 0%, #08102a 60%, #060c1e 100%);
  border-right: 1px solid rgba(99,102,241,0.18);
  box-shadow: 4px 0 32px rgba(0,0,0,0.55);
}
section[data-testid="stSidebar"] * { color: #7a98c8 !important; }

/* ── Metric cards ── */
.metric-card {
  background: linear-gradient(145deg,
    rgba(14,20,44,0.90) 0%,
    rgba(10,16,36,0.95) 50%,
    rgba(12,18,40,0.88) 100%);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(99,102,241,0.14);
  border-top: 2px solid rgba(99,102,241,0.45);
  border-radius: 10px;
  padding: 20px 16px 16px;
  text-align: center;
  position: relative;
  overflow: hidden;
  transition: all 0.38s cubic-bezier(0.16,1,0.3,1);
  box-shadow: 0 4px 20px rgba(0,0,0,0.30),
              inset 0 1px 0 rgba(255,255,255,0.04);
}
.metric-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg,
    transparent, rgba(99,102,241,0.55), rgba(56,189,248,0.45), transparent);
  opacity: 0.7;
}
.metric-card:hover {
  border-top-color: rgba(56,189,248,0.75);
  box-shadow: 0 12px 40px rgba(0,0,0,0.45),
              0 0 28px rgba(56,189,248,0.08),
              inset 0 1px 0 rgba(255,255,255,0.06);
  transform: translateY(-4px);
}
.metric-card-safe { border-top-color: rgba(52,211,153,0.72) !important; }
.metric-card-safe::before { background: linear-gradient(90deg, transparent, rgba(52,211,153,0.5), transparent) !important; }
.metric-card-warn { border-top-color: rgba(251,191,36,0.72) !important; }
.metric-card-warn::before { background: linear-gradient(90deg, transparent, rgba(251,191,36,0.5), transparent) !important; }
.metric-card-fail {
  border-top-color: rgba(248,113,113,0.80) !important;
  box-shadow: 0 0 28px rgba(248,113,113,0.10) !important;
}
.metric-card-fail::before { background: linear-gradient(90deg, transparent, rgba(248,113,113,0.55), transparent) !important; }

.metric-label {
  font-size: 8.5px; letter-spacing: 0.24em; text-transform: uppercase;
  background: linear-gradient(90deg, #7c8fc4, #a8b8e0);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 10px;
  font-family: 'JetBrains Mono', monospace; font-weight: 400;
  opacity: 0.65;
}
.metric-value {
  font-size: 30px; font-weight: 600;
  background: linear-gradient(135deg, #e2f0ff 0%, #a5c8f0 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  font-family: 'Rajdhani', sans-serif; line-height: 1; letter-spacing: 0.02em;
}
.metric-unit {
  font-size: 9.5px;
  color: rgba(122,152,200,0.50);
  font-family: 'JetBrains Mono', monospace; margin-top: 6px; letter-spacing: 0.08em;
}

/* ── Safety Banner (full-width, next line) ── */
.safety-banner {
  width: 100%;
  border-radius: 18px;
  padding: 42px 52px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 40px;
  position: relative;
  overflow: hidden;
  margin-top: 22px;
  transition: all 0.38s cubic-bezier(0.16,1,0.3,1);
  box-shadow: 0 16px 64px rgba(0,0,0,0.55),
              inset 0 1px 0 rgba(255,255,255,0.07);
}
.safety-banner::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
}
.safety-banner-safe {
  background: linear-gradient(135deg,
    rgba(14,38,30,0.96) 0%,
    rgba(10,28,22,0.98) 50%,
    rgba(12,34,26,0.94) 100%);
  border: 1px solid rgba(52,211,153,0.22);
  border-top: 3px solid rgba(52,211,153,0.75);
}
.safety-banner-safe::before {
  background: linear-gradient(90deg, transparent, rgba(52,211,153,0.65), rgba(56,189,248,0.40), transparent);
}
.safety-banner-warn {
  background: linear-gradient(135deg,
    rgba(38,30,10,0.96) 0%,
    rgba(28,22,8,0.98) 50%,
    rgba(34,26,10,0.94) 100%);
  border: 1px solid rgba(251,191,36,0.22);
  border-top: 3px solid rgba(251,191,36,0.75);
}
.safety-banner-warn::before {
  background: linear-gradient(90deg, transparent, rgba(251,191,36,0.65), rgba(245,158,11,0.40), transparent);
}
.safety-banner-fail {
  background: linear-gradient(135deg,
    rgba(38,10,10,0.96) 0%,
    rgba(28,8,8,0.98) 50%,
    rgba(34,10,10,0.94) 100%);
  border: 1px solid rgba(248,113,113,0.22);
  border-top: 3px solid rgba(248,113,113,0.80);
  animation: failGlow 2.4s ease infinite;
}
.safety-banner-fail::before {
  background: linear-gradient(90deg, transparent, rgba(248,113,113,0.65), rgba(239,68,68,0.40), transparent);
}
@keyframes failGlow {
  0%,100% { box-shadow: 0 8px 40px rgba(0,0,0,0.40), inset 0 1px 0 rgba(255,255,255,0.05); }
  50%     { box-shadow: 0 8px 40px rgba(0,0,0,0.40), 0 0 48px rgba(248,113,113,0.18), inset 0 1px 0 rgba(255,255,255,0.05); }
}
.safety-banner-left { display: flex; flex-direction: column; gap: 6px; }
.safety-banner-label {
  font-size: 9px; letter-spacing: 0.30em; text-transform: uppercase;
  color: rgba(122,152,200,0.50);
  font-family: 'JetBrains Mono', monospace; font-weight: 400;
}
.safety-banner-sf {
  font-size: 88px; font-weight: 700; font-family: 'Rajdhani', sans-serif;
  line-height: 1; letter-spacing: 0.02em;
}
.safety-banner-sf-safe  { color: #34d399; text-shadow: 0 0 52px rgba(52,211,153,0.50), 0 0 18px rgba(52,211,153,0.30); }
.safety-banner-sf-warn  { color: #fbbf24; text-shadow: 0 0 52px rgba(251,191,36,0.50), 0 0 18px rgba(251,191,36,0.30); }
.safety-banner-sf-fail  { color: #f87171; text-shadow: 0 0 52px rgba(248,113,113,0.60), 0 0 18px rgba(248,113,113,0.40); }
.safety-banner-sub {
  font-size: 12px; color: rgba(122,152,200,0.60);
  font-family: 'JetBrains Mono', monospace; letter-spacing: 0.08em;
}
.safety-banner-right { display: flex; flex-direction: column; align-items: flex-end; gap: 10px; }
.safety-banner-badge {
  display: inline-flex; align-items: center; gap: 10px;
  border-radius: 14px; padding: 16px 40px;
  font-size: 18px; font-weight: 700;
  font-family: 'Rajdhani', sans-serif; letter-spacing: 0.18em; text-transform: uppercase;
}
.safety-banner-badge-safe {
  background: linear-gradient(90deg, rgba(52,211,153,0.18), rgba(56,189,248,0.12));
  color: #34d399;
  border: 2px solid rgba(52,211,153,0.60);
  box-shadow: 0 0 28px rgba(52,211,153,0.20), inset 0 1px 0 rgba(255,255,255,0.05);
}
.safety-banner-badge-warn {
  background: linear-gradient(90deg, rgba(251,191,36,0.18), rgba(245,158,11,0.12));
  color: #fbbf24;
  border: 2px solid rgba(251,191,36,0.60);
  box-shadow: 0 0 28px rgba(251,191,36,0.20), inset 0 1px 0 rgba(255,255,255,0.05);
}
.safety-banner-badge-fail {
  background: linear-gradient(90deg, rgba(248,113,113,0.22), rgba(239,68,68,0.15));
  color: #f87171;
  border: 2px solid rgba(248,113,113,0.65);
  box-shadow: 0 0 36px rgba(248,113,113,0.30), inset 0 1px 0 rgba(255,255,255,0.05);
}
.safety-banner-detail {
  font-size: 10px; color: rgba(122,152,200,0.50);
  font-family: 'JetBrains Mono', monospace; letter-spacing: 0.10em; text-align: right;
}

/* ── Check-row chips ── */
.check-row { display: flex; gap: 10px; margin: 16px 0 10px 0; flex-wrap: wrap; }
.check-chip {
  background: linear-gradient(145deg, rgba(14,20,44,0.88), rgba(10,15,34,0.92));
  border: 1px solid rgba(99,102,241,0.12);
  border-left: 3px solid rgba(99,102,241,0.45);
  border-radius: 8px;
  padding: 12px 16px; flex: 1; min-width: 160px;
  transition: border-color 0.3s, box-shadow 0.3s;
  box-shadow: 0 3px 14px rgba(0,0,0,0.25);
}
.check-chip:hover {
  border-left-color: rgba(56,189,248,0.75);
  box-shadow: 0 6px 22px rgba(0,0,0,0.35), 0 0 14px rgba(56,189,248,0.06);
}
.check-chip-label {
  font-size: 8px; letter-spacing: 0.22em; text-transform: uppercase;
  color: rgba(122,152,200,0.50);
  font-family: 'JetBrains Mono', monospace; margin-bottom: 5px;
}
.check-chip-val {
  font-size: 20px; font-weight: 600; font-family: 'Rajdhani', sans-serif;
  background: linear-gradient(135deg, #e2f0ff, #a5c8f0);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}
.check-chip-sub {
  font-size: 8px; color: rgba(110,138,180,0.48);
  font-family: 'JetBrains Mono', monospace; margin-top: 3px;
}

/* ── Badges ── */
.lf-badge-char {
  display:inline-flex; align-items:center; gap:5px;
  background: linear-gradient(90deg, rgba(52,211,153,0.10), rgba(56,189,248,0.08));
  color: #34d399;
  border: 1px solid rgba(52,211,153,0.32); border-radius: 6px;
  padding: 5px 14px; font-size: 9px; font-weight: 600;
  font-family: 'JetBrains Mono', monospace; letter-spacing: 0.14em; text-transform: uppercase;
}
.lf-badge-design {
  display:inline-flex; align-items:center; gap:5px;
  background: linear-gradient(90deg, rgba(251,191,36,0.10), rgba(245,158,11,0.07));
  color: #fbbf24;
  border: 1px solid rgba(251,191,36,0.35); border-radius: 6px;
  padding: 5px 14px; font-size: 9px; font-weight: 600;
  font-family: 'JetBrains Mono', monospace; letter-spacing: 0.14em; text-transform: uppercase;
}
.safe-badge {
  display:inline-flex; align-items:center; gap:5px;
  background: linear-gradient(90deg, rgba(52,211,153,0.10), rgba(16,185,129,0.07));
  color: #34d399;
  border: 1px solid rgba(52,211,153,0.35); border-radius: 5px; padding: 5px 14px;
  font-size: 9.5px; font-weight: 600; font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.14em; text-transform: uppercase;
}
.warn-badge {
  display:inline-flex; align-items:center; gap:5px;
  background: linear-gradient(90deg, rgba(251,191,36,0.10), rgba(245,158,11,0.07));
  color: #fbbf24;
  border: 1px solid rgba(251,191,36,0.35); border-radius: 5px; padding: 5px 14px;
  font-size: 9.5px; font-weight: 600; font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.14em; text-transform: uppercase;
}
.fail-badge {
  display:inline-flex; align-items:center; gap:5px;
  background: linear-gradient(90deg, rgba(248,113,113,0.12), rgba(239,68,68,0.08));
  color: #f87171;
  border: 1px solid rgba(248,113,113,0.38); border-radius: 5px; padding: 5px 14px;
  font-size: 9.5px; font-weight: 600; font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.14em; text-transform: uppercase;
  animation: failPulse 2.4s ease infinite;
}
@keyframes failPulse {
  0%,100% { box-shadow: 0 0 0 rgba(248,113,113,0); }
  50%     { box-shadow: 0 0 18px rgba(248,113,113,0.22); }
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: transparent;
  border-bottom: 1px solid rgba(99,102,241,0.14);
  border-radius: 0; padding: 0; gap: 0;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 0 !important;
  color: rgba(122,152,200,0.45) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 10px !important; font-weight: 400 !important;
  padding: 11px 22px !important;
  letter-spacing: 0.14em !important; text-transform: uppercase !important;
  transition: all 0.22s !important;
  border-bottom: 2px solid transparent !important;
  background: transparent !important;
}
.stTabs [data-baseweb="tab"]:hover {
  color: rgba(200,220,255,0.80) !important;
  background: linear-gradient(180deg, rgba(99,102,241,0.06), transparent) !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(180deg, rgba(56,189,248,0.07), transparent) !important;
  color: #e2f0ff !important;
  border-bottom: 2px solid rgba(56,189,248,0.80) !important;
  font-weight: 500 !important;
}

/* ── Expanders ── */
div[data-testid="stExpander"] {
  background: linear-gradient(145deg, rgba(12,18,40,0.92), rgba(10,15,34,0.88)) !important;
  backdrop-filter: blur(10px) !important;
  border: 1px solid rgba(99,102,241,0.10) !important;
  border-left: 3px solid rgba(99,102,241,0.35) !important;
  border-radius: 8px !important;
  transition: border-left-color 0.28s, box-shadow 0.28s !important;
  box-shadow: 0 3px 16px rgba(0,0,0,0.22) !important;
}
div[data-testid="stExpander"]:hover {
  border-left-color: rgba(56,189,248,0.68) !important;
  box-shadow: 0 6px 24px rgba(0,0,0,0.32),
              0 0 16px rgba(56,189,248,0.05) !important;
}
div[data-testid="stExpander"] summary {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 10px !important; letter-spacing: 0.15em !important;
  color: rgba(122,152,200,0.62) !important;
  text-transform: uppercase !important; font-weight: 400 !important;
}

/* ── Sliders ── */
.stSlider [data-baseweb="slider"] [role="slider"] {
  background: linear-gradient(135deg, #38bdf8, #818cf8) !important;
  box-shadow: 0 0 10px rgba(56,189,248,0.50) !important;
  border: 2px solid rgba(56,189,248,0.60) !important;
  width: 14px !important; height: 14px !important;
  transition: box-shadow 0.2s !important;
}
.stSlider [data-baseweb="slider"] [data-testid="stSliderTrackFill"] {
  background: linear-gradient(90deg, #6366f1, #38bdf8) !important;
}

/* ── Select / Input ── */
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
  background: rgba(10,15,34,0.85) !important;
  backdrop-filter: blur(8px) !important;
  border: 1px solid rgba(99,102,241,0.14) !important;
  border-radius: 7px !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
div[data-baseweb="select"] > div:hover,
div[data-baseweb="input"] > div:focus-within {
  border-color: rgba(56,189,248,0.42) !important;
  box-shadow: 0 0 0 3px rgba(56,189,248,0.07) !important;
}
div[data-baseweb="select"] * {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 13px !important; color: #7a98c8 !important;
}

/* ── Download button ── */
.stDownloadButton > button {
  background: linear-gradient(135deg, rgba(52,211,153,0.10), rgba(56,189,248,0.08)) !important;
  color: #34d399 !important;
  border: 1px solid rgba(52,211,153,0.30) !important;
  border-radius: 7px !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 10px !important; font-weight: 500 !important;
  letter-spacing: 0.16em !important; text-transform: uppercase !important;
  padding: 12px 28px !important;
  transition: all 0.25s ease !important;
}
.stDownloadButton > button:hover {
  background: linear-gradient(135deg, rgba(52,211,153,0.16), rgba(56,189,248,0.14)) !important;
  border-color: rgba(52,211,153,0.55) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 28px rgba(0,0,0,0.38),
              0 0 18px rgba(52,211,153,0.12) !important;
}

/* ── Alerts ── */
div[data-testid="stAlert"] {
  border-radius: 7px !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 11px !important;
}
div[data-testid="stInfo"] {
  background: linear-gradient(135deg, rgba(99,102,241,0.07), rgba(56,189,248,0.05)) !important;
  border: 1px solid rgba(99,102,241,0.16) !important;
  border-left: 3px solid rgba(56,189,248,0.50) !important;
  border-radius: 7px !important;
}

/* ── Data tables ── */
.stDataFrame {
  border-radius: 8px !important;
  border: 1px solid rgba(99,102,241,0.10) !important;
  overflow: hidden !important;
}
.stDataFrame th {
  background: linear-gradient(90deg, rgba(99,102,241,0.10), rgba(56,189,248,0.07)) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 9px !important; letter-spacing: 0.16em !important;
  text-transform: uppercase !important;
  color: rgba(122,152,200,0.58) !important; font-weight: 400 !important;
}
.stDataFrame td {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 12.5px !important; color: #7a98c8 !important;
}

/* ── Sidebar section labels ── */
.sidebar-section {
  font-size: 8.5px; letter-spacing: 0.26em; text-transform: uppercase;
  background: linear-gradient(90deg, #6366f1, #38bdf8);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  font-family: 'JetBrains Mono', monospace; font-weight: 500;
  padding: 4px 0 3px 10px;
  border-left: 3px solid transparent;
  border-image: linear-gradient(180deg, #6366f1, #38bdf8) 1;
  margin-bottom: 10px;
  opacity: 0.85;
}

/* ── Typography ── */
h1, h2, h3, h4 {
  font-family: 'Cormorant Garamond', serif !important;
  background: linear-gradient(135deg, #e2f0ff 30%, #a5c8f0 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 400 !important; letter-spacing: -0.01em !important;
}
p, label { color: rgba(122,152,200,0.72) !important; }
hr { border-color: rgba(99,102,241,0.10) !important; }
.stSelectbox label, .stSlider label,
.stNumberInput label, .stTextInput label, .stRadio label {
  color: rgba(122,152,200,0.52) !important;
  font-size: 9px !important; letter-spacing: 0.20em !important;
  text-transform: uppercase !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-weight: 400 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: #060c1a; }
::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #6366f1, #38bdf8);
  border-radius: 2px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(56,189,248,0.60); }

.sr-init {
  opacity: 0;
  transform: translateY(42px);
  transition:
    opacity  0.72s cubic-bezier(0.22, 1, 0.36, 1),
    transform 0.72s cubic-bezier(0.22, 1, 0.36, 1);
  will-change: opacity, transform;
}
.sr-visible {
  opacity: 1 !important;
  transform: translateY(0) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<script>
(function () {
  'use strict';
  var TARGETS = [
    '.metric-card', '.safety-banner',
    '.check-chip',
    'div[data-testid="stExpander"]',
    '.stAlert',
    'div[data-testid="stDataFrame"]',
    'div[data-testid="stImage"]',
  ].join(',');
  var STAGGER_MS = 65;
  var THRESHOLD  = 0.08;
  var ROOT_MARGIN = '0px 0px -24px 0px';
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      var delay = (el._srDelay || 0);
      setTimeout(function () {
        el.classList.remove('sr-init');
        el.classList.add('sr-visible');
      }, delay);
      io.unobserve(el);
    });
  }, { threshold: THRESHOLD, rootMargin: ROOT_MARGIN });
  var _batchCounter = 0;
  function attach() {
    var all = document.querySelectorAll(TARGETS);
    var batchIdx = 0;
    all.forEach(function (el) {
      if (el._srDone) return;
      el._srDone = true;
      var now = Date.now();
      if (now - (_batchCounter._ts || 0) > 350) batchIdx = 0;
      _batchCounter._ts = now;
      el._srDelay = batchIdx * STAGGER_MS;
      batchIdx++;
      el.classList.add('sr-init');
      io.observe(el);
    });
  }
  var mo = new MutationObserver(function () { attach(); });
  mo.observe(document.body, { childList: true, subtree: true });
  setTimeout(attach, 250);
  setTimeout(attach, 800);
  setTimeout(attach, 1800);
})();
</script>
""", unsafe_allow_html=True)

# ─── Plot colour palette ───────────────────────────────────────────────────────
STRESS_CMAP = LinearSegmentedColormap.from_list(
    "aurora",
    ["#060c1a", "#0d1f4a", "#1e4a8a", "#3b82f6", "#38bdf8", "#a5f3fc"], N=256
)
BG   = "#060c1a"
SURF = "#0c1228"
BORD = "#141e3c"
TEXT = "#e2f0ff"
MUTE = "#3d5278"
ACC  = "#38bdf8"
GRN  = "#34d399"
RED  = "#f87171"
YEL  = "#fbbf24"
PURP = "#a78bfa"
IND  = "#818cf8"

# ─── Section Properties Database ──────────────────────────────────────────────
SECTION_PROPS = {
    "Rectangle 100×200mm": {
        "A_cm2": 200.0, "I_cm4": 6666.7,
        "Z_cm3": 666.7,   "Zp_cm3": 1000.0,
        "r_cm": 5.77,
        "y_top_mm": 100.0, "y_bot_mm": 100.0,
        "A_web_mm2": 0.9 * 100.0 * 200.0,
        "shape": "rect",
        "dims": {"b": 100, "h": 200},
        "desc": "b=100mm, h=200mm",
    },
    "I-Section (IPE 200)": {
        "A_cm2": 28.5, "I_cm4": 1943.0,
        "Z_cm3": 194.0,  "Zp_cm3": 220.0,
        "r_cm": 8.26,
        "y_top_mm": 100.0, "y_bot_mm": 100.0,
        "A_web_mm2": 5.6 * (200 - 2 * 8.5),
        "shape": "ipe",
        "dims": {"h": 200, "b": 100, "tf": 8.5, "tw": 5.6},
        "desc": "h=200mm, b=100mm, tf=8.5mm, tw=5.6mm",
    },
    "I-Section (IPE 300)": {
        "A_cm2": 53.8, "I_cm4": 8356.0,
        "Z_cm3": 557.0,  "Zp_cm3": 628.0,
        "r_cm": 12.46,
        "y_top_mm": 150.0, "y_bot_mm": 150.0,
        "A_web_mm2": 7.1 * (300 - 2 * 10.7),
        "shape": "ipe",
        "dims": {"h": 300, "b": 150, "tf": 10.7, "tw": 7.1},
        "desc": "h=300mm, b=150mm, tf=10.7mm, tw=7.1mm",
    },
    "Circular 150mm dia": {
        "A_cm2": 176.7, "I_cm4": 2485.0,
        "Z_cm3": 331.0,  "Zp_cm3": 562.5,
        "r_cm": 3.75,
        "y_top_mm": 75.0, "y_bot_mm": 75.0,
        "A_web_mm2": 0.9 * 176.7 * 100,
        "shape": "circle",
        "dims": {"d": 150},
        "desc": "dia=150mm",
    },
    "T-Section 200×200mm": {
        "A_cm2": 76.0,
        "I_cm4": 2880.0,
        "Z_cm3": 202.0,
        "Zp_cm3": 363.8,
        "r_cm": 6.16,
        "y_top_mm": 57.4,
        "y_bot_mm": 142.6,
        "A_web_mm2": 20.0 * (200 - 20),
        "shape": "tee",
        "dims": {"h": 200, "b": 200, "tf": 20, "tw": 20},
        "desc": "h=200mm, b=200mm, tf=20mm, tw=20mm",
    },
}

FY_MAP = {
    "Structural Steel (Fe250)":     250,
    "High-Strength Steel (Fe415)":  415,
    "Aluminium Alloy":              270,
    "Timber (Grade M30)":            30,
    "Concrete M25 (compression)":    25,
}
E_DEFAULT_MAP = {
    "Structural Steel (Fe250)":     200,
    "High-Strength Steel (Fe415)":  200,
    "Aluminium Alloy":               70,
    "Timber (Grade M30)":            12,
    "Concrete M25 (compression)":    25,
}
RHO_MAP = {
    "Structural Steel (Fe250)":    7850,
    "High-Strength Steel (Fe415)": 7850,
    "Aluminium Alloy":             2700,
    "Timber (Grade M30)":           600,
    "Concrete M25 (compression)":  2400,
}

# ─── Solver ───────────────────────────────────────────────────────────────────
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
        Rb        = Ma / span if span > 0 else 0.0
        Ra        = total_point + udl_total - Rb
        Ma_moment = 0.0
    else:
        Ra        = total_point + udl_total
        Rb        = 0.0
        Ma_moment = -(sum(P * x for x, P in loads) + udl_total * udl_arm)

    n   = 400
    xs  = np.linspace(0, span, n)
    sfd_tol = max(1e-6 * abs(total_point + udl_total), 1e-9)
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
    abs_bmd     = np.abs(bmd)
    max_bmd_abs = float(np.max(abs_bmd)) if float(np.max(abs_bmd)) > 0 else 1.0
    bmd_norm    = abs_bmd / max_bmd_abs

    return {
        "Ra": Ra, "Rb": Rb, "Ma_moment": Ma_moment,
        "xs": xs, "sfd": sfd, "bmd": bmd, "bmd_norm": bmd_norm,
        "max_sfd": float(np.max(np.abs(sfd))),
        "max_bmd": float(np.max(np.abs(bmd))),
        "udl_start": udl_start, "udl_end": udl_end,
    }


def get_section_moduli(section):
    p     = SECTION_PROPS[section]
    Ze_top = (p["I_cm4"] * 10.0) / p["y_top_mm"] if p["y_top_mm"] > 0 else 1e9
    Ze_bot = (p["I_cm4"] * 10.0) / p["y_bot_mm"] if p["y_bot_mm"] > 0 else 1e9
    return Ze_top, Ze_bot


def safety_factor(max_M_kNm, section, material):
    Ze_top, Ze_bot = get_section_moduli(section)
    fy = FY_MAP.get(material, 250)
    M_Nmm = max_M_kNm * 1e6
    sigma_top = M_Nmm / (Ze_top * 1000.0) if Ze_top > 0 else 0.0
    sigma_bot = M_Nmm / (Ze_bot * 1000.0) if Ze_bot > 0 else 0.0
    sigma_gov = max(sigma_top, sigma_bot)
    sf = min(fy / sigma_gov, 999.0) if sigma_gov > 0 else 999.0
    return round(sf, 2), round(sigma_top, 1), round(sigma_bot, 1)


def moment_capacity_is800(section, material, gamma_m0=1.10):
    fy     = FY_MAP.get(material, 250)
    Zp_cm3 = SECTION_PROPS[section]["Zp_cm3"]
    return fy * (Zp_cm3 * 1000.0) / gamma_m0 / 1e6


def shear_capacity_is800(section, material, gamma_m0=1.10):
    A_web = SECTION_PROPS.get(section, SECTION_PROPS["Rectangle 100×200mm"]).get("A_web_mm2", 18000.0)
    fy    = FY_MAP.get(material, 250)
    return fy * A_web / (np.sqrt(3) * gamma_m0) / 1000.0


def natural_frequency(span, E_GPa, I_cm4, section, material, sup_type):
    E     = E_GPa * 1e9
    I     = I_cm4 * 1e-8
    rho   = RHO_MAP.get(material, 7850)
    A_m2  = SECTION_PROPS.get(section, {}).get("A_cm2", 20.0) * 1e-4
    m_bar = rho * A_m2
    if m_bar <= 0 or span <= 0:
        return 0.0
    EI = E * I
    coeff = (np.pi / (2.0 * span ** 2) if sup_type == "simply_supported"
             else 1.8751 ** 2 / (2.0 * np.pi * span ** 2))
    return round(coeff * np.sqrt(EI / m_bar), 3)


def compute_deflection_data(xs, bmd, span, E_GPa, I_cm4, support_type="simply_supported"):
    EI  = E_GPa * 1e9 * I_cm4 * 1e-8
    dx  = xs[1] - xs[0]
    M   = -bmd * 1e3
    curvature = M / EI
    slope = np.concatenate([[0.0],
                            np.cumsum(0.5 * (curvature[:-1] + curvature[1:]) * dx)])
    defl  = np.concatenate([[0.0],
                            np.cumsum(0.5 * (slope[:-1] + slope[1:]) * dx)])
    if support_type == "cantilever":
        defl = -defl
    else:
        chord = np.linspace(defl[0], defl[-1], len(xs))
        defl  = defl - chord
    defl_mm = defl * 1000.0
    idx_max = int(np.argmax(np.abs(defl_mm)))
    return defl_mm, float(defl_mm[idx_max])


# ─── Matplotlib style ─────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": SURF,
    "axes.edgecolor": BORD, "axes.labelcolor": MUTE,
    "xtick.color": MUTE, "ytick.color": MUTE,
    "grid.color": BORD, "text.color": TEXT,
    "font.family": "monospace", "font.size": 9,
})


# ─── Plots ────────────────────────────────────────────────────────────────────
def plot_beam(span, loads, support_a, support_b, res,
              udl=0, udl_start=0, udl_end=None, udl_arrows=8):
    if udl_end is None:
        udl_end = span
    xs = res["xs"]; bmd_norm = res["bmd_norm"]
    Ra, Rb = res["Ra"], res["Rb"]

    fig, ax = plt.subplots(figsize=(12, 4.0))
    fig.patch.set_facecolor(BG); ax.set_facecolor(SURF)
    beam_y = 0.0; beam_h = 0.22; beam_hi = beam_y + beam_h

    img = STRESS_CMAP(bmd_norm).reshape(1, len(bmd_norm), 4)
    ax.imshow(img, aspect='auto', extent=[xs[0], xs[-1], beam_y, beam_hi],
              origin='lower', zorder=1)
    for x0, x1, y0, y1 in [
        (0, span, beam_y, beam_y), (0, span, beam_hi, beam_hi),
        (0, 0, beam_y, beam_hi),   (span, span, beam_y, beam_hi)
    ]:
        ax.plot([x0, x1], [y0, y1], color=BORD, lw=1)

    if udl > 0 and udl_end > udl_start:
        sc = max((udl / 50.0) * 0.4, 0.12)
        ax.fill_between([udl_start, udl_end], beam_hi, beam_hi + sc * 0.7,
                        color=ACC, alpha=0.22, linewidth=0)
        ax.plot([udl_start, udl_end], [beam_hi + sc * 0.7] * 2,
                color=ACC, lw=1.2, linestyle="--")
        for wx in np.linspace(udl_start, udl_end, udl_arrows):
            ax.annotate("", xy=(wx, beam_hi), xytext=(wx, beam_hi + sc * 0.7),
                        arrowprops=dict(arrowstyle="-|>", color=ACC, lw=0.8))
        ax.text((udl_start + udl_end) / 2, beam_hi + sc * 0.7 + 0.05,
                f"w = {udl:.2f} kN/m", ha="center", fontsize=8,
                color=ACC, style="italic")

    for xi, Pi in loads:
        ax.plot([xi, xi], [beam_hi, beam_hi + 0.6], color=RED, lw=1.8, solid_capstyle='round')
        ax.annotate("", xy=(xi, beam_hi + 0.02), xytext=(xi, beam_hi + 0.6),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8, mutation_scale=14))
        ax.text(xi, beam_hi + 0.68, f"{Pi:.2f} kN",
                ha="center", fontsize=8.5, color=RED, fontweight="bold")

    def draw_support(xp, label, reaction, stype):
        if stype == "Pinned":
            tx = [xp-0.22, xp+0.22, xp, xp-0.22]
            ty = [beam_y-0.27, beam_y-0.27, beam_y, beam_y-0.27]
            ax.fill(tx, ty, color=IND, alpha=0.28)
            ax.plot(tx, ty, color=ACC, lw=1)
            for hx in np.linspace(xp-0.28, xp+0.28, 6):
                ax.plot([hx, hx-0.1], [beam_y-0.30, beam_y-0.40],
                        color=ACC, lw=0.8, alpha=0.55)
            ax.plot([xp-0.32, xp+0.32], [beam_y-0.30]*2, color=ACC, lw=1.2)
        elif stype == "Roller":
            tx = [xp-0.22, xp+0.22, xp, xp-0.22]
            ty = [beam_y-0.27, beam_y-0.27, beam_y, beam_y-0.27]
            ax.fill(tx, ty, color=GRN, alpha=0.20)
            ax.plot(tx, ty, color=GRN, lw=1)
            for cx in [xp-0.14, xp, xp+0.14]:
                ax.add_patch(MplCircle((cx, beam_y-0.33), 0.045,
                                       color=GRN, fill=False, lw=0.9))
            ax.plot([xp-0.32, xp+0.32], [beam_y-0.38]*2, color=GRN, lw=1.2)
        elif stype == "Fixed":
            ww, wh = 0.18, 0.55
            ax.fill([xp-ww, xp, xp, xp-ww],
                    [beam_y-wh, beam_y-wh, beam_hi, beam_hi], color=IND, alpha=0.18)
            ax.plot([xp, xp], [beam_y-wh, beam_hi], color=ACC, lw=2.5)
            for hy in np.linspace(beam_y-wh+0.06, beam_hi-0.06, 7):
                ax.plot([xp-ww, xp-ww+0.12], [hy, hy-0.10],
                        color=ACC, lw=0.8, alpha=0.55)
        elif stype == "Free":
            ax.plot([xp, xp], [beam_y-0.45, beam_hi],
                    color=MUTE, lw=1.0, linestyle="--", alpha=0.6)
        if stype != "Free":
            lc = GRN if stype == "Roller" else ACC
            if stype == "Fixed":
                sl = "hogging" if res["Ma_moment"] < 0 else "sagging"
                txt = f"{label}\nM={abs(res['Ma_moment']):.1f} kN·m\n({sl})"
            else:
                txt = f"{label}\n{reaction:.1f} kN"
            ax.text(xp, beam_y-0.52, txt, ha="center", fontsize=8,
                    color=lc, linespacing=1.4)

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

    idx_mm = int(np.argmax(np.abs(res["bmd"])))
    mv = res["bmd"][idx_mm]; mx = res["xs"][idx_mm]
    if abs(mv) > 0:
        ax.scatter([mx], [beam_hi+0.05], color=YEL, s=28, zorder=5)
        ax.text(mx, beam_hi+0.12, f"M={'+'if mv>=0 else ''}{mv:.1f} kN·m",
                ha="center", fontsize=7.5, color=YEL, fontweight="bold")

    ax.set_xlim(-0.5, span+0.5); ax.set_ylim(-0.75, 1.4)
    ax.set_xlabel("Position along beam (m)", fontsize=9, color=MUTE)
    ax.set_title("BEAM — Stress Distribution", fontsize=10, color=TEXT,
                 fontweight="bold", pad=8, loc="left")
    ax.set_yticks([])
    ax.grid(axis="x", alpha=0.15, lw=0.4, linestyle=":")
    for sp in ax.spines.values():
        sp.set_edgecolor(BORD)
    plt.tight_layout(pad=0.5)
    return fig


def _base_fig(h=3.2):
    fig, ax = plt.subplots(figsize=(12, h))
    fig.patch.set_facecolor(BG); ax.set_facecolor(SURF)
    for sp in ax.spines.values():
        sp.set_edgecolor(BORD)
    return fig, ax


def plot_sfd(xs, sfd, span):
    fig, ax = _base_fig()
    ax.fill_between(xs, 0, sfd, where=(sfd >= 0), color=ACC, alpha=0.38, linewidth=0)
    ax.fill_between(xs, 0, sfd, where=(sfd <  0), color=RED, alpha=0.38, linewidth=0)
    ax.plot(xs, sfd, color=ACC, lw=1.6)
    ax.axhline(0, color=BORD, lw=0.8)

    for idx in np.where(np.diff(np.sign(sfd)))[0]:
        x0, x1, v0, v1 = xs[idx], xs[idx+1], sfd[idx], sfd[idx+1]
        xz = x0 - v0*(x1-x0)/(v1-v0) if abs(v1-v0) > 1e-12 else (x0+x1)/2
        ax.axvline(xz, color=YEL, lw=1.0, linestyle=":", alpha=0.7)
        ax.scatter([xz], [0], color=YEL, s=30, zorder=5)
        vr = float(np.max(np.abs(sfd))) or 1.0
        ax.text(xz + span*0.01, vr*0.06, f"V=0\nx={xz:.2f}m",
                fontsize=7, color=YEL, va="bottom")

    ax.set_xlim(0, span)
    ax.set_xlabel("Position (m)", fontsize=9, color=MUTE)
    ax.set_ylabel("Shear (kN)", fontsize=9, color=MUTE)
    ax.set_title("SHEAR FORCE DIAGRAM", fontsize=10, color=TEXT,
                 fontweight="bold", pad=8, loc="left")
    ax.grid(alpha=0.15, lw=0.4, linestyle=":")
    im = int(np.argmax(np.abs(sfd)))
    ax.annotate(f"  {sfd[im]:.1f} kN", xy=(xs[im], sfd[im]), fontsize=8, color=YEL)
    plt.tight_layout(pad=0.5)
    return fig


def plot_bmd(xs, bmd, span):
    fig, ax = _base_fig()
    ax.fill_between(xs, 0, bmd, where=(bmd >= 0), color=GRN, alpha=0.38, linewidth=0)
    ax.fill_between(xs, 0, bmd, where=(bmd <  0), color=RED, alpha=0.38, linewidth=0)
    ax.plot(xs, bmd, color=GRN, lw=1.6)
    ax.axhline(0, color=BORD, lw=0.8)

    mr = float(np.max(np.abs(bmd))) or 1.0
    for idx in np.where(np.diff(np.sign(bmd)))[0]:
        x0, x1, m0, m1 = xs[idx], xs[idx+1], bmd[idx], bmd[idx+1]
        xi = x0 - m0*(x1-x0)/(m1-m0) if abs(m1-m0) > 1e-12 else (x0+x1)/2
        ax.scatter([xi], [0], color=RED, s=40, zorder=6, marker="D")
        ax.text(xi + span*0.01, mr*0.04, f"IP\n{xi:.2f}m",
                fontsize=7, color=RED, va="bottom")

    ax.set_xlim(0, span)
    ax.set_xlabel("Position (m)", fontsize=9, color=MUTE)
    ax.set_ylabel("Moment (kN·m)", fontsize=9, color=MUTE)
    ax.set_title("BENDING MOMENT DIAGRAM", fontsize=10, color=TEXT,
                 fontweight="bold", pad=8, loc="left")
    ax.grid(alpha=0.15, lw=0.4, linestyle=":")
    im = int(np.argmax(np.abs(bmd)))
    ax.annotate(f"  {bmd[im]:.1f} kN·m", xy=(xs[im], bmd[im]),
                fontsize=8, color=YEL)
    plt.tight_layout(pad=0.5)
    return fig


def plot_deflection(xs, defl_mm, span):
    fig, ax = _base_fig()
    ax.fill_between(xs, 0, defl_mm, color=PURP, alpha=0.35, linewidth=0)
    ax.plot(xs, defl_mm, color=PURP, lw=1.6)
    ax.axhline(0, color=BORD, lw=0.8, linestyle="--")
    ax.set_xlim(0, span)
    ax.set_xlabel("Position (m)", fontsize=9, color=MUTE)
    ax.set_ylabel("Deflection (mm)", fontsize=9, color=MUTE)
    ax.set_title("DEFLECTION CURVE (Euler–Bernoulli, constant EI)",
                 fontsize=10, color=TEXT, fontweight="bold", pad=8, loc="left")
    ax.grid(alpha=0.15, lw=0.4, linestyle=":")
    i = int(np.argmax(np.abs(defl_mm)))
    ax.annotate(f"  δ_max = {defl_mm[i]:.2f} mm", xy=(xs[i], defl_mm[i]),
                fontsize=8, color=YEL)
    plt.tight_layout(pad=0.5)
    return fig


def plot_position_query(xs, sfd, bmd, defl_mm, span, x_q):
    fig, axes = plt.subplots(3, 1, figsize=(12, 7.5), sharex=True)
    fig.patch.set_facecolor(BG)
    fig.subplots_adjust(hspace=0.06)
    v_q = float(np.interp(x_q, xs, sfd))
    m_q = float(np.interp(x_q, xs, bmd))
    d_q = float(np.interp(x_q, xs, defl_mm))
    for ax, (data, ylabel, color, title), val in zip(
        axes,
        [(sfd, "Shear Force (kN)", ACC, "SHEAR FORCE"),
         (bmd, "Moment (kN·m)",    GRN, "BENDING MOMENT"),
         (defl_mm, "Deflection (mm)", PURP, "DEFLECTION")],
        [v_q, m_q, d_q]
    ):
        ax.set_facecolor(SURF)
        ax.fill_between(xs, 0, data, color=color, alpha=0.25, linewidth=0)
        ax.plot(xs, data, color=color, lw=1.5)
        ax.axhline(0, color=BORD, lw=0.8, linestyle="--", alpha=0.6)
        ax.axvline(x_q, color=YEL, lw=1.2, linestyle="--", alpha=0.85, zorder=4)
        ax.scatter([x_q], [val], color=YEL, s=55, zorder=6)
        ax.text(x_q + span*0.02, val, f"  {val:.2f}", fontsize=8.5,
                color=YEL, va="center", fontweight="bold")
        ax.set_ylabel(ylabel, fontsize=8, color=MUTE)
        ax.set_title(title, fontsize=8.5, color=TEXT, fontweight="bold", loc="left", pad=4)
        ax.grid(alpha=0.12, lw=0.4, linestyle=":")
        ax.set_xlim(0, span)
        for sp in ax.spines.values():
            sp.set_edgecolor(BORD)
    axes[-1].set_xlabel("Position (m)", fontsize=9, color=MUTE)
    plt.tight_layout(pad=0.4)
    return fig, v_q, m_q, d_q


def plot_cross_section(section, M_kNm):
    p     = SECTION_PROPS.get(section, SECTION_PROPS["Rectangle 100×200mm"])
    shape = p["shape"]; dims = p["dims"]
    I_mm4 = p["I_cm4"] * 1e4
    y_top = p["y_top_mm"]; y_bot = p["y_bot_mm"]
    M_Nmm = M_kNm * 1e6

    sigma_top = -M_Nmm * y_top / I_mm4 if I_mm4 > 0 else 0.0
    sigma_bot =  M_Nmm * y_bot / I_mm4 if I_mm4 > 0 else 0.0

    top_label = "COMPRESSION" if sigma_top <= 0 else "TENSION"
    bot_label = "TENSION"     if sigma_bot >= 0 else "COMPRESSION"
    top_clr   = "#3b82f6"     if sigma_top <= 0 else RED
    bot_clr   = RED           if sigma_bot >= 0 else "#3b82f6"

    SCMAP = LinearSegmentedColormap.from_list(
        "stress_sec", ["#3b82f6", "#e2f0ff", "#f87171"], N=512
    )
    extremes = max(abs(sigma_top), abs(sigma_bot), 1e-9)

    fig, (ax_sec, ax_str) = plt.subplots(
        1, 2, figsize=(10, 5.5), gridspec_kw={"width_ratios": [1.6, 1]}
    )
    fig.patch.set_facecolor(BG)
    for ax in (ax_sec, ax_str):
        ax.set_facecolor(SURF)
        for sp in ax.spines.values():
            sp.set_edgecolor(BORD)

    def strip_color(y_na):
        s = -M_Nmm * y_na / I_mm4 if I_mm4 > 0 else 0.0
        return SCMAP(np.clip((s / extremes + 1) / 2, 0, 1))

    N = 60

    def fill_strips(xl, xr, yb, yt):
        ys = np.linspace(yb, yt, N + 1)
        for j in range(N):
            ym = (ys[j] + ys[j+1]) / 2
            ax_sec.add_patch(mpatches.Rectangle(
                (xl, ys[j]), xr-xl, ys[j+1]-ys[j],
                facecolor=strip_color(ym), edgecolor="none"
            ))
        ax_sec.plot([xl, xr, xr, xl, xl],
                    [yb, yb, yt, yt, yb], color=BORD, lw=1.0)

    if shape == "rect":
        b, h = dims["b"], dims["h"]
        fill_strips(-b/2, b/2, -y_bot, y_top)
        ax_sec.set_xlim(-b*0.85, b*0.85)
    elif shape == "ipe":
        b, tf, tw = dims["b"], dims["tf"], dims["tw"]
        fill_strips(-b/2,  b/2,  y_top-tf, y_top)
        fill_strips(-tw/2, tw/2, -y_bot+tf, y_top-tf)
        fill_strips(-b/2,  b/2,  -y_bot,  -y_bot+tf)
        ax_sec.set_xlim(-b*0.85, b*0.85)
    elif shape == "circle":
        r = dims["d"] / 2
        ys = np.linspace(-r, r, N+1)
        for j in range(N):
            ym = (ys[j]+ys[j+1])/2
            chord = np.sqrt(max(r**2-ym**2, 0))
            ax_sec.add_patch(mpatches.Rectangle(
                (-chord, ys[j]), 2*chord, ys[j+1]-ys[j],
                facecolor=strip_color(ym), edgecolor="none"
            ))
        th = np.linspace(0, 2*np.pi, 200)
        ax_sec.plot(r*np.cos(th), r*np.sin(th), color=BORD, lw=1.2)
        ax_sec.set_xlim(-r*1.6, r*1.6)
    elif shape == "tee":
        b, tf, tw = dims["b"], dims["tf"], dims["tw"]
        fill_strips(-b/2,  b/2,  y_top-tf, y_top)
        fill_strips(-tw/2, tw/2, -y_bot,   y_top-tf)
        ax_sec.set_xlim(-b*0.75, b*0.75)

    ax_sec.axhline(0, color=YEL, lw=1.0, linestyle="--", alpha=0.8)
    xlim = ax_sec.get_xlim()
    ax_sec.text(xlim[0]*0.80, y_top*0.08, "N.A.", fontsize=7.5, color=YEL)
    if y_top > 2:
        ax_sec.text(0, y_top*0.55, top_label, ha="center",
                    fontsize=7, color=top_clr, fontstyle="italic", alpha=0.85)
    if y_bot > 2:
        ax_sec.text(0, -y_bot*0.55, bot_label, ha="center",
                    fontsize=7, color=bot_clr, fontstyle="italic", alpha=0.85)

    ax_sec.set_xlabel("Width (mm)", fontsize=8, color=MUTE)
    ax_sec.set_ylabel("Height from N.A. (mm)", fontsize=8, color=MUTE)
    ax_sec.set_title(f"CROSS-SECTION  |  {section}", fontsize=9, color=TEXT,
                     fontweight="bold", pad=6, loc="left")
    ax_sec.set_aspect("equal", adjustable="datalim")
    ax_sec.grid(alpha=0.10, lw=0.4)

    sm = plt.cm.ScalarMappable(cmap=SCMAP, norm=plt.Normalize(-1, 1))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax_sec, orientation="vertical", pad=0.02, fraction=0.035)
    cbar.set_label("σ  comp → tens", color=MUTE, fontsize=7)
    cbar.set_ticks([-1, 0, 1]); cbar.set_ticklabels(["Comp.", "0", "Tens."])
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=MUTE, fontsize=7)

    total_h  = y_top + y_bot
    y_range  = np.linspace(-y_bot, y_top, 300)
    sarr     = -M_Nmm * y_range / I_mm4 if I_mm4 > 0 else np.zeros(300)
    ax_str.plot(sarr, y_range, color=ACC, lw=1.8)
    ax_str.fill_betweenx(y_range, 0, sarr, where=(sarr < 0),
                         color="#3b82f6", alpha=0.35, linewidth=0)
    ax_str.fill_betweenx(y_range, 0, sarr, where=(sarr >= 0),
                         color=RED, alpha=0.35, linewidth=0)
    ax_str.axhline(0, color=YEL, lw=1.0, linestyle="--", alpha=0.8)
    ax_str.axvline(0, color=BORD, lw=0.8)
    ax_str.scatter([sigma_top], [y_top],  color=top_clr, s=40, zorder=5)
    ax_str.scatter([sigma_bot], [-y_bot], color=bot_clr, s=40, zorder=5)

    t_pfx = "+" if sigma_top > 0 else ""
    b_pfx = "+" if sigma_bot > 0 else ""
    ax_str.text(sigma_top,  y_top  + total_h*0.04,
                f"{t_pfx}{sigma_top:.1f} MPa", fontsize=7.5, color=top_clr,
                ha="center", fontweight="bold")
    ax_str.text(sigma_bot, -y_bot  - total_h*0.06,
                f"{b_pfx}{sigma_bot:.1f} MPa", fontsize=7.5, color=bot_clr,
                ha="center", fontweight="bold")

    ax_str.set_xlabel("Bending Stress σ (MPa)", fontsize=8, color=MUTE)
    ax_str.set_ylabel("Height from N.A. (mm)", fontsize=8, color=MUTE)
    ax_str.set_title("STRESS PROFILE", fontsize=9, color=TEXT,
                     fontweight="bold", pad=6, loc="left")
    ax_str.grid(alpha=0.12, lw=0.4)
    plt.tight_layout(pad=0.6)
    return fig, sigma_top, sigma_bot


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:22px 0 6px 0;'>
      <div style='font-size:17px;font-weight:700;
        background:linear-gradient(90deg,#818cf8,#38bdf8);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-clip:text;letter-spacing:-0.2px;'>⚙️ Beam Setup</div>
      <div style='height:1px;
        background:linear-gradient(90deg,rgba(99,102,241,0.55),rgba(56,189,248,0.4),transparent);
        margin-top:10px;'></div>
    </div>""", unsafe_allow_html=True)

    span = st.slider("Beam Span (m)", 1.0, 20.0, 6.0, 0.5)
    support_a = st.selectbox("Support A (left end)", ["Pinned", "Fixed"], index=0)
    support_b = (
        st.selectbox("Support B (right end)", ["Roller"], index=0, key="sb_p")
        if support_a == "Pinned"
        else st.selectbox("Support B (right end)", ["Free"], index=0, key="sb_f")
    )

    st.markdown(
        "<div style='height:1px;background:linear-gradient(90deg,rgba(99,102,241,0.18),transparent);"
        "margin:14px 0 10px 0;'></div><div class='sidebar-section'>📐 Cross-Section</div>",
        unsafe_allow_html=True
    )
    section  = st.selectbox("Section Profile", list(SECTION_PROPS.keys()))
    material = st.selectbox("Material", list(FY_MAP.keys()))

    with st.expander("📊  Section Properties"):
        sp = SECTION_PROPS[section]
        Ze_top_d, Ze_bot_d = get_section_moduli(section)
        is_asym = abs(Ze_top_d - Ze_bot_d) > 0.5
        ze_note = (f"Ze_top={Ze_top_d:.1f} / Ze_bot={Ze_bot_d:.1f}"
                   if is_asym else f"{sp['Z_cm3']}")
        st.markdown(f"""
        <table style='width:100%;font-family:JetBrains Mono,monospace;font-size:10.5px;
                      color:#7a98c8;border-collapse:collapse;'>
          <tr><td style='padding:3px 6px;opacity:.55;'>A</td>
              <td style='padding:3px 0;text-align:right;color:#e2f0ff;'>{sp['A_cm2']} cm²</td></tr>
          <tr><td style='padding:3px 6px;opacity:.55;'>I</td>
              <td style='padding:3px 0;text-align:right;color:#e2f0ff;'>{sp['I_cm4']} cm⁴</td></tr>
          <tr><td style='padding:3px 6px;opacity:.55;'>Ze</td>
              <td style='padding:3px 0;text-align:right;color:#e2f0ff;'>{ze_note} cm³</td></tr>
          <tr><td style='padding:3px 6px;opacity:.55;'>Zp</td>
              <td style='padding:3px 0;text-align:right;color:#e2f0ff;'>{sp['Zp_cm3']} cm³</td></tr>
          <tr><td style='padding:3px 6px;opacity:.55;'>r</td>
              <td style='padding:3px 0;text-align:right;color:#e2f0ff;'>{sp['r_cm']} cm</td></tr>
          <tr><td style='padding:3px 6px;opacity:.55;'>y_top</td>
              <td style='padding:3px 0;text-align:right;color:#e2f0ff;'>{sp['y_top_mm']} mm</td></tr>
          <tr><td style='padding:3px 6px;opacity:.55;'>y_bot</td>
              <td style='padding:3px 0;text-align:right;color:#e2f0ff;'>{sp['y_bot_mm']} mm</td></tr>
          <tr><td style='padding:3px 6px;opacity:.5;font-size:9px;' colspan=2>{sp['desc']}</td></tr>
        </table>""", unsafe_allow_html=True)

    with st.expander("⚙️  Advanced Parameters"):
        E_GPa = st.number_input("E — Elastic Modulus (GPa)",
                                value=E_DEFAULT_MAP.get(material, 200),
                                min_value=1, max_value=400, key=f"E_{material}")
        I_cm4 = st.number_input("I — Moment of Inertia (cm⁴)",
                                value=int(SECTION_PROPS[section]["I_cm4"]),
                                min_value=10, max_value=500000, key=f"I_{section}")

    st.markdown(
        "<div style='height:1px;background:linear-gradient(90deg,rgba(99,102,241,0.18),transparent);"
        "margin:14px 0 10px 0;'></div><div class='sidebar-section'>⚖️ Load Factor γ_f</div>",
        unsafe_allow_html=True
    )
    gamma_f = st.radio(
        "Apply load factor", options=[1.0, 1.2, 1.5],
        format_func=lambda x: f"γ_f = {x}  {'(Characteristic)' if x==1.0 else '(Design)'}",
        index=0,
    )

    st.markdown(
        "<div style='height:1px;background:linear-gradient(90deg,rgba(99,102,241,0.18),transparent);"
        "margin:14px 0 10px 0;'></div><div class='sidebar-section'>🌊 Distributed Load (UDL)</div>",
        unsafe_allow_html=True
    )
    udl       = st.slider("UDL Intensity (kN/m)", 0.0, 50.0, 0.0, 1.0)
    udl_start = st.slider("UDL Start (m)", 0.0, span, 0.0, 0.5)
    udl_end   = st.slider("UDL End (m)",
                          udl_start if udl_start < span else max(0.0, span-0.5),
                          span, float(span), 0.5)
    udl_arrows = st.slider("Number of load arrows", 2, 20, 8, 1)

    st.markdown(
        "<div style='height:1px;background:linear-gradient(90deg,rgba(99,102,241,0.18),transparent);"
        "margin:14px 0 10px 0;'></div><div class='sidebar-section'>🎯 Point Loads</div>",
        unsafe_allow_html=True
    )
    n_loads = st.number_input("Number of point loads", 0, 6, 1)
    is_cant_sb = (support_a == "Fixed")
    if is_cant_sb and int(n_loads) > 0:
        st.markdown(
            "<div style='font-size:11px;color:#38bdf8;padding:2px 0 6px 0;"
            "font-family:JetBrains Mono,monospace;'>💡 Tip load defaults to free end.</div>",
            unsafe_allow_html=True
        )
    loads = []
    for i in range(int(n_loads)):
        c1, c2 = st.columns(2)
        with c1:
            dx = float(span) if is_cant_sb else round(span/(int(n_loads)+1)*(i+1), 1)
            xi = st.number_input(f"x{i+1} (m)", 0.0, float(span),
                                 min(dx, float(span)), step=0.1, key=f"x{i}")
        with c2:
            Pi = st.number_input(f"P{i+1} (kN)", 0.1, 500.0, 10.0, step=1.0, key=f"p{i}")
        loads.append((float(xi), float(Pi)))

    st.markdown("<div style='height:1px;background:linear-gradient(90deg,"
                "rgba(99,102,241,0.18),transparent);margin:14px 0 10px 0;'></div>",
                unsafe_allow_html=True)
    st.info("⚡ Results update live as you change inputs above.")


# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding:48px 0 22px 0; text-align:center;'>
  <div style='font-size:11px; letter-spacing:0.40em; text-transform:uppercase;
    background:linear-gradient(90deg,#818cf8,#38bdf8);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;
    font-family:JetBrains Mono,monospace; font-weight:400; margin-bottom:18px;
    opacity:0.75;'>Structural Engineering Suite</div>

  <div style='font-size:80px; font-weight:300; font-family:Cormorant Garamond,serif;
    background:linear-gradient(135deg,#e2f0ff 0%,#a5c8f0 50%,#818cf8 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;
    line-height:1; letter-spacing:-0.02em; margin-bottom:10px;'>Mech Vision</div>

  <div style='font-size:22px; font-weight:300; font-style:italic;
    font-family:Cormorant Garamond,serif;
    background:linear-gradient(90deg,rgba(56,189,248,0.70),rgba(129,140,248,0.65));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;
    letter-spacing:0.04em; margin-bottom:28px;'>Beam Load &amp; Stress Analyzer</div>

  <div style='display:flex; align-items:center; justify-content:center;
    gap:16px; margin-bottom:14px;'>
    <div style='height:1px; width:120px;
      background:linear-gradient(90deg,transparent,rgba(99,102,241,0.45));'></div>
    <div style='width:6px;height:6px;border-radius:50%;
      background:linear-gradient(135deg,#6366f1,#38bdf8);
      box-shadow:0 0 12px rgba(56,189,248,0.55);'></div>
    <div style='height:1px; width:120px;
      background:linear-gradient(90deg,rgba(56,189,248,0.45),transparent);'></div>
  </div>
</div>
<div style='height:1px;
  background:linear-gradient(90deg,transparent,rgba(99,102,241,0.35),rgba(56,189,248,0.30),transparent);
  margin-bottom:30px;'></div>
""", unsafe_allow_html=True)


# ─── Main analysis ────────────────────────────────────────────────────────────
sup_type = ("cantilever"
            if (support_a == "Fixed" and support_b == "Free")
            else "simply_supported")

factored_loads = tuple((x, P * gamma_f) for x, P in loads)
factored_udl   = udl * gamma_f

try:
    res = solve_beam(span, factored_loads, support_a, support_b,
                     factored_udl, udl_start, udl_end)

    sf, sigma_top, sigma_bot = safety_factor(res["max_bmd"], section, material)
    sigma = max(sigma_top, sigma_bot)

    total_load  = (sum(P for _, P in factored_loads)
                   + factored_udl * (res["udl_end"] - res["udl_start"]))
    reaction_sum = res["Ra"] + res["Rb"]
    if total_load > 0 and abs(reaction_sum - total_load) > max(0.01*total_load, 0.1):
        st.error(f"⚠️ Equilibrium error: Ra+Rb = {reaction_sum:.2f} kN "
                 f"but total load = {total_load:.2f} kN. Check inputs.")

    if gamma_f > 1.0:
        bc, _ = st.columns([1, 5])
        with bc:
            st.markdown(f"<span class='lf-badge-design'>DESIGN  γ_f = {gamma_f}</span>",
                        unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Metric cards (4 core + optional cantilever moment) ────────────────
    is_cantilever = (support_a == "Fixed" and support_b == "Free")
    n_cols = 5 if is_cantilever else 4
    cols = st.columns(n_cols)

    _mc = lambda l, v, u: f"""<div class='metric-card'>
        <div class='metric-label'>{l}</div>
        <div class='metric-value'>{v}</div>
        <div class='metric-unit'>{u}</div></div>"""

    with cols[0]: st.markdown(_mc("Reaction A",  f"{res['Ra']:.2f}", "kN"), unsafe_allow_html=True)
    with cols[1]: st.markdown(_mc("Reaction B",  f"{res['Rb']:.2f}", "kN"), unsafe_allow_html=True)
    with cols[2]: st.markdown(_mc("Max Shear",   f"{res['max_sfd']:.2f}", "kN"), unsafe_allow_html=True)
    with cols[3]: st.markdown(_mc("Max Moment",  f"{res['max_bmd']:.2f}", "kN·m"), unsafe_allow_html=True)

    if is_cantilever:
        with cols[4]:
            sl = "hogging" if res["Ma_moment"] < 0 else "sagging"
            st.markdown(_mc("Fixed-End Moment", f"{abs(res['Ma_moment']):.2f}",
                            f"kN·m ({sl})"), unsafe_allow_html=True)

    # ── Safety Factor — full-width highlighted banner (next line) ─────────
    gov_lbl = "Bottom" if sigma_bot >= sigma_top else "Top"
    gov_val = sigma

    if sf >= 2.5:
        banner_cls  = "safety-banner-safe"
        sf_cls      = "safety-banner-sf-safe"
        badge_cls   = "safety-banner-badge-safe"
        status_icon = "✓"
        status_txt  = "SAFE"
    elif sf >= 1.5:
        banner_cls  = "safety-banner-warn"
        sf_cls      = "safety-banner-sf-warn"
        badge_cls   = "safety-banner-badge-warn"
        status_icon = "⚠"
        status_txt  = "MARGINAL"
    else:
        banner_cls  = "safety-banner-fail"
        sf_cls      = "safety-banner-sf-fail"
        badge_cls   = "safety-banner-badge-fail"
        status_icon = "✗"
        status_txt  = "FAILURE"

    fy_val = FY_MAP.get(material, 250)
    st.markdown(f"""
    <div class='safety-banner {banner_cls}'>
      <div class='safety-banner-left'>
        <div class='safety-banner-label'>Safety Factor — Elastic (Governing Fibre)</div>
        <div class='safety-banner-sf {sf_cls}'>{sf}</div>
        <div class='safety-banner-sub'>
          σ_top = {sigma_top} MPa &nbsp;·&nbsp; σ_bot = {sigma_bot} MPa
          &nbsp;·&nbsp; Governing: {gov_lbl} fibre @ {gov_val} MPa
        </div>
      </div>
      <div class='safety-banner-right'>
        <div class='safety-banner-badge {badge_cls}'>{status_icon} &nbsp; {status_txt}</div>
        <div class='safety-banner-detail'>
          fy = {fy_val} MPa &nbsp;·&nbsp; {material}<br>
          Section: {section}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── IS 800 check chips ────────────────────────────────────────────────
    Md   = moment_capacity_is800(section, material)
    Vd   = shear_capacity_is800(section, material)
    mu_m = min(res["max_bmd"] / Md, 9.99) if Md > 0 else 0.0
    mu_v = min(res["max_sfd"] / Vd, 9.99) if Vd > 0 else 0.0
    f1   = natural_frequency(span, E_GPa, I_cm4, section, material, sup_type)

    defl_mm_arr, defl_max = compute_deflection_data(
        res["xs"], res["bmd"], span, E_GPa, I_cm4, sup_type
    )
    defl_limit = (span * 1000) / (180 if is_cantilever else 250)
    defl_ratio = abs(defl_max) / defl_limit if defl_limit > 0 else 0.0

    def mu_clr(mu):
        return GRN if mu < 0.75 else ("#fbbf24" if mu < 1.0 else RED)

    mc, vc, dc = mu_clr(mu_m), mu_clr(mu_v), mu_clr(defl_ratio)

    st.markdown(f"""
    <div class='check-row'>
      <div class='check-chip'>
        <div class='check-chip-label'>IS 800 · Moment Capacity (Zp)</div>
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
        <div class='check-chip-label'>Natural Frequency f₁ ↑</div>
        <div class='check-chip-val' style='color:{ACC};'>{f1} Hz</div>
        <div class='check-chip-sub'>Self-weight only · upper bound ·
          {'SS' if sup_type=='simply_supported' else 'Cantilever'}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📐  Model", "⚡  Shear Force", "🌀  Bending Moment",
        "📉  Deflection", "🔍  Query Point", "⬡  Cross-Section",
    ])

    with tab1:
        fig1 = plot_beam(span, factored_loads, support_a, support_b, res,
                         factored_udl, udl_start, udl_end, udl_arrows)
        st.pyplot(fig1, use_container_width=True); plt.close(fig1)

    with tab2:
        fig2 = plot_sfd(res["xs"], res["sfd"], span)
        st.pyplot(fig2, use_container_width=True); plt.close(fig2)

    with tab3:
        fig3 = plot_bmd(res["xs"], res["bmd"], span)
        st.pyplot(fig3, use_container_width=True); plt.close(fig3)

    with tab4:
        fig4 = plot_deflection(res["xs"], defl_mm_arr, span)
        st.pyplot(fig4, use_container_width=True); plt.close(fig4)
        dlim_max = (span * 1000) / 10
        lbl = "L/180 (cantilever)" if is_cantilever else "L/250"
        if abs(defl_max) > dlim_max:
            st.warning(f"⚠️ Deflection {abs(defl_max):.1f} mm exceeds L/10 "
                       f"= {dlim_max:.0f} mm — check E and I.")
        elif abs(defl_max) <= defl_limit:
            st.success(f"✅ Deflection OK — δ_max = {abs(defl_max):.2f} mm  ≤  "
                       f"{lbl} = {defl_limit:.1f} mm")
        else:
            st.error(f"❌ Deflection EXCEEDS limit — δ_max = {abs(defl_max):.2f} mm  >  "
                     f"{lbl} = {defl_limit:.1f} mm")

    with tab5:
        st.markdown("""<div style='font-family:JetBrains Mono,monospace;font-size:9.5px;
             letter-spacing:0.16em;text-transform:uppercase;
             color:rgba(99,102,241,0.55);margin-bottom:12px;'>
        Query internal forces &amp; deflection at any position</div>""",
                    unsafe_allow_html=True)
        x_q = st.slider("Query position x (m)", 0.0, float(span),
                         float(span)/2, 0.01, key="x_query_slider")
        fig_q, v_q, m_q, d_q = plot_position_query(
            res["xs"], res["sfd"], res["bmd"], defl_mm_arr, span, x_q
        )
        st.pyplot(fig_q, use_container_width=True); plt.close(fig_q)
        qc1, qc2, qc3 = st.columns(3)
        for col, lbl, val, unit in [
            (qc1, "Shear V(x)",      v_q, "kN"),
            (qc2, "Moment M(x)",     m_q, "kN·m"),
            (qc3, "Deflection δ(x)", d_q, "mm"),
        ]:
            with col:
                st.markdown(
                    f"<div class='metric-card' style='border-top-color:rgba(56,189,248,0.55);'>"
                    f"<div class='metric-label'>{lbl}</div>"
                    f"<div class='metric-value'>{val:.3f}</div>"
                    f"<div class='metric-unit'>{unit}</div></div>",
                    unsafe_allow_html=True
                )

    with tab6:
        st.markdown("""<div style='font-family:JetBrains Mono,monospace;font-size:9.5px;
             letter-spacing:0.16em;text-transform:uppercase;
             color:rgba(99,102,241,0.55);margin-bottom:12px;'>
        Bending stress distribution at any queried position</div>""",
                    unsafe_allow_html=True)
        x_cs = st.slider("Query position x (m)", 0.0, float(span),
                          float(span)/2, 0.01, key="x_cs_slider")
        M_at_x = float(np.interp(x_cs, res["xs"], res["bmd"]))
        idx_mm = int(np.argmax(np.abs(res["bmd"])))
        st.markdown(
            f"<div style='font-family:JetBrains Mono,monospace;font-size:9px;"
            f"color:rgba(99,102,241,0.50);margin-bottom:10px;letter-spacing:0.12em;'>"
            f"M at x = {x_cs:.2f} m → "
            f"<span style='color:#e2f0ff;font-weight:600;'>{M_at_x:.2f} kN·m</span>"
            f" &nbsp;|&nbsp; M_max = {res['max_bmd']:.2f} kN·m "
            f"at x = {res['xs'][idx_mm]:.2f} m</div>",
            unsafe_allow_html=True
        )

        fig_cs, s_top, s_bot = plot_cross_section(section, M_at_x)
        st.pyplot(fig_cs, use_container_width=True); plt.close(fig_cs)

        top_type = "compression" if s_top <= 0 else "tension"
        bot_type = "tension"     if s_bot >= 0 else "compression"
        top_clr  = "#3b82f6"     if s_top <= 0 else "#f87171"
        bot_clr  = "#f87171"     if s_bot >= 0 else "#3b82f6"
        tp = "+" if s_top > 0 else ""
        bp = "+" if s_bot > 0 else ""
        _p = SECTION_PROPS[section]
        st.markdown(
            f"<div style='font-family:JetBrains Mono,monospace;font-size:9px;"
            f"color:rgba(99,102,241,0.50);margin-top:8px;letter-spacing:0.12em;'>"
            f"σ_top = <span style='color:{top_clr};'>{tp}{s_top:.1f} MPa ({top_type})</span>"
            f" &nbsp;|&nbsp; "
            f"σ_bot = <span style='color:{bot_clr};'>{bp}{s_bot:.1f} MPa ({bot_type})</span>"
            f" &nbsp;|&nbsp; M(x) = {M_at_x:.2f} kN·m"
            f" &nbsp;|&nbsp; I = {_p['I_cm4']} cm⁴</div>",
            unsafe_allow_html=True
        )

    # ── Raw data table ────────────────────────────────────────────────────
    with st.expander("📋 View Raw Data Table (SFD, BMD & Deflection)"):
        step = 50
        st.dataframe(pd.DataFrame({
            "Position (m)":          np.round(res["xs"][::step], 3),
            "Shear Force (kN)":      np.round(res["sfd"][::step], 3),
            "Bending Moment (kN·m)": np.round(res["bmd"][::step], 3),
            "Deflection (mm)":       np.round(defl_mm_arr[::step], 3),
            "BMD Normalised [0–1]":  np.round(res["bmd_norm"][::step], 3),
        }), use_container_width=True, height=280)

    # ── Engineering summary ───────────────────────────────────────────────
    with st.expander("📝 Engineering Summary"):
        fy_val       = FY_MAP.get(material, 250)
        dl_lbl       = "L/180 (cantilever)" if is_cantilever else "L/250"
        govern_fibre = "Bottom" if sigma_bot >= sigma_top else "Top"
        summary_df = pd.DataFrame({
            "Parameter": [
                "Beam Span", "Support Configuration", "Load Factor γ_f",
                "Total Applied Load (factored)", "Support A (Reaction)", "Support B (Reaction)",
                "Max Shear Force", "Max Bending Moment",
                "σ_top — top fibre (magnitude)", "σ_bot — bottom fibre (magnitude)",
                "Governing fibre", "Material Yield Strength",
                "Safety Factor (elastic, gov. fibre)", "Safety Status",
                "IS 800 · Moment Utilisation (Zp)", "IS 800 · Moment Check",
                "IS 800 · Shear Utilisation",       "IS 800 · Shear Check",
                "Max Deflection", f"Deflection Limit ({dl_lbl})",
                "Deflection Check", "Natural Frequency f₁ (self-wt)",
                "Section Profile", "Material",
            ],
            "Value": [
                f"{span} m", f"{support_a} – {support_b}", str(gamma_f),
                f"{total_load:.2f} kN",
                f"{res['Ra']:.2f} kN", f"{res['Rb']:.2f} kN",
                f"{res['max_sfd']:.2f} kN", f"{res['max_bmd']:.2f} kN·m",
                f"{sigma_top} MPa", f"{sigma_bot} MPa",
                f"{govern_fibre}  —  {sigma} MPa", f"{fy_val} MPa",
                str(sf),
                "SAFE" if sf >= 2.5 else ("MARGINAL" if sf >= 1.5 else "FAILURE"),
                f"{mu_m*100:.1f}%", "PASS" if mu_m < 1.0 else "FAIL",
                f"{mu_v*100:.1f}%", "PASS" if mu_v < 1.0 else "FAIL",
                f"{abs(defl_max):.2f} mm", f"{defl_limit:.1f} mm",
                "PASS" if abs(defl_max) <= defl_limit else "FAIL",
                f"{f1} Hz", section, material,
            ]
        })
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        if "Concrete" in material:
            st.warning("Plain concrete cannot resist bending tension. "
                       "Safety factor is indicative only.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download Engineering Summary (CSV)",
            data=summary_df.to_csv(index=False).encode("utf-8"),
            file_name="mech_vision_summary.csv",
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
  border-top:1px solid rgba(99,102,241,0.10);'>
  <div style='display:flex; align-items:center; justify-content:center;
    gap:18px; margin-bottom:20px;'>
    <div style='height:1px; width:70px;
      background:linear-gradient(90deg,transparent,rgba(99,102,241,0.35));'></div>
    <span style='font-size:10px;
      background:linear-gradient(90deg,#6366f1,#38bdf8);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;
      background-clip:text;'>◆</span>
    <div style='height:1px; width:70px;
      background:linear-gradient(90deg,rgba(56,189,248,0.35),transparent);'></div>
  </div>
  <div style='display:inline-flex; align-items:center; gap:16px;
    font-family:Cormorant Garamond,serif; font-size:22px; font-weight:300;
    font-style:italic; letter-spacing:0.04em;
    background:linear-gradient(90deg,rgba(56,189,248,0.70),rgba(129,140,248,0.65));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;'>
    <span style='font-size:22px; font-style:normal;
      background:linear-gradient(135deg,#6366f1,#38bdf8);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;
      background-clip:text;'>✦</span>
    <span>Engineered by Yogesh S</span>
    <span style='font-size:22px; font-style:normal;
      background:linear-gradient(135deg,#38bdf8,#6366f1);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;
      background-clip:text;'>✦</span>
  </div>
</div>
""", unsafe_allow_html=True)
