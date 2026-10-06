import React from "react";

export default function Navbar({ activePage, setActivePage, serverOnline }) {
  const navItems = [
    { id: "home", label: "Detector", icon: "⚡" },
    { id: "dashboard", label: "Analytics Dashboard", icon: "📊" },
    { id: "history", label: "Prediction History", icon: "📜" },
    { id: "dataset", label: "Dataset Insights", icon: "📁" },
    { id: "model", label: "ML Pipeline & Stats", icon: "🤖" }
  ];

  return (
    <header className="sticky top-0 z-40 bg-slate-900/90 backdrop-blur-md border-b border-slate-800 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Title */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActivePage("home")}>
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 p-0.5 shadow-indigo-500/30 shadow-lg flex items-center justify-center">
              <div className="h-full w-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                <span className="text-xl">🛡️</span>
              </div>
            </div>
            <div>
              <span className="text-lg font-bold bg-gradient-to-r from-white via-indigo-100 to-indigo-400 bg-clip-text text-transparent">
                VeriTruth AI
              </span>
              <span className="hidden sm:inline-block ml-2 text-xs font-semibold px-2 py-0.5 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-full">
                Fake News Analytics
              </span>
            </div>
          </div>

          {/* Desktop Navigation Tabs */}
          <nav className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const isActive = activePage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActivePage(item.id)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? "bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 shadow-inner"
                      : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                  }`}
                >
                  <span>{item.icon}</span>
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Backend Status Indicator */}
          <div className="flex items-center space-x-2">
            <div className={`h-2.5 w-2.5 rounded-full ${serverOnline ? "bg-emerald-500 animate-pulse shadow-emerald-500/50 shadow-sm" : "bg-rose-500"}`} />
            <span className="text-xs text-slate-400 font-mono hidden sm:inline">
              {serverOnline ? "API Online :5000" : "API Connecting..."}
            </span>
          </div>
        </div>
      </div>

      {/* Mobile Tab Strip */}
      <div className="md:hidden flex overflow-x-auto px-2 py-1.5 border-t border-slate-800/80 bg-slate-950/60 space-x-1 scrollbar-none">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setActivePage(item.id)}
            className={`whitespace-nowrap px-3 py-1.5 rounded-md text-xs font-medium ${
              activePage === item.id
                ? "bg-indigo-600 text-white font-semibold"
                : "text-slate-400 hover:text-white"
            }`}
          >
            {item.icon} {item.label}
          </button>
        ))}
      </div>
    </header>
  );
}
