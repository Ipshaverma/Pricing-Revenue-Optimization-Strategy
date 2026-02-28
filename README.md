# Pricing & Revenue Optimization Analytics Project 📊

This project focus on maximizing revenue and profit margins using data-driven pricing strategies. It combines advanced retail analytics, price elasticity modeling, and competitor benchmarking to provide actionable pricing recommendations.

## 🚀 Project Overview

The core objective is to analyze sales data to identify price sensitivity, segment products based on their contribution to revenue, and simulate the impact of price changes on total revenue.

### Key Features
*   **Price Elasticity Modeling**: Quantifying how changes in price affect demand using log-log regression concepts.
*   **SKU Segmentation (Pareto/ABC Analysis)**: Identifying "Category A" products that drive 80% of revenue.
*   **What-If Revenue Simulation**: Predicting revenue outcomes for various price change scenarios (e.g., -10% to +20%).
*   **Market Benchmarking**: Comparing internal pricing against competitor data to identify market positioning (Premium vs. Discounted).
*   **Inventory Risk Assessment**: Linking pricing strategy with stock levels to avoid stockouts on high-velocity items.

---

## 📂 Project Structure

```text
├── data/                       # Generated and processed datasets
│   ├── raw_sales_data.csv
│   ├── processed_sales_data.csv
│   ├── sku_segmentation.csv
│   ├── sku_elasticity.csv
│   ├── revenue_simulation.csv
│   ├── competitor_analysis.csv
│   └── inventory_sufficiency.csv
├── scripts/                    # Python analysis pipeline
│   ├── generate_data.py        # Synthesizes realistic retail datasets
│   ├── analyze_segments.py     # Performs Pareto/ABC segmentation
│   ├── analyze_elasticity.py   # Calculates price elasticity coefficients
│   └── analyze_market_inventory.py # Competitor and inventory risk analysis
├── PowerBI_Guide.md            # Instructions for dashboard building
└── README.md                   # Project documentation
```

---

## 🛠️ Getting Started

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Environment Setup
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pandas numpy matplotlib seaborn scipy statsmodels
```

### 3. Data Pipeline Execution
Run the scripts in the following order to generate the analysis:
1.  **Generate Data**: `python scripts/generate_data.py`
2.  **Segment SKUs**: `python scripts/analyze_segments.py`
3.  **Analyze Elasticity**: `python scripts/analyze_elasticity.py`
4.  **Market/Inventory Analysis**: `python scripts/analyze_market_inventory.py`

---

## 📈 Power BI Dashboard

The project includes a comprehensive guide to building a 4-page interactive dashboard in Power BI:
1.  **Executive Overview**: High-level revenue and Pareto trends.
2.  **Price Elasticity**: Scatter plots and heatmaps of price sensitivity.
3.  **What-If Simulator**: Interactive bridge charts for revenue prediction.
4.  **Market & Inventory**: Comparison against competitors and stock health.

Refer to [PowerBI_Guide.md](PowerBI_Guide.md) for detailed DAX measures and visualization setups.

---

## 🧪 Technologies Used
*   **Python**: Data processing and statistical modeling.
*   **Pandas/NumPy**: Data manipulation.
*   **Matplotlib/Seaborn**: Exploratory data visualization.
*   **Power BI**: Interactive business intelligence reporting.
