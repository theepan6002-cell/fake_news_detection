import React from "react";

export default function Toast({ toast, onClose }) {
  if (!toast) return null;

  const isError = toast.type === "error";

  return (
    <div className="fixed bottom-5 right-5 z-50 animate-bounce-in max-w-md shadow-2xl">
      <div
        className={`flex items-start justify-between p-4 rounded-xl border backdrop-blur-md ${
          isError
            ? "bg-rose-950/90 text-rose-200 border-rose-800/80 shadow-rose-950/50"
            : "bg-emerald-950/90 text-emerald-200 border-emerald-800/80 shadow-emerald-950/50"
        }`}
      >
        <div className="flex items-center space-x-3">
          <span className="text-xl">{isError ? "⚠️" : "✅"}</span>
          <p className="text-sm font-medium">{toast.message}</p>
        </div>
        <button
          onClick={onClose}
          className="ml-4 text-slate-400 hover:text-white font-bold text-lg leading-none"
        >
          &times;
        </button>
      </div>
    </div>
  );
}
