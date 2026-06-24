# 🦅 Nigeria Insurgency Tracker

A data-driven intelligence platform engineered to track, map, and analyze conflict and insurgency across Nigeria. 

This project aims to provide real-time, actionable intelligence to aid in conflict resolution and restore regional stability. The system is built on a robust data pipeline capable of aggregating historical conflict datasets alongside live, scraped intelligence from regional networks.

## 🧠 Core Architecture

The platform relies on a dual-ingestion pipeline, ensuring both broad historical context and immediate situational awareness.

### 1. Data Ingestion Pipeline
* **Established Databases:** Automated ETL pipelines integrating with structured conflict databases (e.g., ACLED) to establish baseline historical trends and regional threat heatmaps.
* **Custom Intelligence Scrapers:** Purpose-built asynchronous scrapers designed to monitor local networks, news feeds, and regional sources for real-time incident reporting.

### 2. Processing & Analytics
* **ETL Framework:** Normalizes disparate data formats, resolves conflicting reports, and geocodes incident locations for spatial analysis.
* **Threat Modeling:** Analyzes incident frequency, perpetrator tactics, and regional vulnerabilities to generate actionable insights and predictive trend lines.

## ⚙️ Installation & Setup

1. **Clone the repository:**
```bash
   git clone [https://github.com/yourusername/Nigeria-Insurgency-Tracker.git](https://github.com/yourusername/Nigeria-Insurgency-Tracker.git)
   cd Nigeria-Insurgency-Tracker
