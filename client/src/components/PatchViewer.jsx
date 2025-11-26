import React from 'react';
import { DiffEditor } from '@monaco-editor/react';
import { useTheme } from '../context/ThemeContext';

const PatchViewer = ({ originalCode, patchedCode, language = 'python' }) => {
  const { theme } = useTheme();

  return (
    <div className="h-[400px] w-full border border-[var(--border-color)] rounded-lg overflow-hidden">
      <DiffEditor
        height="100%"
        original={originalCode}
        modified={patchedCode}
        language={language}
        theme={theme === 'dark' ? 'vs-dark' : 'light'}
        options={{
          readOnly: true,
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          fontSize: 14,
          renderSideBySide: true,
        }}
      />
    </div>
  );
};

export default PatchViewer;
