import React, { useState } from 'react';
import axios from 'axios';
import { Shield, Sun, Moon } from 'lucide-react';
import ScanForm from './components/ScanForm';
import Dashboard from './components/Dashboard';
import VulnerabilityList from './components/VulnerabilityList';
import History from './components/History';
import { useTheme } from './context/ThemeContext';

import LandingPage from './components/LandingPage';

function App() {
  const [showLanding, setShowLanding] = useState(true);
  const [showHistory, setShowHistory] = useState(false);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const { theme, toggleTheme } = useTheme();

  const handleScan = async (path, model) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('/api/scan', {
        path,
        model
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to connect to scanner API');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[var(--bg-main)] text-[var(--text-main)] p-4 md:p-8 transition-colors duration-300">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="mb-10 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-[var(--color-primary)] p-2 rounded-lg">
              <Shield className="w-6 h-6 text-[var(--text-on-primary)]" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-[var(--text-main)] tracking-tight">
                Vulnora AI <span className="text-[var(--text-muted)] font-normal">— See the Unseen</span>
              </h1>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={() => {
                setShowHistory(false);
                setShowLanding(false);
                setResult(null);
              }}
              className={`text-sm font-medium transition-colors ${!showHistory && !showLanding ? 'text-[var(--text-main)] underline underline-offset-4' : 'text-[var(--text-muted)] hover:text-[var(--text-main)]'}`}
            >
              New Scan
            </button>
            <button
              onClick={() => {
                setShowHistory(true);
                setShowLanding(false);
              }}
              className={`text-sm font-medium transition-colors ${showHistory ? 'text-[var(--text-main)] underline underline-offset-4' : 'text-[var(--text-muted)] hover:text-[var(--text-main)]'}`}
            >
              History
            </button>
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg text-[var(--text-muted)] hover:bg-[var(--border-color)] transition-colors"
            >
              {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
          </div>
        </header>

        {/* Main Content */}
        <main>
          {showLanding ? (
            <LandingPage onStart={() => setShowLanding(false)} />
          ) : showHistory ? (
            <History onLoadScan={(scanData) => {
              setResult(scanData);
              setShowHistory(false);
            }} />
          ) : (
            <div className="animate-in fade-in slide-in-from-bottom-8 duration-500">
              <ScanForm
                onScan={handleScan}
                isLoading={isLoading}
                initialPath={result?.project_path}
              />

              {error && (
                <div className="bg-red-500/10 border border-red-500/50 text-red-400 p-4 rounded-lg mb-8">
                  {error}
                </div>
              )}

              {result && (
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 space-y-8">
                  <Dashboard result={result} />
                  <VulnerabilityList issues={result.issues} />
                </div>
              )}
            </div>
          )}
        </main>
      </div >
    </div >
  );
}

export default App;
