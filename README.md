# Mech-vision

# 🏗️ Mech Vision — Beam Load & Stress Analyzer

> **Made by YOGESH S**  
> A software-based structural analysis tool built for the college symposium expo.

---

## 📌 What is Mech Vision?

**Mech Vision** is an interactive beam load and stress analyzer built entirely in Python using Streamlit. It simulates how a structural beam behaves under point loads and distributed loads — computing reactions, shear forces, bending moments, stress distribution, and deflection — all in real time with live diagrams.

This project combines **mechanical engineering principles** (statics, strength of materials) with **programming** to create a fully software-based educational tool — no hardware required.

---

## ✨ Features

- 🔧 **Two beam types** — Simply Supported (Pinned–Roller) and Cantilever (Fixed–Free)
- ⚡ **Live results** — all diagrams update instantly as you change inputs
- 📊 **4 diagrams** — Stress-coloured beam, Shear Force Diagram (SFD), Bending Moment Diagram (BMD), Deflection Curve
- 🎯 **5 cross-section profiles** — Rectangle, IPE 200, IPE 300, Circular, T-Section
- 🧪 **5 materials** — Structural Steel, High-Strength Steel, Aluminium, Timber, Concrete
- 🔢 **Up to 6 point loads** with custom positions and magnitudes
- 🌊 **Distributed load (UDL)** with adjustable intensity, range, and number of visual arrows
- ✅ **Safety factor badge** — SAFE / MARGINAL / FAILURE with colour coding
- 📐 **Deflection serviceability check** — L/250 for simply supported, L/180 for cantilever
- ⚠️ **Equilibrium verification** — solver checks Ra + Rb = total load at runtime
- 📋 **Raw data table** — full SFD & BMD values at every section point
- 📝 **Engineering summary** — complete results table with pass/fail status

---

## 🖥️ Tech Stack

| Layer | Tool |
|---|---|
| UI Framework | Streamlit |
| Math Engine | NumPy |
| Visualization | Matplotlib |
| Data Tables | Pandas |
| Language | Python 3.9+ |

---

## 🚀 How to Run

### Step 1 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2 — Launch the app

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
mech-vision/
│
├── app.py               ← main application (all logic + UI in one file)
├── requirements.txt     ← Python dependencies
└── README.md            ← this file
```

---

## 🧮 Engineering Behind the Tool

### Reactions
Solved using static equilibrium equations:
- **Simply Supported**: ΣM_A = 0 → R_B, then R_A = total load − R_B
- **Cantilever**: ΣF_y = 0 → R_A = total load; ΣM_A = 0 → fixed-end moment

### Shear Force & Bending Moment
Computed at 1000 evenly spaced sections along the beam using the left-of-cut free body diagram convention (strict `<` operator for load application).

### Bending Stress
```
σ = M / Z
```
Where Z is the section modulus (mm³) from standard tables.

### Safety Factor
```
SF = f_y / σ
```
Colour-coded: ✅ SAFE (SF ≥ 2.5) | ⚠️ MARGINAL (SF ≥ 1.5) | ❌ FAILURE (SF < 1.5)

### Deflection
Double numerical integration of the moment-curvature relation using the trapezoidal rule:
```
EI · d²y/dx² = M(x)
```
Boundary conditions applied per beam type.

---

## ⚠️ Limitations

- Handles **statically determinate beams only** (Pinned–Roller and Fixed–Free)
- Does not support Fixed–Fixed, Fixed–Pinned, or overhanging beams
- Plain concrete bending check is indicative only — not valid for unreinforced concrete design
- Deflection is an approximation (numerical integration, not closed-form)
- Not intended for real structural design — educational and demonstration use only

---

## 🎓 Academic Context

Built for the **college symposium expo** as a demonstration of combining:
- Mechanical design knowledge (statics, SOM, machine design)
- Software development (Python, Streamlit, NumPy, Matplotlib)

---

## 👤 Author

**YOGESH S**  
Mechanical Engineering Student  

---

*Mech Vision — where mechanics meets code.*
