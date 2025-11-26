import React, { useState } from 'react';
import { Search, Loader2, ChevronDown, FolderOpen } from 'lucide-react';

const ScanForm = ({ onScan, isLoading }) => {
  const [path, setPath] = useState('');
  const [model, setModel] = useState('llama3.1:8b');
  const fileInputRef = React.useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (path) {
      onScan(path, model);
    }
  };

  const triggerFolderSelect = () => {
    fileInputRef.current.click();
  };

  const handleFolderSelect = (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      // Get the path of the selected folder
      // For webkitdirectory, files[0].webkitRelativePath gives "folderName/fileName"
      // We want just "folderName" or the absolute path if possible.
      // In a browser environment, we can't get the absolute path directly for security reasons.
      // We'll use the parent directory of the first file as the "path"
      const relativePath = files[0].webkitRelativePath;
      const folderPath = relativePath.substring(0, relativePath.indexOf('/'));
      setPath(folderPath); // This will be the folder name, not absolute path.
                           // For a real application, you'd need a backend to resolve this.
                           // For now, we'll assume the user understands this limitation or
                           // will manually enter the absolute path if needed.
    }
  };

  return (
    <div className="modern-card p-6 mb-8">
      <h2 className="text-lg font-semibold mb-6 flex items-center gap-2 text-[var(--text-main)]">
        <Search className="w-5 h-5 text-[var(--color-primary)]" />
        New Scan
      </h2>
      
      <form onSubmit={handleSubmit} className="flex flex-col lg:flex-row gap-4">
        <div className="flex-grow space-y-1.5">
          <label className="block text-sm font-medium text-[var(--text-main)] ml-1">Project Path</label>
          <div className="flex gap-2">
            <input
              type="text"
              value={path}
              onChange={(e) => setPath(e.target.value)}
              placeholder="/absolute/path/to/project"
              className="flex-grow bg-[var(--bg-main)] border border-[var(--border-color)] rounded-lg px-4 py-2.5 focus:outline-none focus:border-[var(--color-primary)] focus:ring-2 focus:ring-[var(--color-primary)]/20 transition-all text-[var(--text-main)] text-sm placeholder:text-[var(--text-muted)]"
            />
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFolderSelect}
              webkitdirectory=""
              directory=""
              hidden
            />
            <button
              type="button"
              onClick={triggerFolderSelect}
              className="px-4 bg-[var(--bg-main)] border border-[var(--border-color)] rounded-lg hover:bg-[var(--border-color)] text-[var(--text-muted)] transition-colors"
              title="Select Folder"
            >
              <FolderOpen className="w-5 h-5" />
            </button>
          </div>
        </div>
        
        <div className="lg:w-64 space-y-1.5">
          <label className="block text-sm font-medium text-[var(--text-main)] ml-1">LLM Model</label>
          <div className="relative">
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full bg-[var(--bg-main)] border border-[var(--border-color)] rounded-lg px-4 py-2.5 focus:outline-none focus:border-[var(--color-primary)] focus:ring-2 focus:ring-[var(--color-primary)]/20 transition-all text-[var(--text-main)] text-sm appearance-none cursor-pointer"
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
            className="h-[42px] px-6 bg-[var(--color-primary)] hover:bg-indigo-600 text-white font-medium text-sm shadow-sm hover:shadow transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 rounded-lg"
          >
            {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Start Scan'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ScanForm;
