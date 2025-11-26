import React, { useState } from 'react';
import { Search, Loader2, ChevronDown } from 'lucide-react';

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
    <div className="tech-card p-8 rounded-lg mb-8">
      <h2 className="text-lg font-bold mb-6 flex items-center gap-3 text-[var(--text-main)] uppercase tracking-wide">
        <Search className="w-5 h-5 text-[var(--color-primary)]" />
        New Scan Configuration
      </h2>
      
      <form onSubmit={handleSubmit} className="flex flex-col lg:flex-row gap-6">
        <div className="flex-grow space-y-2">
          <label className="block text-xs font-bold text-[var(--text-muted)] ml-1 uppercase tracking-wider">Project Path</label>
          <div className="flex gap-2">
            <input
              type="text"
              value={path}
              onChange={(e) => setPath(e.target.value)}
              placeholder="/absolute/path/to/project"
              className="flex-grow bg-[var(--bg-main)] border border-[var(--border-color)] rounded-none px-4 py-3 focus:outline-none focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition-all text-[var(--text-main)] font-mono text-sm placeholder:text-[var(--text-muted)]/50"
            />
          </div>
        </div>
        
        <div className="lg:w-72 space-y-2">
          <label className="block text-xs font-bold text-[var(--text-muted)] ml-1 uppercase tracking-wider">LLM Model</label>
          <div className="relative">
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full bg-[var(--bg-main)] border border-[var(--border-color)] rounded-none px-4 py-3 focus:outline-none focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition-all text-[var(--text-main)] font-mono text-sm appearance-none cursor-pointer"
            >
              <option value="llama3.1:8b">llama3.1:8b</option>
              <option value="llama3">llama3</option>
              <option value="mistral">mistral</option>
            </select>
            <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-[var(--text-muted)]">
              <ChevronDown className="w-4 h-4" />
            </div>
          </div>
        </div>
        
        <div className="flex items-end">
          <button
            type="submit"
            disabled={isLoading || !path}
            className="h-[46px] px-8 bg-[var(--color-primary)] hover:bg-blue-700 text-white font-bold text-sm uppercase tracking-wider shadow-sm hover:shadow-md transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 rounded-sm"
          >
            {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Initialize Scan'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ScanForm;
