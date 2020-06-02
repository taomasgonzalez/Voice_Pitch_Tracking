# Voice_Pitch_Tracking

> **Automated pitch-tracking algorithms** for voice signals, with a focus on real-time implementation and comparative evaluation.

---

## Table of Contents

1. [Overview](#overview)
2. [Report](#report)
3. [Code](#code)
4. [Key Features](#key-features)
5. [Highlights](#highlights)


---
## Report

For a complete report of the findings, analysis, and results, see:
- [PitchTrackingVoice.pdf](./Report/PitchTrackingVoice.pdf)

---
## Code

All implementations and supporting scripts live in the [`Code/`](./Code/) directory.

---

## Overview

Voice_Pitch_Tracking contains several implementations of pitch-tracking algorithms for automatic annotation of voice signals. We compare and evaluate multiple methods, and in particular propose and validate a real-time-capable approach on our dataset.
The following (custom modified) algorithms were implemented:

- **Algorithms implemented:**
  - Short-time Auto-correlation (modified)
  - Harmonic Product Spectrum (modified)
  - YIN algorithm (modified)

- **Goal:**
  1. Implement and compare different pitch-tracking approaches.
  2. Develop a **real-time** implementation.
  3. Evaluate performance (accuracy, computational load) on the given voice database.

---

## Key Features

- **Multiple Algorithms**: Implementations of auto-correlation, HPS, and YIN with modifications for improved performance.
- **Real-Time-Capable**: A proposed pipeline that processes incoming audio frames in (near) real time.
- **Comparative Evaluation**: Comprehensive analysis and benchmarking in the report.

---

## Highlights

> **Real-Time Implementation**
> One of the main contributions is a method for real-time execution of the YIN pitch-tracking algorithm. This was implemented, tested on the provided voice database, and proved successful in achieving low-latency, accurate pitch estimates.

> **Comparative Analysis**
> In the report, you’ll find:
> - Quantitative metrics (e.g., accuracy vs. ground truth, computational cost)
> - Qualitative discussion of strengths/weaknesses of each algorithm
