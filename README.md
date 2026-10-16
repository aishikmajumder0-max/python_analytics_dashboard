# Python Analytics Dashboard

A complete Streamlit + Pandas + Plotly analytics dashboard inspired by the supplied reference image.

## Features

- Dark professional analytics UI
- KPI cards
- Interactive region/category/time filters
- Revenue trend line chart
- Customer/category distribution donut chart
- Top products chart
- World sales map
- Revenue bar chart
- Recent orders table
- Responsive Streamlit layout
- Generated sample business data
- No external database required

## Project structure

```text
python_analytics_dashboard/
├── app.py
├── requirements.txt
├── README.md
├── run.bat
└── data/
    └── README.txt
```

## Windows setup

Open PowerShell or CMD inside this folder.

### 1. Create a virtual environment

```powershell
python -m venv venv
```

### 2. Activate it

PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

CMD:

```cmd
venv\Scripts\activate
```

### 3. Install packages

```powershell
pip install -r requirements.txt
```

### 4. Run

```powershell
streamlit run app.py
```

The browser normally opens at:

```text
http://localhost:8501
```

## One-click Windows run

Double-click `run.bat`.

## Notes

The dashboard currently creates realistic sample data inside `app.py`, so it works immediately without MySQL or another database.

To connect a real CSV/Excel/database later, replace the `make_data()` function with your data source while keeping the dashboard components unchanged.
