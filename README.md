# CRC-Style Error Detection and Noisy Channel Simulation

**Course:** MAT-239 — Discrete Mathematics for Computing  
**Institution:** Southern New Hampshire University  
**Focus:** Error Detection, Noisy Channels, Probability Theory  

---

## Project Overview

This project investigates digital signal transmission over a noisy communication channel and evaluates the effectiveness of a **CRC-style checksum mechanism** for detecting data corruption. The work combines:

- **Large-scale Monte Carlo simulation** to empirically measure error-detection behavior under stochastic noise, and  
- **An interactive Python visualizer** to demonstrate transmission, noise injection, and receiver decision logic in real time.

Noise is modeled using independent Bernoulli trials, and checksum verification is used to accept or reject received messages. The project emphasizes probabilistic reasoning, system reliability, and the practical limitations of redundancy-based error detection schemes.

---

## Repository Contents

| Component | Language | Description |
|---------|----------|-------------|
| **Visualizer** | Python | A graphical “conveyor belt” simulation illustrating message transmission, bit-level noise, checksum verification, and ACK/NACK decisions in real time. |
| **Statistical Analysis** | Python / Spreadsheet | Empirical results derived from large-scale Monte Carlo simulations (up to 1,000,000 trials per noise level), summarized in tabular form. |
| **Presentation** | PDF | Slides describing the system model, probability analysis, and observed detection limits. |

---

## System Model

### Message Encoding
- **Data payload:** 8-bit message (0–255)
- **Checksum:** 3-bit redundancy computed as  
  \[
  \text{checksum} = (\text{base-10 value of data}) \bmod 7
  \]

This mechanism is **CRC-style in concept** (redundancy-based error detection) but does **not** implement polynomial CRC division.

### Noise Model
- Each transmitted bit (data and checksum) is flipped independently with probability \( p \in [0, 0.20] \).
- Noise is modeled using Bernoulli trials.

---

## Outcome Classification

Each transmission is evaluated using both ground truth (actual data integrity) and receiver decision (checksum verification):

- **GG (Good–Good):** Data intact and accepted.
- **GB (Good–Bad):** Data intact but falsely rejected.
- **BB (Bad–Bad):** Data corrupted and correctly rejected.
- **BG (Bad–Good):** Data corrupted but accepted (undetected error).

These categories are used consistently in both the visual simulation and the statistical analysis.

---

## Retransmission Logic

The receiver implements a simple **Automatic Repeat Request (ARQ)** strategy:

- `ACK = 0` → message accepted  
- `ACK = 1` → retransmission requested  

This allows observation of retransmission growth as channel noise increases.

---

## Performance Analysis Summary

As documented in the accompanying presentation and probability tables:

- **Detection effectiveness:** The modulo-7 checksum provides reliable detection at low to moderate noise levels.
- **Retransmission behavior:** Retransmission rates increase rapidly as noise approaches higher probabilities, illustrating diminishing network efficiency.
- **Theoretical limitation:** Collisions occur when distinct data values produce identical modulo-7 checksums, demonstrating inherent limits of simple checksum-based detection.

---

## Technologies Used

- **Python:** `pygame`, `random` (visual simulation)
- **Analysis Tools:** Spreadsheet-based aggregation of Monte Carlo results
- **Concepts:** Discrete probability, Bernoulli trials, binomial distributions, error detection theory

---

## How to Run the Visual Simulation

Ensure Python and `pygame` are installed:

```bash
pip install pygame
python src/crc_simulation.py
