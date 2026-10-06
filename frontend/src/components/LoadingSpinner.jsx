import React from "react";

export default function LoadingSpinner({ label = "Analyzing news content..." }) {
  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-4">
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 rounded-full border-4 border-indigo-500/20 animate-ping" />
        <div className="absolute inset-0 rounded-full border-4 border-t-indigo-500 border-r-purple-500 border-b-pink-500 border-l-transparent animate-spin" />
      </div>
      <div className="text-center">
        <p className="text-sm font-semibold text-indigo-300 animate-pulse">{label}</p>
        <p className="text-xs text-slate-400 mt-1">Cleaning text, vectorizing TF-IDF n-grams & querying ML models...</p>
      </div>
    </div>
  );
}
