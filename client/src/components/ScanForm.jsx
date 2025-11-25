import React, { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';

const ScanForm = ({ onScan, isLoading }) => {
  const [path, setPath] = useState('');
  const [model, setModel] = useState('llama3.1:8b');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (path) {
      onScan(path, model);
    }
  };

  return (
    <div className="bg-card p-6 rounded-xl shadow-lg border border-slate-700 mb-8">
      <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
        <Search className="w-5 h-5 text-primary" />
        Start New Scan
      </h2>
      <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-4">
        <div className="flex-grow">
          <label className="block text-sm text-slate-400 mb-1">Project Path</label>
          <input
            type="text"
            value={path}
            onChange={(e) => setPath(e.target.value)}
            placeholder="/absolute/path/to/project"
            className="w-full bg-dark border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-primary transition-colors"
          />
        </div>
        <div className="md:w-64">
          <label className="block text-sm text-slate-400 mb-1">LLM Model</label>
          <select
            value={model}
            onChange={(e) => setModel(e.target.value)}
            className="w-full bg-dark border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-primary transition-colors"
          >
            <option value="llama3.1:8b">llama3.1:8b</option>
            <option value="llama3">llama3</option>
            <option value="mistral">mistral</option>
          </select>
        </div>
        <div className="flex items-end">
          <button
            type="submit"
            disabled={isLoading || !path}
            className="bg-gradient-to-r from-primary to-secondary hover:opacity-90 text-white font-medium py-2 px-6 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Scan Now'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ScanForm;
