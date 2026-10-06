import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import Toast from "./components/Toast";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import Dataset from "./pages/Dataset";
import ModelStats from "./pages/ModelStats";

export default function App() {
  const [activePage, setActivePage] = useState("home");
  const [serverOnline, setServerOnline] = useState(false);
  const [toast, setToast] = useState(null);

  // Ping API server status on mount
  useEffect(() => {
    const checkServer = async () => {
      try {
        const res = await fetch("http://127.0.0.1:5000/");
        if (res.ok) setServerOnline(true);
      } catch (err) {
        setServerOnline(false);
      }
    };
    checkServer();
    const interval = setInterval(checkServer, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans antialiased flex flex-col selection:bg-indigo-500 selection:text-white">
      {/* Top Navbar Header */}
      <Navbar activePage={activePage} setActivePage={setActivePage} serverOnline={serverOnline} />

      {/* Main Page Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        {activePage === "home" && <Home setActivePage={setActivePage} setToast={setToast} />}
        {activePage === "dashboard" && <Dashboard setToast={setToast} />}
        {activePage === "history" && <History setToast={setToast} />}
        {activePage === "dataset" && <Dataset setToast={setToast} />}
        {activePage === "model" && <ModelStats setToast={setToast} />}
      </main>

      {/* Alert Toast Notification */}
      <Toast toast={toast} onClose={() => setToast(null)} />

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950/80 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>🛡️ VeriTruth AI - Powered by Scikit-learn, TF-IDF Vectorization & Flask</span>
          <span>Academic Data Science & Machine Learning Capstone</span>
        </div>
      </footer>
    </div>
  );
}
