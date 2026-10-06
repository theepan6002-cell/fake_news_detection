import React, { useState, useEffect } from "react";
import { getDashboardStats } from "../services/api";
import LoadingSpinner from "../components/LoadingSpinner";

export default function Dashboard({ setToast }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const data = await getDashboardStats();
      setStats(data);
    } catch (err) {
      setToast({ type: "error", message: err.message || "Failed to load dashboard data." });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="bg-slate-900/60 rounded-2xl border border-slate-800 p-12 my-8">
        <LoadingSpinner label="Fetching Live Analytics & Model Performance Metrics..." />
      </div>
    );
  }

  const cards = stats?.cards || {};
  const cm = stats?.confusion_matrix || { tp: 0, tn: 0, fp: 0, fn: 0 };
  const timeline = stats?.timeline || [];
  const modelPerf = stats?.model_performance || {};

  const total = (cards.likely_real || 0) + (cards.likely_fake || 0);
  const realPct = total > 0 ? Math.round((cards.likely_real / total) * 100) : 50;
  const fakePct = 100 - realPct;

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white">AI Analytics & Performance Dashboard</h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time inference statistics and dynamic Machine Learning model metrics.
          </p>
        </div>
        <button
          onClick={fetchStats}
          className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-xl text-xs font-semibold transition-all flex items-center space-x-2 self-start sm:self-auto"
        >
          <span>🔄 Refresh Stats</span>
        </button>
      </div>

      {/* Section 1: 7 KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-4">
        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-xs text-slate-400 font-medium">Total Checked</span>
          <p className="text-2xl font-black text-white font-mono">{cards.total_checked || 0}</p>
          <span className="text-[10px] text-indigo-400">Live DB Audit</span>
        </div>

        <div className="bg-emerald-950/20 border border-emerald-500/30 p-4 rounded-xl space-y-1">
          <span className="text-xs text-emerald-400 font-medium">Likely Real</span>
          <p className="text-2xl font-black text-emerald-300 font-mono">{cards.likely_real || 0}</p>
          <span className="text-[10px] text-emerald-400/80">{realPct}% of total</span>
        </div>

        <div className="bg-rose-950/20 border border-rose-500/30 p-4 rounded-xl space-y-1">
          <span className="text-xs text-rose-400 font-medium">Likely Fake</span>
          <p className="text-2xl font-black text-rose-300 font-mono">{cards.likely_fake || 0}</p>
          <span className="text-[10px] text-rose-400/80">{fakePct}% of total</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-xs text-slate-400 font-medium">Model Accuracy</span>
          <p className="text-2xl font-black text-cyan-400 font-mono">{cards.accuracy}%</p>
          <span className="text-[10px] text-slate-500">Test Set</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-xs text-slate-400 font-medium">Precision</span>
          <p className="text-2xl font-black text-purple-400 font-mono">{cards.precision}%</p>
          <span className="text-[10px] text-slate-500">True Positives</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-xs text-slate-400 font-medium">Recall</span>
          <p className="text-2xl font-black text-amber-400 font-mono">{cards.recall}%</p>
          <span className="text-[10px] text-slate-500">Sensitivity</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-xs text-slate-400 font-medium">F1 Score</span>
          <p className="text-2xl font-black text-emerald-400 font-mono">{cards.f1_score}%</p>
          <span className="text-[10px] text-slate-500">Harmonic Mean</span>
        </div>
      </div>

      {/* Section 2: Visual Charts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* A. Real vs Fake Donut Chart */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4">
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <span>🍩</span>
            <span>Real vs Fake Predictions</span>
          </h3>

          <div className="flex items-center justify-center py-6">
            <div className="relative w-44 h-44 rounded-full border-8 border-slate-800 flex items-center justify-center">
              {/* Conic Gradient Donut Ring */}
              <div
                className="absolute inset-0 rounded-full"
                style={{
                  background: `conic-gradient(#10b981 0% ${realPct}%, #f43f5e ${realPct}% 100%)`
                }}
              />
              {/* Inner Circle */}
              <div className="absolute inset-4 rounded-full bg-slate-950 flex flex-col items-center justify-center z-10 shadow-inner">
                <span className="text-2xl font-extrabold text-white font-mono">{total}</span>
                <span className="text-[10px] text-slate-400 uppercase">Total News</span>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2 text-center pt-2">
            <div className="bg-emerald-950/30 border border-emerald-800/40 p-2 rounded-xl">
              <span className="text-xs font-semibold text-emerald-400">Likely Real</span>
              <p className="text-lg font-bold text-white font-mono">{cards.likely_real || 0} ({realPct}%)</p>
            </div>
            <div className="bg-rose-950/30 border border-rose-800/40 p-2 rounded-xl">
              <span className="text-xs font-semibold text-rose-400">Likely Fake</span>
              <p className="text-lg font-bold text-white font-mono">{cards.likely_fake || 0} ({fakePct}%)</p>
            </div>
          </div>
        </div>

        {/* B. Predictions Over Time (Line Chart Timeline) */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 lg:col-span-2">
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <span>📈</span>
            <span>Predictions Over Time (Activity Timeline)</span>
          </h3>

          {timeline.length > 0 ? (
            <div className="space-y-3 py-2">
              {timeline.map((item, idx) => {
                const maxVal = Math.max(...timeline.map((t) => t.total || 1));
                const widthPct = Math.min(100, Math.max(10, (item.total / maxVal) * 100));
                return (
                  <div key={idx} className="space-y-1">
                    <div className="flex justify-between text-xs font-mono">
                      <span className="text-slate-300 font-semibold">{item.date}</span>
                      <span className="text-slate-400">{item.total} checked ({item.real} Real, {item.fake} Fake)</span>
                    </div>
                    <div className="w-full bg-slate-950 rounded-full h-3 flex overflow-hidden border border-slate-800">
                      <div
                        className="bg-emerald-500 h-full transition-all"
                        style={{ width: `${(item.real / (item.total || 1)) * widthPct}%` }}
                      />
                      <div
                        className="bg-rose-500 h-full transition-all"
                        style={{ width: `${(item.fake / (item.total || 1)) * widthPct}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="p-8 text-center text-slate-500 text-xs">
              No historical timeline data recorded yet.
            </div>
          )}
        </div>

        {/* D. Model Performance Comparison */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 lg:col-span-2">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-white flex items-center space-x-2">
              <span>🤖</span>
              <span>Machine Learning Model Comparison</span>
            </h3>
            <span className="text-xs px-2.5 py-0.5 bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 rounded-full">
              Selected: {stats?.best_model_name || "Logistic Regression"}
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-950 text-slate-400 uppercase font-mono border-b border-slate-800">
                <tr>
                  <th className="p-3">Model Algorithm</th>
                  <th className="p-3">Accuracy</th>
                  <th className="p-3">Precision</th>
                  <th className="p-3">Recall</th>
                  <th className="p-3">F1 Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono">
                {Object.keys(modelPerf).length > 0 ? (
                  Object.entries(modelPerf).map(([key, m]) => (
                    <tr key={key} className="hover:bg-slate-800/40">
                      <td className="p-3 font-sans font-semibold text-white flex items-center space-x-2">
                        <span>{m.model_name === stats?.best_model_name ? "⭐" : "🔹"}</span>
                        <span>{m.model_name}</span>
                      </td>
                      <td className="p-3 text-cyan-400 font-bold">{(m.accuracy * 100).toFixed(2)}%</td>
                      <td className="p-3 text-purple-400 font-bold">{(m.precision * 100).toFixed(2)}%</td>
                      <td className="p-3 text-amber-400 font-bold">{(m.recall * 100).toFixed(2)}%</td>
                      <td className="p-3 text-emerald-400 font-bold">{(m.f1_score).toFixed(4)}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={5} className="p-4 text-center text-slate-500">
                      No model metrics recorded.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* E. Confusion Matrix Card */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4">
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <span>🎯</span>
            <span>Confusion Matrix (Test Evaluation)</span>
          </h3>

          <div className="grid grid-cols-2 gap-3 pt-2">
            <div className="bg-emerald-950/40 border border-emerald-500/40 p-4 rounded-xl text-center space-y-1">
              <span className="text-[10px] uppercase font-bold text-emerald-400 tracking-wider">
                True Positives (TP)
              </span>
              <p className="text-2xl font-black text-white font-mono">{cm.tp || 0}</p>
              <p className="text-[10px] text-slate-400">Actual Real → Pred Real</p>
            </div>

            <div className="bg-rose-950/40 border border-rose-500/40 p-4 rounded-xl text-center space-y-1">
              <span className="text-[10px] uppercase font-bold text-rose-400 tracking-wider">
                False Positives (FP)
              </span>
              <p className="text-2xl font-black text-white font-mono">{cm.fp || 0}</p>
              <p className="text-[10px] text-slate-400">Actual Fake → Pred Real</p>
            </div>

            <div className="bg-amber-950/40 border border-amber-500/40 p-4 rounded-xl text-center space-y-1">
              <span className="text-[10px] uppercase font-bold text-amber-400 tracking-wider">
                False Negatives (FN)
              </span>
              <p className="text-2xl font-black text-white font-mono">{cm.fn || 0}</p>
              <p className="text-[10px] text-slate-400">Actual Real → Pred Fake</p>
            </div>

            <div className="bg-teal-950/40 border border-teal-500/40 p-4 rounded-xl text-center space-y-1">
              <span className="text-[10px] uppercase font-bold text-teal-400 tracking-wider">
                True Negatives (TN)
              </span>
              <p className="text-2xl font-black text-white font-mono">{cm.tn || 0}</p>
              <p className="text-[10px] text-slate-400">Actual Fake → Pred Fake</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
