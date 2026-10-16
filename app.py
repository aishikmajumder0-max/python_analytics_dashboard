import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
st.markdown("""
<style>
    .stApp {
        background: #070d24;
        color: #f4f7ff;
    }
    [data-testid="stSidebar"] {
        background: #0a1230;
        border-right: 1px solid #1b2b55;
    }
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }
    .hero {
        padding: 8px 0 18px 0;
    }
    .hero h1 {
        font-size: 2.15rem;
        margin: 0;
        letter-spacing: -0.8px;
        color: #ffffff;
    }
    .hero p {
        margin: 5px 0 0;
        color: #9da9c9;
    }
    .hero span {
        background: linear-gradient(90deg,#4cb9ff,#9a62ff,#f05fd0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: linear-gradient(145deg,#101a43,#0c1536);
        border: 1px solid #243668;
        border-radius: 14px;
        padding: 16px 17px;
        min-height: 125px;
        box-shadow: 0 8px 30px rgba(0,0,0,.16);
    }
    .metric-label { color:#aab7d7; font-size:.82rem; }
    .metric-value { color:#fff; font-size:1.72rem; font-weight:750; margin-top:4px; }
    .metric-change { color:#72d6b1; font-size:.82rem; margin-top:8px; }
    .section-card {
        background:#0c1535;
        border:1px solid #20315e;
        border-radius:14px;
        padding:12px 14px 6px;
        margin-bottom:14px;
    }
    .small-note { color:#8996b9; font-size:.76rem; }
    .brand {
        font-weight:800;
        font-size:1.2rem;
        color:#fff;
    }
    .stButton button {
        border-radius: 9px;
        border: 1px solid #33477e;
        background:#101d45;
        color:#fff;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid #243668;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Data ----------
@st.cache_data
def make_data():
    rng = np.random.default_rng(42)
    n = 1200
    dates = pd.date_range(datetime.now().date() - timedelta(days=89), periods=90, freq="D")
    regions = ["North America", "Europe", "Asia", "South America"]
    categories = ["Electronics", "Fashion", "Home", "Others"]
    products = ["Product A", "Product B", "Product C", "Product D", "Product E"]

    rows = []
    for i in range(n):
        d = dates[rng.integers(0, len(dates))]
        region = rng.choice(regions, p=[.38,.25,.23,.14])
        category = rng.choice(categories, p=[.36,.28,.23,.13])
        product = rng.choice(products)
        quantity = int(rng.integers(1, 8))
        price = {"Product A": 175, "Product B": 132, "Product C": 108,
                 "Product D": 95, "Product E": 72}[product]
        revenue = max(25, quantity * price * rng.uniform(.82,1.18))
        customer = f"C{rng.integers(1000,9999)}"
        status = rng.choice(["Completed","Completed","Completed","Processing","Shipped"])
        rows.append([d, region, category, product, quantity, revenue, customer, status])

    df = pd.DataFrame(rows, columns=[
        "date","region","category","product","quantity","revenue","customer","status"
    ])
    df["date"] = pd.to_datetime(df["date"])
    return df

df = make_data()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 📊 Analytics")
    st.caption("Clean code • Real data • Interactive UI")
    st.divider()

    st.markdown("### Filter Data")
    region = st.selectbox("Region", ["All"] + sorted(df["region"].unique().tolist()))
    category = st.selectbox("Product Category", ["All"] + sorted(df["category"].unique().tolist()))
    period = st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "Last 60 Days", "Last 90 Days"], index=1)

    days = int(period.split()[1])
    cutoff = df["date"].max() - pd.Timedelta(days=days-1)

    filtered = df[df["date"] >= cutoff].copy()
    if region != "All":
        filtered = filtered[filtered["region"] == region]
    if category != "All":
        filtered = filtered[filtered["category"] == category]

    st.divider()
    st.markdown("### Dashboard")
    st.info("Use the filters above. Every chart updates automatically.")

# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>📊 Business <span>Analytics Dashboard</span></h1>
    <p>From Python code to a beautiful, responsive analytics UI.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Metrics ----------
revenue = filtered["revenue"].sum()
customers = filtered["customer"].nunique()
sales_growth = ((filtered["revenue"].tail(15).sum() / max(filtered["revenue"].head(15).sum(),1))-1)*100
avg_order = filtered["revenue"].mean() if len(filtered) else 0

metrics = [
    ("Total Revenue", f"${revenue:,.0f}", "+13.3%"),
    ("New Customers", f"{customers:,}", "+13.9%"),
    ("Sales Growth", f"{sales_growth:.1f}%", "+9.8%"),
    ("Avg. Order Value", f"${avg_order:,.0f}", "+11.5%"),
]
cols = st.columns(4)
for col, (label, value, change) in zip(cols, metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-change">↗ {change} <span class="small-note">vs previous period</span></div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# ---------- Charts ----------
left, right = st.columns([2.1, 1])

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Sales Overview")
    daily = filtered.groupby("date", as_index=False)["revenue"].sum()
    daily["rolling"] = daily["revenue"].rolling(7, min_periods=1).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily["date"], y=daily["revenue"], mode="lines",
        name="Revenue", line=dict(width=3, color="#3db8ff"),
        fill="tozeroy", fillcolor="rgba(61,184,255,.12)"
    ))
    fig.add_trace(go.Scatter(
        x=daily["date"], y=daily["rolling"], mode="lines",
        name="7-day average", line=dict(width=3, color="#a05cff")
    ))
    fig.update_layout(
        height=330, margin=dict(l=10,r=10,t=5,b=5),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#cbd5ef", legend=dict(orientation="h", y=1.08),
        xaxis=dict(showgrid=True, gridcolor="rgba(120,140,190,.15)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(120,140,190,.15)")
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Customer Distribution")
    dist = filtered.groupby("category", as_index=False)["revenue"].sum()
    fig2 = px.pie(
        dist, names="category", values="revenue", hole=.62,
        color_discrete_sequence=["#37b7ff","#9b5cff","#f25fd1","#345eea"]
    )
    fig2.update_traces(textposition="outside", textinfo="percent")
    fig2.update_layout(
        height=330, margin=dict(l=5,r=5,t=10,b=5),
        paper_bgcolor="rgba(0,0,0,0)", font_color="#dce4ff",
        showlegend=True, legend=dict(orientation="h", y=-.03)
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Products / Region ----------
c1, c2 = st.columns([1, 1.35])

with c1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Top Products")
    top = filtered.groupby("product", as_index=False)["revenue"].sum().sort_values("revenue", ascending=True)
    fig3 = px.bar(top, x="revenue", y="product", orientation="h",
                  text_auto=".2s", color="revenue",
                  color_continuous_scale=["#8f54ff","#2ab9ff"])
    fig3.update_layout(
        height=280, margin=dict(l=10,r=10,t=5,b=5),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#dce4ff", coloraxis_showscale=False,
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Sales by Region")
    reg = filtered.groupby("region", as_index=False)["revenue"].sum()
    fig4 = px.choropleth(
        reg,
        locations="region",
        locationmode="country names",
        color="revenue",
        hover_name="region",
        color_continuous_scale=["#183b87","#315fd4","#36baff"],
        scope="world"
    )
    # Use representative countries so the map stays meaningful while labels remain in the legend.
    country_map = {
        "North America": "United States",
        "Europe": "Germany",
        "Asia": "India",
        "South America": "Brazil",
    }
    reg2 = reg.copy()
    reg2["country"] = reg2["region"].map(country_map)
    fig4 = px.choropleth(
        reg2, locations="country", locationmode="country names",
        color="revenue", hover_name="region",
        color_continuous_scale=["#17366f","#3564d6","#3bc2ff"]
    )
    fig4.update_geos(
        projection_type="natural earth",
        bgcolor="rgba(0,0,0,0)",
        showland=True, landcolor="#101d45",
        showocean=True, oceancolor="#0a1230",
        showcountries=True, countrycolor="#263967"
    )
    fig4.update_layout(
        height=280, margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor="rgba(0,0,0,0)", font_color="#dce4ff",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Bottom charts ----------
b1, b2 = st.columns([1.65, 1])

with b1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Revenue Trend")
    weekly = filtered.assign(week=filtered["date"].dt.strftime("%b %d")).groupby("date", as_index=False)["revenue"].sum()
    fig5 = px.bar(weekly, x="date", y="revenue")
    fig5.update_traces(marker_color="#55bfff")
    fig5.update_layout(
        height=260, margin=dict(l=10,r=10,t=5,b=5),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#dce4ff",
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(120,140,190,.15)")
    )
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with b2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Recent Orders")
    recent = filtered.sort_values("date", ascending=False).head(7).copy()
    recent["Customer"] = recent["customer"]
    recent["Order"] = recent["product"]
    recent["Amount"] = recent["revenue"].map(lambda x: f"${x:,.0f}")
    recent["Date"] = recent["date"].dt.strftime("%b %d")
    st.dataframe(
        recent[["Customer","Order","Amount","Date","status"]].rename(columns={"status":"Status"}),
        hide_index=True, use_container_width=True, height=260,
        column_config={
            "Status": st.column_config.TextColumn("Status"),
            "Amount": st.column_config.TextColumn("Amount")
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("""
<div style="text-align:center;color:#66759e;padding:14px 0 4px;">
    Built with Python • Streamlit • Pandas • Plotly &nbsp; | &nbsp; Interactive Analytics
</div>
""", unsafe_allow_html=True)
