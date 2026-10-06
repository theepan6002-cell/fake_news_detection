import React, { useState, useEffect } from "react";
import { getModelPerformance } from "../services/api";
import LoadingSpinner from "../components/LoadingSpinner";

export default function ModelStats({ setToast }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchModelStats = async () => {
    setLoading(true);
    try {
      const res = await getModelPerformance();
      setData(res);
    } catch (err) {
      setToast({ type: "error", message: err.message || "Failed to load model specs." });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchModelStats();
  }, []);

  if (loading) {
    return (
      <div className="bg-slate-900/60 rounded-2xl border border-slate-800 p-12 my-8">
        <LoadingSpinner label="Fetching Machine Learning Pipeline & Comparative Metrics..." />
      </div>
    );
  }

  const pipeline = data?.pipeline || {};
  const comparison = data?.models_comparison || {};

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-extrabold text-white">ML Architecture & Model Performance</h1>
        <p className="text-slate-400 text-sm mt-1">
          Technical overview of data cleaning, TF-IDF vectorization, algorithm training, and comparative evaluation.
        </p>
      </div>

      {/* Selected Model Banner */}
      <div className="bg-gradient-to-r from-indigo-950 via-purple-950 to-slate-900 border border-indigo-500/30 p-6 rounded-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center space-x-4">
          <div className="h-12 w-12 rounded-xl bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center text-2xl">
            🏆
          </div>
          <div>
            <span className="text-xs uppercase font-semibold text-indigo-300 tracking-wider">
              Selected Best Performing Classifier
            </span>
            <h2 className="text-2xl font-extrabold text-white">{data?.best_model || "Logistic Regression"}</h2>
          </div>
        </div>
        <div className="flex items-center space-x-2 bg-slate-950/60 px-4 py-2 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-400">Optimization Goal:</span>
          <span className="text-xs font-bold font-mono text-emerald-400">Maximized Test F1 Score</span>
        </div>
      </div>

      {/* Pipeline Breakdown Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Step 1: Preprocessing */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-3">
          <div className="flex items-center space-x-3">
            <span className="h-8 w-8 rounded-lg bg-indigo-500/20 text-indigo-300 font-bold flex items-center justify-center text-sm">
              1
            </span>
            <h3 className="text-base font-bold text-white">Text Preprocessing</h3>
          </div>
          <ul className="space-y-1.5 text-xs text-slate-300">
            {pipeline.text_preprocessing?.map((step, idx) => (
              <li key={idx} className="flex items-center space-x-2">
                <span className="text-emerald-400">✓</span>
                <span>{step}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Step 2: Feature Extraction */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-3">
          <div className="flex items-center space-x-3">
            <span className="h-8 w-8 rounded-lg bg-indigo-500/20 text-indigo-300 font-bold flex items-center justify-center text-sm">
              2
            </span>
            <h3 className="text-base font-bold text-white">TF-IDF Vectorization</h3>
          </div>
          <div className="space-y-2 text-xs text-slate-300 font-mono">
            <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
              <span className="text-slate-400 block text-[10px]">Method:</span>
              <span className="text-indigo-300 font-bold">{pipeline.feature_extraction?.method}</span>
            </div>
            <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
              <span className="text-slate-400 block text-[10px]">N-Gram Range:</span>
              <span className="text-white font-bold">{pipeline.feature_extraction?.ngram_range}</span>
            </div>
            <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
              <span className="text-slate-400 block text-[10px]">Max Vocabulary:</span>
              <span className="text-white font-bold">{pipeline.feature_extraction?.max_features} top features</span>
            </div>
          </div>
        </div>

        {/* Step 3: Model Training */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-3">
          <div className="flex items-center space-x-3">
            <span className="h-8 w-8 rounded-lg bg-indigo-500/20 text-indigo-300 font-bold flex items-center justify-center text-sm">
              3
            </span>
            <h3 className="text-base font-bold text-white">Trained Algorithms</h3>
          </div>
          <div className="space-y-2 text-xs">
            {pipeline.algorithms_trained?.map((alg, idx) => (
              <div key={idx} className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
                <span className="font-bold text-white block">{alg.name}</span>
                <span className="text-[10px] text-slate-400">{alg.type}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Model Performance Matrix Table */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
        <h3 className="text-base font-bold text-white flex items-center space-x-2">
          <span>📊</span>
          <span>Comparative Model Evaluation Metrics</span>
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950 text-slate-400 uppercase font-mono border-b border-slate-800">
              <tr>
                <th className="p-4">Algorithm</th>
                <th className="p-4">Accuracy</th>
                <th className="p-4">Precision</th>
                <th className="p-4">Recall</th>
                <th className="p-4">F1-Score</th>
                <th className="p-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono text-slate-300">
              {Object.entries(comparison).map(([key, m]) => {
                const isSelected = m.model_name === data?.best_model;
                return (
                  <tr key={key} className={isSelected ? "bg-indigo-950/30" : "hover:bg-slate-800/40"}>
                    <td className="p-4 font-sans font-bold text-white flex items-center space-x-2">
                      <span>{isSelected ? "⭐" : "🔹"}</span>
                      <span>{m.model_name}</span>
                    </td>
                    <td className="p-4 text-cyan-400 font-bold">{(m.accuracy * 100).toFixed(2)}%</td>
                    <td className="p-4 text-purple-400 font-bold">{(m.precision * 100).toFixed(2)}%</td>
                    <td className="p-4 text-amber-400 font-bold">{(m.recall * 100).toFixed(2)}%</td>
                    <td className="p-4 text-emerald-400 font-bold">{(m.f1_score).toFixed(4)}</td>
                    <td className="p-4 font-sans">
                      <span
                        className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                          isSelected
                            ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                            : "bg-slate-800 text-slate-400"
                        }`}
                      >
                        {isSelected ? "Deploy Model" : "Evaluated"}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
