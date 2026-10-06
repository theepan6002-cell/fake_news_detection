import React, { useState, useEffect } from "react";
import { getPredictionHistory, deleteHistoryRecord, clearAllHistory } from "../services/api";
import LoadingSpinner from "../components/LoadingSpinner";

export default function History({ setToast }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("all");
  const [sort, setSort] = useState("newest");
  const [selectedRecord, setSelectedRecord] = useState(null);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const data = await getPredictionHistory(search, filter, sort);
      setHistory(data.history || []);
    } catch (err) {
      setToast({ type: "error", message: err.message || "Failed to load prediction history." });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [search, filter, sort]);

  const handleDeleteOne = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm("Are you sure you want to delete this record?")) return;
    try {
      await deleteHistoryRecord(id);
      setToast({ type: "success", message: "Record deleted successfully." });
      fetchHistory();
    } catch (err) {
      setToast({ type: "error", message: err.message || "Failed to delete record." });
    }
  };

  const handleClearAll = async () => {
    if (!window.confirm("Are you sure you want to clear ALL prediction history? This action cannot be undone.")) return;
    try {
      await clearAllHistory();
      setToast({ type: "success", message: "All history cleared." });
      fetchHistory();
    } catch (err) {
      setToast({ type: "error", message: err.message || "Failed to clear history." });
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white">Prediction History & Audit Log</h1>
          <p className="text-slate-400 text-sm mt-1">
            Search, filter, inspect, and manage past news classification records stored in SQLite.
          </p>
        </div>
        {history.length > 0 && (
          <button
            onClick={handleClearAll}
            className="px-4 py-2 bg-rose-950/60 hover:bg-rose-900 text-rose-300 border border-rose-800 rounded-xl text-xs font-semibold transition-all self-start sm:self-auto"
          >
            🗑️ Clear Entire History
          </button>
        )}
      </div>

      {/* Filters Bar */}
      <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-2xl flex flex-col md:flex-row gap-4 justify-between items-center">
        {/* Search Input */}
        <div className="relative w-full md:w-80">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search article text or keywords..."
            className="w-full bg-slate-950 text-slate-200 placeholder-slate-500 rounded-xl pl-9 pr-4 py-2 text-xs border border-slate-800 focus:border-indigo-500 outline-none"
          />
          <span className="absolute left-3 top-2.5 text-xs text-slate-500">🔍</span>
        </div>

        {/* Filter Pills & Sort */}
        <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
          <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800">
            {["all", "likely real", "likely fake"].map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-3 py-1 rounded-lg text-xs font-medium capitalize transition-all ${
                  filter === f
                    ? "bg-indigo-600 text-white font-semibold"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                {f}
              </button>
            ))}
          </div>

          <select
            value={sort}
            onChange={(e) => setSort(e.target.value)}
            className="bg-slate-950 text-slate-300 text-xs rounded-xl px-3 py-2 border border-slate-800 outline-none cursor-pointer"
          >
            <option value="newest">Sort: Newest First</option>
            <option value="oldest">Sort: Oldest First</option>
          </select>
        </div>
      </div>

      {/* Main Table / List */}
      {loading ? (
        <div className="bg-slate-900/60 rounded-2xl border border-slate-800 p-12">
          <LoadingSpinner label="Loading Prediction History Records..." />
        </div>
      ) : history.length > 0 ? (
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 uppercase font-mono border-b border-slate-800">
                <tr>
                  <th className="p-4">ID</th>
                  <th className="p-4">News Article Text Snippet</th>
                  <th className="p-4">Prediction</th>
                  <th className="p-4">Confidence</th>
                  <th className="p-4">Top Feature Signals</th>
                  <th className="p-4">Timestamp</th>
                  <th className="p-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-300 font-sans">
                {history.map((rec) => {
                  const isReal = rec.prediction === "Likely Real";
                  return (
                    <tr
                      key={rec.id}
                      onClick={() => setSelectedRecord(rec)}
                      className="hover:bg-slate-800/40 cursor-pointer transition-colors"
                    >
                      <td className="p-4 font-mono text-slate-500">#{rec.id}</td>
                      <td className="p-4 max-w-xs sm:max-w-md truncate font-medium text-slate-200">
                        {rec.news_text}
                      </td>
                      <td className="p-4">
                        <span
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${
                            isReal
                              ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
                              : "bg-rose-500/10 text-rose-400 border-rose-500/30"
                          }`}
                        >
                          {isReal ? "✅ Likely Real" : "🚨 Likely Fake"}
                        </span>
                      </td>
                      <td className="p-4 font-mono font-bold text-white">
                        {rec.confidence}%
                      </td>
                      <td className="p-4">
                        <div className="flex flex-wrap gap-1">
                          {rec.top_words && rec.top_words.length > 0 ? (
                            rec.top_words.slice(0, 3).map((w, idx) => (
                              <span
                                key={idx}
                                className="px-1.5 py-0.5 bg-slate-800 text-indigo-300 rounded text-[10px] font-mono"
                              >
                                {w}
                              </span>
                            ))
                          ) : (
                            <span className="text-[10px] text-slate-500">N/A</span>
                          )}
                        </div>
                      </td>
                      <td className="p-4 font-mono text-slate-400 text-[11px]">
                        {rec.timestamp}
                      </td>
                      <td className="p-4 text-right">
                        <button
                          onClick={(e) => handleDeleteOne(rec.id, e)}
                          className="px-2.5 py-1 bg-slate-800 hover:bg-rose-900 text-rose-300 rounded-lg text-[11px] border border-slate-700 transition-colors"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="bg-slate-900/60 rounded-2xl border border-slate-800 p-12 text-center space-y-3">
          <span className="text-4xl block">📜</span>
          <h3 className="text-lg font-bold text-white">No Prediction History Found</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto">
            Try adjusting your search criteria or analyze a news article on the Home page.
          </p>
        </div>
      )}

      {/* Expand Full Text Modal */}
      {selectedRecord && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div className="flex items-center space-x-2">
                <span className="font-mono text-xs text-slate-500">Record #{selectedRecord.id}</span>
                <span
                  className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
                    selectedRecord.prediction === "Likely Real"
                      ? "bg-emerald-500/20 text-emerald-400"
                      : "bg-rose-500/20 text-rose-400"
                  }`}
                >
                  {selectedRecord.prediction} ({selectedRecord.confidence}%)
                </span>
              </div>
              <button
                onClick={() => setSelectedRecord(null)}
                className="text-slate-400 hover:text-white font-bold text-xl"
              >
                &times;
              </button>
            </div>

            <div className="space-y-2">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Full News Text
              </span>
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 max-h-60 overflow-y-auto text-sm text-slate-200 leading-relaxed font-sans">
                {selectedRecord.news_text}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 text-xs">
              <div>
                <span className="text-slate-400 block mb-1">Top Word Signals:</span>
                <div className="flex flex-wrap gap-1">
                  {selectedRecord.top_words?.map((w, idx) => (
                    <span key={idx} className="px-2 py-0.5 bg-slate-800 text-indigo-300 rounded font-mono">
                      #{w}
                    </span>
                  ))}
                </div>
              </div>
              <div>
                <span className="text-slate-400 block mb-1">Timestamp:</span>
                <span className="font-mono text-slate-300">{selectedRecord.timestamp}</span>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setSelectedRecord(null)}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-bold"
              >
                Close View
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
