import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import api_client
from utils.sidebar import render_account_sidebar
from utils.theme import inject_custom_css, page_header, COLORS
from utils.auth import require_login

inject_custom_css()

require_login()

# Dashboard access is only allowed after onboarding is completed.
# This protects the page even if a user opens the dashboard URL directly.
if not st.session_state.get("onboarding_completed", False):
    st.warning("🔒 Please complete your onboarding before accessing the dashboard.")
    st.info("Complete the required setup steps to unlock your organization dashboard.")
    if st.button("Complete Onboarding →", type="primary"):
        st.switch_page("portal/0_onboarding.py")
    st.stop()

render_account_sidebar()

page_header("📊", "Dashboard", f"Welcome back, {st.session_state.user.get('first_name', '')}")

# ---------------- summary fetch ----------------
try:
    summary = api_client.get_dashboard_summary()
except Exception as e:
    st.error(f"Dashboard data load nahi ho saka. ({e})")
    st.stop()

# ---------------- top metric cards ----------------
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Leads", summary.get("total_leads", 0))
c2.metric("Active Employees", summary.get("active_employees", 0))
c3.metric("Inactive Employees", summary.get("inactive_employees", 0))
c4.metric("Knowledge Sources", summary.get("total_knowledge_sources", 0))
c5.metric("Representatives", summary.get("total_representatives", 0))
st.caption(
    f"👥 {summary.get('active_representatives', 0)} active representative(s) "
    f"out of {summary.get('total_representatives', 0)}"
)

st.divider()

# ---------------- lead pipeline ----------------
st.subheader("Lead Pipeline")
p1, p2, p3, p4 = st.columns(4)
p1.metric("🆕 New", summary.get("new_leads", 0))
p2.metric("📞 Contacted", summary.get("contacted_leads", 0))
p3.metric("✅ Qualified", summary.get("qualified_leads", 0))
p4.metric("❌ Lost", summary.get("lost_leads", 0))

st.divider()

# ---------------- leads over time chart ----------------
st.subheader("Leads Over Time (Last 30 Days)")

try:
    lot = api_client.get_leads_over_time(days=30)
    df = pd.DataFrame(lot["points"])
    df["date"] = pd.to_datetime(df["date"])

    with st.container(border=True):
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df["count"],
                mode="lines+markers",
                line=dict(color=COLORS["primary"], width=3, shape="spline"),
                marker=dict(
                    size=9,
                    color=COLORS["accent"],
                    line=dict(width=2, color=COLORS["bg"]),
                ),
                fill="tozeroy",
                fillcolor="rgba(99, 102, 241, 0.18)",
                hovertemplate="%{x|%b %d}<br><b>%{y} leads</b><extra></extra>",
            )
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLORS["text"], size=13),
            margin=dict(l=10, r=10, t=10, b=10),
            height=380,
            hovermode="x unified",
            xaxis=dict(
                title="Date",
                showgrid=True,
                gridcolor="rgba(255,255,255,0.06)",
                zeroline=False,
            ),
            yaxis=dict(
                title="Leads Captured",
                showgrid=True,
                gridcolor="rgba(255,255,255,0.06)",
                zeroline=False,
            ),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
except Exception as e:
    st.error(f"Chart load nahi ho saka. ({e})")