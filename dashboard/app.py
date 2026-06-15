
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Delhivery Network Intelligence", layout="wide")

# ── Load pre-computed artifacts ──────────────────────────────────────────────
@st.cache_data
def load_data():
    corridor_agg = pd.read_csv("dashboard/corridor_agg.csv")
    bottleneck_df = pd.read_csv("dashboard/bottleneck_df.csv")
    model_comparison = pd.read_csv("dashboard/model_comparison.csv")
    return corridor_agg, bottleneck_df, model_comparison

corridor_agg, bottleneck_df, model_comparison = load_data()

st.title("Delhivery Delivery Network Intelligence Dashboard")
st.caption("Graph-based ETA optimization, bottleneck detection & corridor delay audit")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Network Overview", "Bottleneck Hubs", "Corridor Delay Audit", "Model Performance"]
)

# ── TAB 1: Network Overview ──────────────────────────────────────────────────
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Corridors", f"{len(corridor_agg):,}")
    col2.metric("Total Facilities", f"{bottleneck_df['facility_code'].nunique():,}")
    col3.metric("High-Delay Corridors (>20%)", f"{(corridor_agg['is_high_delay_corridor']==1).sum():,}")
    col4.metric("Avg Median Delay Ratio", f"{corridor_agg['median_delay_ratio'].mean():.2f}")

    st.subheader("Route Type Mix")
    route_mix = corridor_agg['dominant_route_type'].value_counts().reset_index()
    route_mix.columns = ['route_type', 'count']
    fig = px.pie(route_mix, names='route_type', values='count', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# ── TAB 2: Bottleneck Hubs ────────────────────────────────────────────────────
with tab2:
    st.subheader("Top Bottleneck Hubs by Structural Risk Score")
    top_n = st.slider("Number of hubs to display", 5, 50, 20)
    top_hubs = bottleneck_df.sort_values('structural_risk_score', ascending=False).head(top_n)

    fig = px.bar(top_hubs, x='structural_risk_score', y='facility_name',
                  orientation='h', color='structural_risk_score',
                  color_continuous_scale='Reds',
                  title="Structural Risk Score")
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Bottleneck Quadrant: Importance vs Delay")
    fig2 = px.scatter(bottleneck_df, x='betweenness_centrality', y='avg_outbound_delay_ratio',
                       size='total_segment_volume', color='structural_risk_score',
                       hover_name='facility_name', color_continuous_scale='Viridis')
    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(top_hubs[['facility_name', 'structural_risk_score', 'betweenness_centrality',
                            'pagerank', 'avg_outbound_delay_ratio', 'sla_breach_contribution_pct']])

# ── TAB 3: Corridor Delay Audit ───────────────────────────────────────────────
with tab3:
    st.subheader("Corridor Delay Explorer")
    min_volume = st.slider("Minimum trip volume", 1, int(corridor_agg['trip_volume'].max()), 5)
    filtered = corridor_agg[corridor_agg['trip_volume'] >= min_volume]

    fig = px.scatter(filtered, x='avg_distance_km', y='median_delay_ratio',
                      size='trip_volume', color='dominant_route_type',
                      hover_name='corridor_label' if 'corridor_label' in filtered.columns else None,
                      title="Distance vs Median Delay Ratio")
    fig.add_hline(y=1.2, line_dash="dash", line_color="red", annotation_text="High-Delay Threshold")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Worst Corridors by Median Delay Ratio")
    worst = filtered.sort_values('median_delay_ratio', ascending=False).head(20)
    st.dataframe(worst[['corridor_label' if 'corridor_label' in worst.columns else 'source_center',
                          'median_delay_ratio', 'trip_volume', 'dominant_route_type']])

# ── TAB 4: Model Performance ──────────────────────────────────────────────────
with tab4:
    st.subheader("ETA Model Comparison: OSRM vs RF vs XGBoost vs Graph-Enhanced XGBoost")
    metric_choice = st.selectbox("Metric", ['MAE', 'RMSE', 'R2', 'pct_within_15pct'])
    fig = px.bar(model_comparison, x='model', y=metric_choice, color='model',
                  title=f"Model Comparison — {metric_choice}")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(model_comparison)

    st.info(
        "The Graph-Enhanced model adds Node2Vec embeddings of source/destination "
        "facilities to the baseline XGBoost feature set, capturing each facility's "
        "structural position in the corridor network."
    )
