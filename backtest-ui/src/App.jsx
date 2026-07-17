import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Play, TrendingUp, AlertTriangle, Activity } from 'lucide-react';

export default function App() {
  const [prompt, setPrompt] = useState("Buy when SMA_50 crosses above SMA_200 and sell when it falls below");
  const [ticker, setTicker] = useState("AAPL");
  const [startDate, setStartDate] = useState("2023-01-01");
  const [endDate, setEndDate] = useState("2025-01-01");

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [chartData, setChartData] = useState([]);

  const handleRunBacktest = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8080/api/v1/backtests/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, ticker, startDate, endDate })
      });

      const data = await response.json();
      setResults(data);

      if (data.equityCurveJson) {
        setChartData(JSON.parse(data.equityCurveJson));
      }
    } catch (error) {
      alert("Failed to execute backtest. Ensure Spring Boot and Python engines are active.");
    } finally {
      setLoading(false);
    }
  };

  return (
      <div className="min-h-screen p-8 max-w-7xl mx-auto bg-slate-950 text-slate-100 text-left">
        <header className="mb-8 border-b border-slate-800 pb-4">
          <h1 className="text-3xl font-bold tracking-tight text-white text-left">Natural Language Strategy Backtester</h1>
          <p className="text-slate-400 mt-1">Convert Plain-English Trading Rules into Executable Financial Analytics</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Input Configuration Panel */}
          <div className="lg:col-span-1 bg-slate-900 border border-slate-800 p-6 rounded-xl flex flex-col gap-4">
            <h2 className="text-xl font-semibold text-slate-200">Strategy Rules</h2>

            <div>
              <label className="text-xs font-semibold text-slate-400 block mb-1">PLAIN-ENGLISH RULES</label>
              <textarea
                  rows="4"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-sm text-slate-200 focus:outline-none focus:border-indigo-500 resize-none"
              />
            </div>

            <div className="grid grid-cols-3 gap-2">
              <div className="col-span-1">
                <label className="text-xs font-semibold text-slate-400 block mb-1">TICKER</label>
                <input type="text" value={ticker} onChange={(e) => setTicker(e.target.value.toUpperCase())} className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-sm text-center text-slate-200 focus:outline-none focus:border-indigo-500" />
              </div>
              <div className="col-span-2">
                <label className="text-xs font-semibold text-slate-400 block mb-1">START DATE</label>
                <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500" />
              </div>
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-400 block mb-1">END DATE</label>
              <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500" />
            </div>

            <button
                onClick={handleRunBacktest}
                disabled={loading}
                className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 text-white font-medium p-3 rounded-lg flex items-center justify-center gap-2 transition cursor-pointer mt-2"
            >
              {loading ? "Processing Performance..." : <><Play size={16} fill="currentColor"/> Run Backtest</>}
            </button>
          </div>

          {/* Dashboard Analytics & Graph View */}
          <div className="lg:col-span-2 flex flex-col gap-6">
            {/* Performance Summary Cards */}
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex items-center gap-4">
                <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-lg"><TrendingUp size={24}/></div>
                <div>
                  <span className="text-xs text-slate-400 font-medium block">TOTAL RETURN</span>
                  <span className={`text-xl font-bold ${results?.totalReturn >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                  {results ? `${results.totalReturn}%` : '—'}
                </span>
                </div>
              </div>

              <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex items-center gap-4">
                <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-lg"><Activity size={24}/></div>
                <div>
                  <span className="text-xs text-slate-400 font-medium block">SHARPE RATIO</span>
                  <span className="text-xl font-bold text-slate-200">{results ? results.sharpeRatio : '—'}</span>
                </div>
              </div>

              <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex items-center gap-4">
                <div className="p-3 bg-rose-500/10 text-rose-400 rounded-lg"><AlertTriangle size={24}/></div>
                <div>
                  <span className="text-xs text-slate-400 font-medium block">MAX DRAWDOWN</span>
                  <span className="text-xl font-bold text-rose-400">{results ? `${results.maxDrawdown}%` : '—'}</span>
                </div>
              </div>
            </div>

            {/* Interactive Equity Chart Frame */}
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl flex-1 min-h-[400px] flex flex-col">
              <h3 className="text-lg font-semibold text-slate-200 mb-4">Strategy Growth Curve</h3>
              <div className="flex-1 w-full min-h-[320px]">
                {chartData.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                        <XAxis dataKey="date" stroke="#64748b" fontSize={12} tickLine={false} />
                        <YAxis stroke="#64748b" fontSize={12} tickLine={false} domain={['auto', 'auto']} />
                        <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }} />
                        <Line type="monotone" dataKey="value" stroke="#6366f1" strokeWidth={2.5} dot={false} />
                      </LineChart>
                    </ResponsiveContainer>
                ) : (
                    <div className="h-full flex items-center justify-center text-slate-500 text-sm border-2 border-dashed border-slate-800 rounded-lg">
                      Submit text configuration settings rules to calculate equity matrix curves
                    </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
  );
}