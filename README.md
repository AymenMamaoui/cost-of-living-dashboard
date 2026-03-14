# 🌍 Global Cost of Living Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3D4E7A?logo=plotly&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-KMeans-F7931E?logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

An interactive data analysis dashboard that explores the **cost of living across cities and countries worldwide** — covering housing, food, transportation, and more. Built with Python, Streamlit, and Plotly, with KMeans clustering to group cities by cost profile.

---

## 📸 Dashboard Preview

> *Screenshots will be added after deployment.*

---

## 🎯 Project Objectives

- Analyze cost of living data across **hundreds of cities and countries**
- Visualize key expenses: **rent, food, transportation, utilities, and more**
- Build an **interactive dashboard** with dynamic filters (by country, city, region)
- Apply **KMeans clustering** to group cities by their overall cost profile
- Compute an **Affordability Index** per city based on salary vs. cost ratio

---

## 🗂️ Project Structure

```
cost-of-living-dashboard/
│
├── data/
│   ├── raw/                      # Original dataset (untouched)
│   └── processed/                # Cleaned & transformed data
│
├── notebooks/
│   └── 01_exploration.ipynb      # Exploratory Data Analysis (EDA)
│
├── src/                          # Core Python modules
│   ├── __init__.py
│   ├── data_loader.py            # Load dataset
│   ├── data_cleaning.py          # Clean & preprocess data
│   ├── analysis.py               # Affordability index & statistics
│   └── clustering.py             # KMeans clustering logic
│
├── app/                          # Streamlit frontend
│   ├── main.py                   # App entry point
│   └── pages/
│       ├── overview.py           # Global world view
│       ├── country_view.py       # Country & city deep dive
│       └── clustering_view.py    # KMeans clustering results
│
├── assets/                       # Static assets (images, icons)
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AymenMamaoui/cost-of-living-dashboard.git
cd cost-of-living-dashboard
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the dataset

Download the dataset from [Kaggle – Global Cost of Living](https://www.kaggle.com/datasets/mvieira101/global-cost-of-living) and place the CSV file in:

```
data/raw/cost_of_living.csv
```

### 5. Run the Streamlit app

```bash
streamlit run app/main.py
```

---

## 📊 Features

| Feature | Description |
|---|---|
| 🗺️ World Map | Interactive choropleth map of cost of living by country |
| 🏙️ City Explorer | Filter and compare cities by expense category |
| 📈 Expense Breakdown | Bar charts & treemaps for food, rent, transport, etc. |
| 🤖 KMeans Clustering | Cities grouped by cost profile (budget / mid-range / expensive) |
| 💡 Affordability Index | Computed score: average salary vs. total cost of living |

---

## 🧰 Tech Stack

| Tool | Usage |
|---|---|
| Python 3.10+ | Core language |
| Pandas | Data manipulation |
| Scikit-Learn | KMeans clustering |
| Plotly | Interactive charts & maps |
| Streamlit | Web dashboard interface |
| Jupyter | Exploratory data analysis |

---

## 📦 Dataset

- **Source:** [Kaggle – Global Cost of Living by mvieira101](https://www.kaggle.com/datasets/mvieira101/global-cost-of-living)
- **Coverage:** 500+ cities across 100+ countries
- **Features:** 50+ columns including rent, groceries, restaurants, transportation, salaries

---

## 📁 Key Python Modules

### `src/data_loader.py`
Loads the raw CSV dataset and returns a clean Pandas DataFrame.

### `src/data_cleaning.py`
Handles missing values, outliers, column renaming, and feature engineering.

### `src/analysis.py`
Computes the **Affordability Index** and key statistics per city/country.

### `src/clustering.py`
Applies **KMeans clustering** to segment cities into cost profiles and returns cluster labels.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Aymen MAMAOUI**
- GitHub: [@AymenMamaoui](https://github.com/AymenMamaoui)
- LinkedIn: [Aymen MAMAOUI](https://www.linkedin.com/in/aymen-mamaoui-527a343a8/)
