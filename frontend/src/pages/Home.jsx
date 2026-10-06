import React, { useState } from "react";
import { predictNews } from "../services/api";
import LoadingSpinner from "../components/LoadingSpinner";

const SAMPLE_REAL = `WASHINGTON (Reuters) - The US Federal Reserve maintained interest rates at current benchmarks today, signaling a cautious approach toward inflation and economic indicators. Chairman Powell noted that labor market conditions remain stable while consumer price indices show encouraging signs of gradual deceleration toward the target target range.`;

const SAMPLE_FAKE = `SHOCKING REVELATION: Secret miracle elixir discovered by underground scientists reverses aging process by 30 years in just 48 hours! Pharmaceutical giants are trying to ban this document from public view! Read before it gets deleted!`;

export default function Home({ setActivePage, setToast }) {
  const [newsText, setNewsText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    if (!newsText.trim()) {
      setToast({ type: "error", message: "Please enter news article text before analyzing." });
      return;
    }
    setLoading(true);
    setResult(null);

    try {
      const data = await predictNews(newsText);
      setResult(data);
      setToast({ type: "success", message: `Classification complete: ${data.prediction}` });
    } catch (err) {
      setToast({ type: "error", message: err.message || "Classification failed." });
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setNewsText("");
    setResult(null);
  };

  const wordCount = newsText.trim() ? newsText.trim().split(/\s+/).length : 0;
  const isReal = result?.prediction === "Likely Real";

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-12">
      {/* Hero Header */}
      <div className="text-center space-y-4 pt-4">
        <div className="inline-flex items-center space-x-2 px-3 py-1 bg-indigo-500/10 border border-indigo-500/20 rounded-full text-indigo-300 text-xs font-semibold">
          <span>🧠 NLP & TF-IDF Vectorization</span>
          <span>•</span>
          <span>Machine Learning Intelligence</span>
        </div>
        <h1 className="text-4xl sm:text-5xl font-extrabold text-white tracking-tight">
          AI Fake News Detector & Analytics
        </h1>
        <p className="max-w-2xl mx-auto text-slate-400 text-base sm:text-lg">
          Paste any news article headline or full body text below to analyze linguistic signals, lexical frequencies, and ML classification probability.
        </p>
      </div>

      {/* Main Input Card */}
      <div className="bg-slate-900/80 rounded-2xl border border-slate-800 p-6 sm:p-8 shadow-xl backdrop-blur-sm space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <label className="text-sm font-semibold text-slate-200 flex items-center space-x-2">
            <span>📝</span>
            <span>Article Text Input</span>
          </label>
          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-400">Sample Presets:</span>
            <button
              onClick={() => setNewsText(SAMPLE_REAL)}
              className="text-xs px-2.5 py-1 rounded bg-slate-800 hover:bg-emerald-950 text-emerald-300 border border-emerald-800/50 transition-colors"
            >
              Real News Example
            </button>
            <button
              onClick={() => setNewsText(SAMPLE_FAKE)}
              className="text-xs px-2.5 py-1 rounded bg-slate-800 hover:bg-rose-950 text-rose-300 border border-rose-800/50 transition-colors"
            >
              Fake News Clickbait
            </button>
          </div>
        </div>

        {/* Text Area */}
        <div className="relative">
          <textarea
            rows={7}
            value={newsText}
            onChange={(e) => setNewsText(e.target.value)}
            placeholder="Paste news headline or full body article text here..."
            className="w-full bg-slate-950/80 text-slate-100 placeholder-slate-500 rounded-xl p-4 border border-slate-800 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30 outline-none text-sm transition-all resize-y"
          />
          <div className="absolute bottom-3 right-3 text-xs text-slate-500 font-mono">
            {wordCount} words | {newsText.length} chars
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center justify-between gap-4 pt-2">
          <button
            onClick={handleClear}
            disabled={loading || (!newsText && !result)}
            className="px-5 py-2.5 rounded-xl border border-slate-700 hover:bg-slate-800 text-slate-300 text-sm font-medium transition-all disabled:opacity-40 disabled:cursor-not-allowed"
          >
            🗑️ Clear Input
          </button>
          <button
            onClick={handleAnalyze}
            disabled={loading || !newsText.trim()}
            className="flex-1 sm:flex-initial px-8 py-3 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-bold text-sm shadow-lg shadow-indigo-600/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            {loading ? (
              <span>Analyzing Content...</span>
            ) : (
              <>
                <span>⚡ Analyze News Article</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Loading Animation */}
      {loading && (
        <div className="bg-slate-900/60 rounded-2xl border border-slate-800 p-8 shadow-xl backdrop-blur-sm">
          <LoadingSpinner label="Running NLP Preprocessing & ML Classification Model..." />
        </div>
      )}

      {/* Prediction Result Display */}
      {result && !loading && (
        <div
          className={`rounded-2xl border p-6 sm:p-8 shadow-2xl backdrop-blur-md transition-all ${
            isReal
              ? "bg-emerald-950/20 border-emerald-500/40 shadow-emerald-950/30"
              : "bg-rose-950/20 border-rose-500/40 shadow-rose-950/30"
          }`}
        >
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-slate-800/80">
            {/* Main Badge */}
            <div className="flex items-center space-x-4">
              <div
                className={`h-14 w-14 rounded-2xl flex items-center justify-center text-3xl shadow-lg ${
                  isReal
                    ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 shadow-emerald-500/20"
                    : "bg-rose-500/20 text-rose-400 border border-rose-500/30 shadow-rose-500/20"
                }`}
              >
                {isReal ? "✅" : "🚨"}
              </div>
              <div>
                <span className="text-xs uppercase tracking-wider font-semibold text-slate-400">
                  Model Prediction Output
                </span>
                <h2
                  className={`text-2xl sm:text-3xl font-extrabold ${
                    isReal ? "text-emerald-400" : "text-rose-400"
                  }`}
                >
                  {result.prediction}
                </h2>
              </div>
            </div>

            {/* Confidence Gauge */}
            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 min-w-[220px]">
              <div className="flex justify-between items-center text-xs mb-1">
                <span className="text-slate-400 font-medium">Model Confidence:</span>
                <span className="font-bold text-white font-mono">{result.confidence}%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-3 overflow-hidden p-0.5">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${
                    isReal ? "bg-gradient-to-r from-emerald-500 to-teal-400" : "bg-gradient-to-r from-rose-500 to-orange-400"
                  }`}
                  style={{ width: `${result.confidence}%` }}
                />
              </div>
              <div className="flex justify-between text-[10px] text-slate-500 mt-1 font-mono">
                <span>Fake: {result.probabilities?.fake || 0}%</span>
                <span>Real: {result.probabilities?.real || 0}%</span>
              </div>
            </div>
          </div>

          {/* Details & Signal Keywords */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-6">
            <div className="space-y-2">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Key Lexical Features / Signal Words
              </span>
              <div className="flex flex-wrap gap-2">
                {result.top_words && result.top_words.length > 0 ? (
                  result.top_words.map((w, idx) => (
                    <span
                      key={idx}
                      className="px-2.5 py-1 rounded-md bg-slate-800 text-indigo-300 text-xs font-mono border border-slate-700"
                    >
                      #{w}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-500">General text tokens</span>
                )}
              </div>
            </div>

            <div className="space-y-1">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Classification Timestamp
              </span>
              <p className="text-sm font-mono text-slate-300">{result.timestamp}</p>
            </div>
          </div>

          {/* Explanation Warning */}
          <div className="mt-6 p-4 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-slate-400 leading-relaxed flex items-start space-x-3">
            <span className="text-lg">ℹ️</span>
            <div>
              <p className="font-semibold text-slate-300 mb-0.5">Machine Learning Prediction Disclaimer</p>
              <p>{result.explanation}</p>
            </div>
          </div>
        </div>
      )}

      {/* Quick Navigation Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-4">
        <div
          onClick={() => setActivePage("dashboard")}
          className="bg-slate-900/60 border border-slate-800 hover:border-indigo-500/50 p-5 rounded-2xl cursor-pointer transition-all hover:scale-[1.02] group"
        >
          <span className="text-2xl mb-2 block">📊</span>
          <h3 className="text-white font-bold text-base group-hover:text-indigo-400">Analytics Dashboard</h3>
          <p className="text-slate-400 text-xs mt-1">View real vs fake pie breakdown, timeline line charts, and accuracy KPIs.</p>
        </div>

        <div
          onClick={() => setActivePage("history")}
          className="bg-slate-900/60 border border-slate-800 hover:border-indigo-500/50 p-5 rounded-2xl cursor-pointer transition-all hover:scale-[1.02] group"
        >
          <span className="text-2xl mb-2 block">📜</span>
          <h3 className="text-white font-bold text-base group-hover:text-indigo-400">Prediction History</h3>
          <p className="text-slate-400 text-xs mt-1">Browse, search, filter, and delete past checked news audit logs.</p>
        </div>

        <div
          onClick={() => setActivePage("dataset")}
          className="bg-slate-900/60 border border-slate-800 hover:border-indigo-500/50 p-5 rounded-2xl cursor-pointer transition-all hover:scale-[1.02] group"
        >
          <span className="text-2xl mb-2 block">📁</span>
          <h3 className="text-white font-bold text-base group-hover:text-indigo-400">Dataset Insights</h3>
          <p className="text-slate-400 text-xs mt-1">Explore training dataset counts, class distributions, and top word frequencies.</p>
        </div>
      </div>
    </div>
  );
}
