import json
import yfinance as yf
import pandas as pd
import requests

def run_vectorized_backtest(strategy, start_date: str, end_date: str) -> dict:
    """
    Downloads historical stock datasets via an unblocked request mechanism,
    simulates trading strategy vectors, and returns structured metrics.
    """
    # Force upper-case symbol mapping
    ticker = strategy.ticker.upper()

    # Smart Ticker mapping fallback for Gold commodity requests
    if ticker == "XAU":
        ticker = "GC=F"  # Auto-correct to Yahoo Finance Gold Futures
        print("💡 Ticker XAU automatically remapped to standard Yahoo Gold Futures (GC=F)")

    print(f"📈 Executing calculation pipeline for asset: {ticker}")

    # 1. Forge a vanilla Requests Session with realistic browser emulation headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    })

    # 2. Extract price array safely bypassing the internal curl_cffi routine completely
    try:
        # We leverage yf.Ticker().history to completely isolate network behaviors from yf.download
        ticker_obj = yf.Ticker(ticker, session=session)
        df = ticker_obj.history(start=start_date, end=end_date, interval="1d")
    except Exception as e:
        raise ValueError(f"Network downloading wrapper failed: {str(e)}")

    if df.empty or 'Close' not in df.columns:
        raise ValueError(f"No historical asset data returned for ticker '{ticker}'. Ensure your network is online.")

    # 3. Clean and Flatten DataFrames (Handles single or multi-index tables safely)
    df = df.sort_index()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    # Standardize Series items out of any dimensional array wrappers
    df['Close'] = df['Close'].astype(float)

    # 4. Standard Indicator Building Framework
    # Dynamically map custom SMA/EMA references derived from the LLM engine
    for ind in [strategy.indicator_1, strategy.indicator_2]:
        if "SMA" in ind:
            period = int(''.join(filter(str.isdigit, ind)) or 50)
            df[ind] = df['Close'].rolling(window=period).mean()
        elif "EMA" in ind:
            period = int(''.join(filter(str.isdigit, ind)) or 20)
            df[ind] = df['Close'].ewm(span=period, adjust=False).mean()

    # Apply fail-safes if the indicators generated are unrecognized structural properties
    if strategy.indicator_1 not in df.columns:
        df[strategy.indicator_1] = df['Close'].rolling(window=50).mean()
    if strategy.indicator_2 not in df.columns:
        df[strategy.indicator_2] = df['Close'].rolling(window=200).mean()

    # 5. Execute Vectorized Backtest Calculations
    df['Signal'] = 0
    if "above" in strategy.condition or "greater" in strategy.condition:
        df.loc[df[strategy.indicator_1] > df[strategy.indicator_2], 'Signal'] = 1
    else:
        df.loc[df[strategy.indicator_1] < df[strategy.indicator_2], 'Signal'] = 1

    df['Position'] = df['Signal'].shift(1).fillna(0)
    df['Market_Returns'] = df['Close'].pct_change().fillna(0)
    df['Strategy_Returns'] = df['Position'] * df['Market_Returns']

    # Generate the compounding tracking timeline scale normalized at baseline 100
    df['Cumulative_Strategy'] = (1 + df['Strategy_Returns']).cumprod()
    df['Equity_Curve'] = df['Cumulative_Strategy'] * 100

    # 6. Performance Analytical Metrics Parsing
    total_return = round((df['Cumulative_Strategy'].iloc[-1] - 1) * 100, 2)
    daily_std = df['Strategy_Returns'].std()
    mean_return = df['Strategy_Returns'].mean()
    sharpe_ratio = round((mean_return / daily_std) * (252 ** 0.5), 2) if daily_std != 0 else 0.0

    rolling_max = df['Equity_Curve'].cummax()
    drawdown = (df['Equity_Curve'] - rolling_max) / rolling_max
    max_drawdown = round(drawdown.min() * 100, 2)

    # 7. Convert timeline structures into a clean JSON array for our React Dashboard Recharts line graph
    chart_payload = []
    for date, row in df.iterrows():
        chart_payload.append({
            "date": date.strftime('%Y-%m-%d'),
            "value": round(float(row['Equity_Curve']), 2)
        })

    return {
        "ticker": ticker,
        "totalReturn": total_return,
        "sharpeRatio": sharpe_ratio,
        "maxDrawdown": max_drawdown,
        "equityCurveJson": json.dumps(chart_payload)
    }