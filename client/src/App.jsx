import React, { useState } from 'react';
import axios from 'axios';
import { Shield } from 'lucide-react';
import ScanForm from './components/ScanForm';
import Dashboard from './components/Dashboard';
import VulnerabilityList from './components/VulnerabilityList';

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleScan = async (path, model) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      // Use relative path, Vite proxy will handle the rest
      const response = await axios.post('/api/scan', {
        path,
        model
      });
      setResult(response.data);
      console.log(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to connect to scanner API');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-darker text-slate-200 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="mb-10 flex items-center gap-3 border-b border-slate-800 pb-6">
          <div className="bg-gradient-to-br from-primary to-secondary p-3 rounded-xl shadow-lg shadow-primary/20">
            <Shield className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
              Vulnora AI
            </h1>
            <p className="text-slate-400">Advanced Multi-Language Security Scanner</p>
          </div>
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
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
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
