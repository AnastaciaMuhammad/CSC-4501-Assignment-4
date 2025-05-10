# SDN Controller – CSC 4501 Assignment 4

## Overview
This Python program simulates a simplified Software-Defined Networking (SDN) controller. It builds and manages a network topology, computes shortest paths, injects and prioritizes traffic, handles link failures, and visualizes active flows and utilization.

---

## Features

- Dynamic network topology with weighted links
- Shortest-path routing using Dijkstra’s algorithm
- Load-balancing across equal-cost paths
- Traffic prioritization: NORMAL and HIGH
- Backup path rerouting after simulated link failures
- Visualization of topology and flow paths
- CLI interface for testing and interaction
- SHA-256 watermark to verify code originality

---

## How to Run

### Requirements:
- Python 3.x
- `networkx`
- `matplotlib`

### Install:
```bash
pip install networkx matplotlib
