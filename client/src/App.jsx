import React, { useState } from 'react';
import axios from 'axios';
import { Shield, Sun, Moon } from 'lucide-react';
import ScanForm from './components/ScanForm';
import Dashboard from './components/Dashboard';
import VulnerabilityList from './components/VulnerabilityList';
import { useTheme } from './context/ThemeContext';

function App() {
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
        <header className="mb-8 flex items-center justify-between border-b border-[var(--border-color)] pb-6">
          <div className="flex items-center gap-4">
            <div className="bg-[var(--color-primary)] p-2 rounded-lg shadow-lg shadow-blue-500/20">
              <Shield className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-[var(--text-main)] uppercase">
                Vulnora AI
              </h1>
              <p className="text-[var(--text-muted)] text-xs font-mono tracking-wider">SECURE CODE ANALYSIS SYSTEM</p>
            </div>
          </div>
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg border border-[var(--border-color)] hover:bg-[var(--border-color)] transition-colors"
          >
            {theme === 'dark' ? <Sun className="w-5 h-5 text-yellow-400" /> : <Moon className="w-5 h-5 text-slate-600" />}
          </button>
        </header>

        {/* Main Content */}
        <main>
          <ScanForm onScan={handleScan} isLoading={isLoading} />

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
        </main>
      </div>
    </div>
  );
}

export default App;
