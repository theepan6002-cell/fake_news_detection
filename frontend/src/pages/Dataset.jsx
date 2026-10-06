import React, { useState, useEffect } from "react";
import { getDatasetStats } from "../services/api";
import LoadingSpinner from "../components/LoadingSpinner";

export default function Dataset({ setToast }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchPreview, setSearchPreview] = useState("");

  const fetchStats = async () => {
    setLoading(true);
    try {
      const data = await getDatasetStats();
      setStats(data);
    } catch (err) {
      setToast({ type: "error", message: err.message || "Failed to load dataset insights." });
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
        <LoadingSpinner label="Calculating Dynamic Dataset Statistics & Frequent Word Tokens..." />
      </div>
    );
  }

  const samplePreview = stats?.sample_preview || [];
  const filteredPreview = samplePreview.filter(
    (item) =>
      item.title?.toLowerCase().includes(searchPreview.toLowerCase()) ||
      item.text?.toLowerCase().includes(searchPreview.toLowerCase())
  );

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-extrabold text-white">Dataset Analytics & Exploratory Data Analysis</h1>
        <p className="text-slate-400 text-sm mt-1">
          Dynamic statistics computed directly from the uploaded merged training dataset.
        </p>
      </div>

      {/* Overview KPI Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-xs text-slate-400 font-medium">Total Records</span>
          <p className="text-2xl font-black text-white font-mono">{stats?.total_records || 0}</p>
          <span className="text-[10px] text-slate-500">Merged CSV</span>
        </div>

        <div className="bg-emerald-950/20 border border-emerald-500/30 p-4 rounded-xl space-y-1">
          <span className="text-xs text-emerald-400 font-medium">Real News Count</span>
          <p className="text-2xl font-black text-emerald-300 font-mono">{stats?.real_count || 0}</p>
          <span className="text-[10px] text-emerald-400">{stats?.real_percentage}% balance</span>
        </div>

        <div className="bg-rose-950/20 border border-rose-500/30 p-4 rounded-xl space-y-1">
          <span className="text-xs text-rose-400 font-medium">Fake News Count</span>
          <p className="text-2xl font-black text-rose-300 font-mono">{stats?.fake_count || 0}</p>
          <span className="text-[10px] text-rose-400">{stats?.fake_percentage}% balance</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-xs text-slate-400 font-medium">Missing Values</span>
          <p className="text-2xl font-black text-amber-400 font-mono">{stats?.missing_records || 0}</p>
          <span className="text-[10px] text-slate-500">Filtered out</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-xs text-slate-400 font-medium">Duplicate Records</span>
          <p className="text-2xl font-black text-orange-400 font-mono">{stats?.duplicate_records || 0}</p>
          <span className="text-[10px] text-slate-500">Removed</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-xs text-slate-400 font-medium">Class Ratio</span>
          <p className="text-2xl font-black text-purple-400 font-mono">1 : 1.02</p>
          <span className="text-[10px] text-emerald-400">Balanced Set</span>
        </div>
      </div>

      {/* Dataset Distribution & Top Word Frequency Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Class Balance Visual Bar */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4">
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <span>⚖️</span>
            <span>Class Balance Distribution</span>
          </h3>

          <div className="space-y-4 pt-2">
            <div>
              <div className="flex justify-between text-xs font-semibold mb-1">
                <span className="text-emerald-400">Likely Real News: {stats?.real_count} articles</span>
                <span className="text-white font-mono">{stats?.real_percentage}%</span>
              </div>
              <div className="w-full bg-slate-950 rounded-full h-4 overflow-hidden border border-slate-800 p-0.5">
                <div
                  className="bg-emerald-500 h-full rounded-full transition-all duration-700"
                  style={{ width: `${stats?.real_percentage}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold mb-1">
                <span className="text-rose-400">Likely Fake News: {stats?.fake_count} articles</span>
                <span className="text-white font-mono">{stats?.fake_percentage}%</span>
              </div>
              <div className="w-full bg-slate-950 rounded-full h-4 overflow-hidden border border-slate-800 p-0.5">
                <div
                  className="bg-rose-500 h-full rounded-full transition-all duration-700"
                  style={{ width: `${stats?.fake_percentage}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Top 15 Word Frequencies */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4">
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <span>🔤</span>
            <span>Top Frequent Token Frequencies</span>
          </h3>

          <div className="flex flex-wrap gap-2 pt-2">
            {stats?.top_words?.map((item, idx) => (
              <div
                key={idx}
                className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono"
              >
                <span className="text-indigo-300">#{item.word}</span>
                <span className="px-1.5 py-0.5 bg-slate-800 text-slate-400 rounded-md text-[10px]">
                  {item.count}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Dataset Sample Preview Table */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <span>👁️</span>
            <span>Dataset Preview (Sample Records)</span>
          </h3>
          <input
            type="text"
            value={searchPreview}
            onChange={(e) => setSearchPreview(e.target.value)}
            placeholder="Search preview records..."
            className="bg-slate-950 text-slate-200 placeholder-slate-500 rounded-xl px-3 py-1.5 text-xs border border-slate-800 outline-none w-full sm:w-64"
          />
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950 text-slate-400 uppercase font-mono border-b border-slate-800">
              <tr>
                <th className="p-3">Title</th>
                <th className="p-3">Text Snippet</th>
                <th className="p-3">Subject</th>
                <th className="p-3">Label</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300 font-sans">
              {filteredPreview.length > 0 ? (
                filteredPreview.slice(0, 15).map((row, idx) => {
                  const isReal = parseInt(row.label) === 1;
                  return (
                    <tr key={idx} className="hover:bg-slate-800/40">
                      <td className="p-3 font-semibold text-white max-w-xs truncate">{row.title}</td>
                      <td className="p-3 max-w-md truncate text-slate-400">{row.text || row.cleaned_content}</td>
                      <td className="p-3 font-mono text-slate-400 capitalize">{row.subject || "general"}</td>
                      <td className="p-3">
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            isReal ? "bg-emerald-500/20 text-emerald-400" : "bg-rose-500/20 text-rose-400"
                          }`}
                        >
                          {isReal ? "Likely Real" : "Likely Fake"}
                        </span>
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan={4} className="p-4 text-center text-slate-500">
                    No preview records match your search query.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
