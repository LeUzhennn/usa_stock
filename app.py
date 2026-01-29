import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

# --- 頁面配置 ---
st.set_page_config(
    page_title="美股綜合分析系統 (Streamlit UI 範例)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 模擬數據與功能 (Placeholder) ---

def get_dummy_candlestick_chart(ticker: str) -> go.Figure:
    """模擬生成一個 Plotly K 線圖"""
    # 創建模擬數據
    data = {
        'Date': pd.to_datetime(pd.date_range(start='2025-01-01', periods=100, freq='D')),
        'Open': [100 + i % 10 for i in range(100)],
        'High': [105 + i % 10 for i in range(100)],
        'Low': [95 + i % 10 for i in range(100)],
        'Close': [102 + i % 10 for i in range(100)],
    }
    df = pd.DataFrame(data)

    # 創建 K 線圖
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Candlestick'
    )])

    fig.update_layout(
        title=f'{ticker} 股價走勢 (模擬數據)',
        xaxis_rangeslider_visible=False,
        height=500
    )
    return fig

# --- 側邊欄控制項實作 ---

# 預設值
today = date.today()
default_start_date = today - timedelta(days=10 * 365) # 10 年前

st.sidebar.title("📈 股市分析儀")

# 股票代碼輸入
ticker = st.sidebar.text_input("請輸入美股代碼", "AAPL").upper()

# 日期範圍選擇
st.sidebar.subheader("📅 分析日期範圍")
start_date = st.sidebar.date_input("起始日期", default_start_date)
end_date = st.sidebar.date_input("結束日期", today)

# 策略回測控制項
st.sidebar.subheader("⚙️ 策略回測設定")
strategy_options = {
    "均線交叉策略": "GoldenCross",
    "突破策略": "Breakout",
    "多因子綜合策略": "MultiFactor"
}
selected_strategy_name = st.sidebar.selectbox(
    "選擇回測策略",
    list(strategy_options.keys())
)
selected_strategy_key = strategy_options[selected_strategy_name]

# 根據選擇的策略顯示參數調整
st.sidebar.markdown("---")
st.sidebar.subheader("參數調整")

if selected_strategy_key == "GoldenCross":
    fast_ma = st.sidebar.slider("短期均線 (Fast MA)", 5, 60, 20)
    slow_ma = st.sidebar.slider("長期均線 (Slow MA)", 50, 300, 60)
    st.sidebar.info(f"策略參數: 短期 {fast_ma} 日, 長期 {slow_ma} 日")

elif selected_strategy_key == "Breakout":
    period = st.sidebar.slider("突破週期 (Period)", 5, 100, 20)
    st.sidebar.info(f"策略參數: {period} 日突破")

elif selected_strategy_key == "MultiFactor":
    rsi_buy = st.sidebar.slider("RSI 買入閾值", 10, 40, 30)
    rsi_sell = st.sidebar.slider("RSI 賣出閾值", 60, 90, 70)
    st.sidebar.info(f"策略參數: RSI 買入 < {rsi_buy}, 賣出 > {rsi_sell}")

# 執行回測按鈕
st.sidebar.markdown("---")
if st.sidebar.button("🚀 執行策略回測"):
    st.sidebar.success("回測請求已送出...")
    # 這裡將調用 backtester/engine.py 中的 run_backtest 函式

# --- 主內容區分頁實作 ---

st.title(f"美股綜合分析系統 - {ticker}")
st.markdown(f"分析期間: **{start_date}** 至 **{end_date}**")

# 使用 st.tabs 創建分頁
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "總覽 (Overview)",
    "基本面 (Fundamental)",
    "技術面 (Technical)",
    "心理面 (Sentiment)",
    "策略回測 (Backtest)"
])

with tab1:
    st.header("總覽")
    st.info(f"正在顯示 {ticker} 的公司基本資訊與股價摘要...")
    # 這裡將顯示 get_info(ticker) 的結果
    st.subheader("股價走勢")
    st.plotly_chart(get_dummy_candlestick_chart(ticker))

with tab2:
    st.header("基本面分析")
    st.warning("此處將顯示財務報表趨勢圖與財務比率表格。")
    # 這裡將調用 analysis/fundamental.py 中的函式

with tab3:
    st.header("技術面分析")
    st.warning("此處將顯示可疊加技術指標的互動式 K 線圖。")
    # 這裡將調用 analysis/technical.py 中的函式

with tab4:
    st.header("心理面分析")
    st.warning("此處將顯示 VIX 恐慌指數圖與新聞情緒分析結果。")
    # 這裡將調用 analysis/sentiment.py 中的函式

with tab5:
    st.header("策略回測結果")
    st.warning(f"當前選擇策略: **{selected_strategy_name}**。回測結果將在此處呈現。")
    # 這裡將顯示 backtester/engine.py 輸出的績效報告與權益曲線圖
    st.subheader("績效指標 (Performance Metrics)")
    st.dataframe(pd.DataFrame({
        "指標": ["年化報酬率", "最大回撤", "夏普比率"],
        "數值": ["25.5%", "-15.2%", "1.5"]
    }))
    st.subheader("權益曲線圖 (Equity Curve)")
    # 這裡將顯示模擬的權益曲線圖

st.markdown("---")
st.caption("本應用程式為美股分析系統的 Streamlit 介面設計範例。")
