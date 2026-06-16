# app.py
# pip install streamlit pandas numpy plotly
# streamlit run app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date, datetime, timedelta

# =========================================================
# Page Config
# =========================================================
st.set_page_config(
    page_title="法特科技｜AI 採購預測與 Planning Demo",
    page_icon="📦",
    layout="wide",
)

# =========================================================
# Style
# =========================================================
st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(135deg, #f7fbff 0%, #f5fff8 45%, #fffaf3 100%);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f3d3e 0%, #155e63 100%);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .main-title {
        font-size: 34px;
        font-weight: 900;
        color: #0f3d3e;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }

    .sub-title {
        color: #557;
        font-size: 15px;
        margin-bottom: 24px;
    }

    .card {
        padding: 20px 22px;
        border-radius: 20px;
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(15,61,62,0.08);
        box-shadow: 0 10px 28px rgba(15,61,62,0.08);
        margin-bottom: 18px;
    }

    .metric-card {
        padding: 18px 20px;
        border-radius: 18px;
        background: white;
        border-left: 7px solid #2d9cdb;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    }

    .metric-label {
        font-size: 13px;
        color: #667;
        font-weight: 700;
    }

    .metric-value {
        font-size: 28px;
        color: #0f3d3e;
        font-weight: 900;
        margin-top: 6px;
    }

    .metric-note {
        font-size: 12px;
        color: #889;
        margin-top: 4px;
    }

    .pill {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 999px;
        background: #e8f7ff;
        color: #116b93;
        font-size: 12px;
        font-weight: 800;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    .pill-green {
        background: #e9f9ef;
        color: #1f7a3a;
    }

    .pill-orange {
        background: #fff1df;
        color: #a85d00;
    }

    .section-header {
        font-size: 22px;
        font-weight: 900;
        color: #0f3d3e;
        margin-top: 8px;
        margin-bottom: 10px;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(0,0,0,0.08);
        box-shadow: 0 8px 22px rgba(0,0,0,0.05);
    }

    .warning-box {
        background: #fff1df;
        color: #8a4b00;
        border-left: 6px solid #ff9800;
        padding: 14px 16px;
        border-radius: 14px;
        font-weight: 700;
        margin-bottom: 14px;
    }

    .success-box {
        background: #e9f9ef;
        color: #176c32;
        border-left: 6px solid #2eaf5d;
        padding: 14px 16px;
        border-radius: 14px;
        font-weight: 700;
        margin-bottom: 14px;
    }

    .info-box {
        background: #e8f7ff;
        color: #116b93;
        border-left: 6px solid #2d9cdb;
        padding: 14px 16px;
        border-radius: 14px;
        font-weight: 700;
        margin-bottom: 14px;
    }

    h1, h2, h3 {
        color: #0f3d3e;
    }
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# Demo Data
# =========================================================
np.random.seed(42)

TODAY = date(2026, 6, 16)

ITEMS = [
    {"料件名稱": "智慧控制板 A1", "料號": "71033"},
    {"料件名稱": "智慧控制板 A1-P2", "料號": "71033-P2"},
    {"料件名稱": "馬達模組 M8", "料號": "14802"},
    {"料件名稱": "感測器 S-Pro", "料號": "80122"},
    {"料件名稱": "電源轉換器 65W", "料號": "92015"},
    {"料件名稱": "金屬外殼 K2", "料號": "52201"},
    {"料件名稱": "連接線束 C7", "料號": "63591"},
    {"料件名稱": "風扇模組 F4", "料號": "74420"},
    {"料件名稱": "無線模組 W9", "料號": "88213"},
    {"料件名稱": "顯示面板 D5", "料號": "31504"},
    {"料件名稱": "散熱片 H3", "料號": "22018"},
    {"料件名稱": "電池模組 B6", "料號": "49027"},
    {"料件名稱": "包裝盒 P1", "料號": "PCK-001"},
    {"料件名稱": "螺絲組 SC-12", "料號": "SC-012"},
    {"料件名稱": "絕緣墊片 I8", "料號": "INS-008"},
    {"料件名稱": "主機板 MB-3", "料號": "MB-003"},
    {"料件名稱": "鏡頭模組 L2", "料號": "LEN-002"},
    {"料件名稱": "橡膠腳墊 R4", "料號": "RUB-004"},
    {"料件名稱": "天線組 ANT-7", "料號": "ANT-007"},
    {"料件名稱": "變壓器 T9", "料號": "TRN-009"},
]

CHANNELS = ["THD", "VC", "SC", "DF", "other"]


def month_options(start_month: date, months: int = 12):
    result = []
    y = start_month.year
    m = start_month.month
    for i in range(months):
        yy = y + (m + i - 1) // 12
        mm = (m + i - 1) % 12 + 1
        result.append(f"{yy}/{mm:02d}")
    return result


def month_start_end(month_text: str):
    y, m = map(int, month_text.split("/"))
    start = date(y, m, 1)
    if m == 12:
        end = date(y + 1, 1, 1) - timedelta(days=1)
    else:
        end = date(y, m + 1, 1) - timedelta(days=1)
    return start, end


def display_range_for_month(month_text: str):
    start, end = month_start_end(month_text)
    if start.year == TODAY.year and start.month == TODAY.month:
        start = TODAY
    return start, end


@st.cache_data
def create_forecast_data():
    rows = []
    options = month_options(date(2026, 6, 1), 12)

    for month_text in options:
        start, end = month_start_end(month_text)
        days_in_month = (end - start).days + 1

        for idx, item in enumerate(ITEMS):
            base = np.random.randint(120, 950)
            season_factor = 1 + (options.index(month_text) * 0.025)
            channel_qty = {
                ch: int(max(0, np.random.normal(base / 5 * season_factor, base * 0.04)))
                for ch in CHANNELS
            }

            monthly_ai = int(sum(channel_qty.values()) * np.random.uniform(0.85, 1.15))
            monthly_buyer = int(monthly_ai * np.random.uniform(0.88, 1.18))
            monthly_actual = int(monthly_buyer * np.random.uniform(0.8, 1.28))

            rows.append(
                {
                    "月份": month_text,
                    "日期": f"{start.strftime('%Y/%m/%d')} - {end.strftime('%Y/%m/%d')}",
                    "料件名稱": item["料件名稱"],
                    "料號": item["料號"],
                    "THD": channel_qty["THD"],
                    "VC": channel_qty["VC"],
                    "SC": channel_qty["SC"],
                    "DF": channel_qty["DF"],
                    "other": channel_qty["other"],
                    "AI預測該月剩餘需求": monthly_ai,
                    "採購人員預測該月剩餘需求": monthly_buyer,
                    "實際銷售數據": monthly_actual,
                }
            )

    df = pd.DataFrame(rows)
    df["Variance"] = df["實際銷售數據"] / df["採購人員預測該月剩餘需求"] - 1
    return df


BOM_MAP = {
    "71033": [
        {"子件": "14802", "component QTY": 1},
        {"子件": "80122", "component QTY": 2},
    ],
    "71033-P2": [
        {"子件": "14802", "component QTY": 2},
        {"子件": "92015", "component QTY": 1},
    ],
    "MB-003": [
        {"子件": "71033", "component QTY": 1},
        {"子件": "ANT-007", "component QTY": 1},
        {"子件": "LEN-002", "component QTY": 1},
    ],
    "TRN-009": [
        {"子件": "63591", "component QTY": 2},
        {"子件": "INS-008", "component QTY": 4},
    ],
    "74420": [
        {"子件": "22018", "component QTY": 2},
        {"子件": "SC-012", "component QTY": 8},
    ],
}


@st.cache_data
def create_planning_data():
    rows = []
    options = month_options(date(2026, 6, 1), 12)

    for month_text in options:
        for item in ITEMS:
            children = BOM_MAP.get(item["料號"], [{"子件": "-", "component QTY": 1}])

            for child in children:
                qb = int(np.random.randint(0, 350))
                fba = int(np.random.randint(0, 220))
                vc_sellable = int(np.random.randint(0, 260))
                vc_transit = int(np.random.randint(0, 180))
                vc_di = int(np.random.randint(0, 120))
                purchase_not_water = int(np.random.randint(0, 260))
                forecast = int(np.random.randint(80, 720))
                actual = int(forecast * np.random.uniform(0.72, 1.32))

                total_stock = qb + fba + vc_sellable + vc_transit + vc_di
                qty_on_hand = total_stock + purchase_not_water - forecast
                param_forecast = forecast * 3
                stock_status = qty_on_hand - param_forecast

                rows.append(
                    {
                        "年月": month_text,
                        "料件名稱": item["料件名稱"],
                        "料號": item["料號"],
                        "子件": child["子件"],
                        "component QTY": child["component QTY"],
                        "總庫存數": total_stock,
                        "QB All QOH": qb,
                        "FBA Total Units": fba,
                        "VC Sellable On Hand Units": vc_sellable,
                        "VC Inbound or Vendor in transit": vc_transit,
                        "VC Inbound -DI": vc_di,
                        "Purchase Not On Water": purchase_not_water,
                        "Forecast": forecast,
                        "實際銷售數據": actual,
                        "QTY on hand": qty_on_hand,
                        "參數* forecast": param_forecast,
                        "stock status on the end -公式": stock_status,
                    }
                )

    df = pd.DataFrame(rows)

    child_usage = (
        df[df["子件"] != "-"]
        .assign(子件需求=lambda x: x["Forecast"] * x["component QTY"])
        .groupby(["年月", "子件"], as_index=False)["子件需求"]
        .sum()
        .rename(columns={"子件": "料號", "子件需求": "被上層料件使用需求"})
    )

    df = df.merge(child_usage, on=["年月", "料號"], how="left")
    df["被上層料件使用需求"] = df["被上層料件使用需求"].fillna(0).astype(int)
    return df


forecast_df = create_forecast_data()
planning_df = create_planning_data()

if "forecast_editor_df" not in st.session_state:
    st.session_state["forecast_editor_df"] = forecast_df.copy()

# =========================================================
# Sidebar
# =========================================================
st.sidebar.markdown("## 法特科技")
st.sidebar.markdown("### 採購 AI Demo")
page = st.sidebar.radio(
    "功能選單",
    [
        "① 需求預測",
        "② 採購 Planning",
        "③ 公式與使用說明",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("#### Demo 範圍")
st.sidebar.markdown("20 個料件")
st.sidebar.markdown("未來 12 個月")
st.sidebar.markdown("可編輯採購人員預測")
st.sidebar.markdown("自動計算庫存與缺口")

# =========================================================
# Header
# =========================================================
st.markdown('<div class="main-title">法特科技｜AI 採購預測與 Planning 系統</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">用於採購團隊掌握料件需求、銷售差異、庫存水位與未來補貨風險。</div>',
    unsafe_allow_html=True,
)

# =========================================================
# Page 1 Forecast
# =========================================================
if page == "① 需求預測":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">① 需要採購的數量預測</div>', unsafe_allow_html=True)

    month_list = month_options(date(2026, 6, 1), 12)
    selected_month = st.selectbox("選擇月份", month_list, index=0)

    range_start, range_end = display_range_for_month(selected_month)
    st.markdown(
        f"""
        <span class="pill">目前日期：{TODAY.strftime('%Y/%m/%d')}</span>
        <span class="pill pill-green">查詢期間：{range_start.strftime('%Y/%m/%d')} - {range_end.strftime('%Y/%m/%d')}</span>
        <span class="pill pill-orange">資料筆數：20 個料件</span>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    df = st.session_state["forecast_editor_df"].copy()
    month_df = df[df["月份"] == selected_month].copy()
    month_df["日期"] = f"{range_start.strftime('%Y/%m/%d')} - {range_end.strftime('%Y/%m/%d')}"
    month_df["Variance"] = month_df["實際銷售數據"] / month_df["採購人員預測該月剩餘需求"] - 1

    total_ai = int(month_df["AI預測該月剩餘需求"].sum())
    total_buyer = int(month_df["採購人員預測該月剩餘需求"].sum())
    total_actual = int(month_df["實際銷售數據"].sum())
    avg_variance = month_df["Variance"].mean()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">AI 預測剩餘需求</div>
                <div class="metric-value">{total_ai:,}</div>
                <div class="metric-note">本月剩餘區間合計</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color:#2eaf5d;">
                <div class="metric-label">採購人員預測需求</div>
                <div class="metric-value">{total_buyer:,}</div>
                <div class="metric-note">可在下方表格修改</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color:#ff9800;">
                <div class="metric-label">實際銷售數據</div>
                <div class="metric-value">{total_actual:,}</div>
                <div class="metric-note">Demo 模擬銷售結果</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        color = "#d92d20" if abs(avg_variance) > 0.15 else "#2eaf5d"
        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color:{color};">
                <div class="metric-label">平均 Variance</div>
                <div class="metric-value">{avg_variance:.1%}</div>
                <div class="metric-note">實際 / 採購預測 - 1</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    high_risk = month_df[month_df["Variance"].abs() >= 0.2]
    if len(high_risk) > 0:
        st.markdown(
            f"""
            <div class="warning-box">
                偵測到 {len(high_risk)} 個料件 Variance 超過 ±20%，建議採購重新檢查預測量或補貨節奏。
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="success-box">
                本月料件預測差異皆在可控範圍內。
            </div>
            """,
            unsafe_allow_html=True,
        )

    edit_cols = [
        "日期",
        "料件名稱",
        "料號",
        "THD",
        "VC",
        "SC",
        "DF",
        "other",
        "AI預測該月剩餘需求",
        "採購人員預測該月剩餘需求",
        "實際銷售數據",
        "Variance",
    ]

    edited = st.data_editor(
        month_df[edit_cols],
        use_container_width=True,
        hide_index=True,
        height=620,
        disabled=[
            "日期",
            "料件名稱",
            "料號",
            "THD",
            "VC",
            "SC",
            "DF",
            "other",
            "AI預測該月剩餘需求",
            "實際銷售數據",
            "Variance",
        ],
        column_config={
            "採購人員預測該月剩餘需求": st.column_config.NumberColumn(
                "採購人員預測該月剩餘需求",
                min_value=0,
                step=10,
                help="採購可自行修正本月剩餘需求預測",
            ),
            "Variance": st.column_config.NumberColumn(
                "Variance",
                format="%.2f",
                help="實際銷售數據 / 採購人員預測該月剩餘需求 - 1",
            ),
        },
        key=f"forecast_editor_{selected_month}",
    )

    update_map = edited.set_index("料號")["採購人員預測該月剩餘需求"].to_dict()
    mask = st.session_state["forecast_editor_df"]["月份"] == selected_month

    st.session_state["forecast_editor_df"].loc[
        mask, "採購人員預測該月剩餘需求"
    ] = st.session_state["forecast_editor_df"].loc[mask, "料號"].map(update_map)

    st.session_state["forecast_editor_df"]["Variance"] = (
        st.session_state["forecast_editor_df"]["實際銷售數據"]
        / st.session_state["forecast_editor_df"]["採購人員預測該月剩餘需求"]
        - 1
    )

    st.write("")
    chart_df = st.session_state["forecast_editor_df"]
    chart_df = chart_df[chart_df["月份"] == selected_month].copy()
    chart_df["Variance"] = chart_df["實際銷售數據"] / chart_df["採購人員預測該月剩餘需求"] - 1

    left, right = st.columns([1.1, 0.9])

    with left:
        fig = px.bar(
            chart_df,
            x="料號",
            y=["AI預測該月剩餘需求", "採購人員預測該月剩餘需求", "實際銷售數據"],
            barmode="group",
            title="AI 預測 vs 採購預測 vs 實際銷售",
        )
        fig.update_layout(
            height=430,
            legend_title_text="指標",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig2 = px.bar(
            chart_df,
            x="料號",
            y="Variance",
            title="Variance 差異監控",
        )
        fig2.update_layout(
            height=430,
            yaxis_tickformat=".0%",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# Page 2 Planning
# =========================================================
elif page == "② 採購 Planning":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">② Demo 採購 Planning</div>', unsafe_allow_html=True)

    month_list = month_options(date(2026, 6, 1), 12)
    selected_month = st.selectbox("選擇年月", month_list, index=0)

    st.markdown(
        f"""
        <span class="pill">年月：{selected_month}</span>
        <span class="pill pill-green">公式自動計算</span>
        <span class="pill pill-orange">此頁不提供修改功能</span>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    month_plan = planning_df[planning_df["年月"] == selected_month].copy()

    shortage_count = int((month_plan["stock status on the end -公式"] < 0).sum())
    total_stock = int(month_plan["總庫存數"].sum())
    total_forecast = int(month_plan["Forecast"].sum())
    total_shortage = int(month_plan.loc[month_plan["stock status on the end -公式"] < 0, "stock status on the end -公式"].sum())

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">總庫存數合計</div>
                <div class="metric-value">{total_stock:,}</div>
                <div class="metric-note">五種庫存來源加總</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color:#2eaf5d;">
                <div class="metric-label">Forecast 合計</div>
                <div class="metric-value">{total_forecast:,}</div>
                <div class="metric-note">本月預測需求</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color:#d92d20;">
                <div class="metric-label">低於安全水位筆數</div>
                <div class="metric-value">{shortage_count}</div>
                <div class="metric-note">stock status 小於 0</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color:#ff9800;">
                <div class="metric-label">缺口合計</div>
                <div class="metric-value">{total_shortage:,}</div>
                <div class="metric-note">負數代表需要補貨</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    if shortage_count > 0:
        st.markdown(
            f"""
            <div class="warning-box">
                本月共有 {shortage_count} 筆料件或子件低於安全庫存水位，建議優先安排採購或確認在途數量。
            </div>
            """,
            unsafe_allow_html=True,
        )

    display_cols = [
        "年月",
        "料件名稱",
        "料號",
        "子件",
        "component QTY",
        "被上層料件使用需求",
        "總庫存數",
        "QB All QOH",
        "FBA Total Units",
        "VC Sellable On Hand Units",
        "VC Inbound or Vendor in transit",
        "VC Inbound -DI",
        "Purchase Not On Water",
        "Forecast",
        "實際銷售數據",
        "QTY on hand",
        "參數* forecast",
        "stock status on the end -公式",
    ]

    st.dataframe(
        month_plan[display_cols],
        use_container_width=True,
        hide_index=True,
        height=620,
        column_config={
            "stock status on the end -公式": st.column_config.NumberColumn(
                "stock status on the end -公式",
                help="QTY on hand - 參數* forecast",
            ),
            "被上層料件使用需求": st.column_config.NumberColumn(
                "被上層料件使用需求",
                help="此料號被其他父料件作為子件使用的總需求",
            ),
        },
    )

    st.write("")

    left, right = st.columns([1, 1])

    with left:
        chart = month_plan.groupby("料號", as_index=False)[
            ["總庫存數", "Forecast", "QTY on hand", "參數* forecast"]
        ].sum()

        fig = px.bar(
            chart,
            x="料號",
            y=["總庫存數", "Forecast", "QTY on hand", "參數* forecast"],
            barmode="group",
            title="料件庫存與 Forecast 比較",
        )
        fig.update_layout(
            height=450,
            legend_title_text="指標",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        risk = (
            month_plan.groupby("料號", as_index=False)["stock status on the end -公式"]
            .sum()
            .sort_values("stock status on the end -公式")
        )
        fig2 = px.bar(
            risk,
            x="料號",
            y="stock status on the end -公式",
            title="月底庫存狀態缺口排序",
        )
        fig2.update_layout(
            height=450,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 子件使用量統計")
    st.markdown(
        """
        <div class="info-box">
            若某料號同時也是其他料件的子件，系統會依照「父料件 Forecast × component QTY」統計該子件被使用的總需求。
        </div>
        """,
        unsafe_allow_html=True,
    )

    child_summary = (
        month_plan[month_plan["子件"] != "-"]
        .assign(子件需求=lambda x: x["Forecast"] * x["component QTY"])
        .groupby(["子件"], as_index=False)["子件需求"]
        .sum()
        .sort_values("子件需求", ascending=False)
    )

    st.dataframe(
        child_summary,
        use_container_width=True,
        hide_index=True,
        height=300,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# Page 3 Formula
# =========================================================
else:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">③ 公式與使用邏輯說明</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-box">
            本 Demo 提供法特科技採購團隊使用，請勿外傳。
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## 一、需求預測頁使用邏輯")

    st.markdown(
        """
| 功能 | 說明 |
|---|---|
| 月份選單 | 可選擇 2026/06 起算未來 12 個月 |
| 2026/06 顯示區間 | 因 Demo 今日設定為 2026/06/16，所以選 2026/06 時顯示 2026/06/16 - 2026/06/30 |
| 其他月份顯示區間 | 例如選 2026/07，顯示 2026/07/01 - 2026/07/31 |
| 料件數量 | Demo 產生 20 個料件 |
| 通路購買數量 | THD、VC、SC、DF、other 五個通路分開呈現 |
| 可編輯欄位 | 採購人員預測該月剩餘需求 |
| 不可編輯欄位 | 日期、料件名稱、料號、通路數量、AI 預測、實際銷售數據、Variance |
"""
    )

    st.markdown("## 二、需求預測頁公式")

    st.latex(r"Variance = \frac{實際銷售數據}{採購人員預測該月剩餘需求} - 1")

    st.markdown(
        """
| 指標 | 判斷方式 |
|---|---|
| Variance > 0 | 實際銷售高於採購人員預測，可能有缺貨風險 |
| Variance < 0 | 實際銷售低於採購人員預測，可能有庫存過高風險 |
| abs(Variance) >= 20% | 系統顯示警告，建議重新檢查預測 |
"""
    )

    st.markdown("## 三、採購 Planning 頁使用邏輯")

    st.markdown(
        """
| 欄位 | 說明 |
|---|---|
| 年月 | 採購 Planning 的月份 |
| 料件名稱 | 主料件名稱 |
| 料號 | 主料件料號 |
| 子件 | 若主料件有 BOM 結構，列出其子件料號 |
| component QTY | 生產 1 個主料件需要消耗多少子件 |
| 被上層料件使用需求 | 當某料號被其他主料件當作子件時，統計其被使用的總需求 |
| Forecast | 預測需求數 |
| 實際銷售數據 | Demo 模擬銷售結果 |
| stock status on the end -公式 | 月底庫存安全水位判斷 |
"""
    )

    st.markdown("## 四、採購 Planning 公式")

    st.markdown("### 1. 總庫存數")
    st.latex(
        r"""
        總庫存數 =
        QB\ All\ QOH
        + FBA\ Total\ Units
        + VC\ Sellable\ On\ Hand\ Units
        + VC\ Inbound\ or\ Vendor\ in\ transit
        + VC\ Inbound\ -DI
        """
    )

    st.markdown("### 2. QTY on hand")
    st.latex(
        r"""
        QTY\ on\ hand =
        總庫存數
        + Purchase\ Not\ On\ Water
        - Forecast
        """
    )

    st.markdown("### 3. 參數 * forecast")
    st.latex(
        r"""
        參數 * forecast = Forecast \times 3
        """
    )

    st.markdown("### 4. stock status on the end -公式")
    st.latex(
        r"""
        stock\ status\ on\ the\ end =
        QTY\ on\ hand
        - 參數 * forecast
        """
    )

    st.markdown("### 5. 子件需求統計")
    st.latex(
        r"""
        子件需求 =
        父料件Forecast
        \times
        component\ QTY
        """
    )

    st.markdown(
        """
        若同一個子件被多個主料件使用，系統會把每一筆子件需求加總：
        """
    )

    st.latex(
        r"""
        子件總需求 =
        \sum(父料件Forecast \times component\ QTY)
        """
    )

    st.markdown("## 五、採購判斷建議")

    st.markdown(
        """
| 狀態 | 判斷邏輯 | 採購建議 |
|---|---|---|
| stock status on the end < 0 | 月底庫存低於安全需求 | 優先採購或確認在途數量 |
| stock status on the end = 0 | 剛好滿足安全水位 | 建議觀察銷售波動 |
| stock status on the end > 0 | 庫存高於安全水位 | 可延後採購或降低下單量 |
| Variance 過高 | 實際銷售高於預測 | 檢查是否需要追加採購 |
| Variance 過低 | 實際銷售低於預測 | 檢查是否有庫存積壓 |
"""
    )

    st.markdown("</div>", unsafe_allow_html=True)
