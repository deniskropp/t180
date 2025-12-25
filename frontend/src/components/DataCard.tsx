import React, { useState } from 'react';
import type { ClipboardEntry } from '../types';
import { PrismLight as SyntaxHighlighter } from 'react-syntax-highlighter';
import tsx from 'react-syntax-highlighter/dist/esm/languages/prism/tsx';
import typescript from 'react-syntax-highlighter/dist/esm/languages/prism/typescript';
import javascript from 'react-syntax-highlighter/dist/esm/languages/prism/javascript';
import python from 'react-syntax-highlighter/dist/esm/languages/prism/python';
import json from 'react-syntax-highlighter/dist/esm/languages/prism/json';
import sql from 'react-syntax-highlighter/dist/esm/languages/prism/sql';
import css from 'react-syntax-highlighter/dist/esm/languages/prism/css';
import bash from 'react-syntax-highlighter/dist/esm/languages/prism/bash';
import markdown from 'react-syntax-highlighter/dist/esm/languages/prism/markdown';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Download, Copy, ZoomIn, ZoomOut, Check } from 'lucide-react';

// Register languages
SyntaxHighlighter.registerLanguage('tsx', tsx);
SyntaxHighlighter.registerLanguage('typescript', typescript);
SyntaxHighlighter.registerLanguage('javascript', javascript);
SyntaxHighlighter.registerLanguage('python', python);
SyntaxHighlighter.registerLanguage('json', json);
SyntaxHighlighter.registerLanguage('sql', sql);
SyntaxHighlighter.registerLanguage('css', css);
SyntaxHighlighter.registerLanguage('bash', bash);
SyntaxHighlighter.registerLanguage('markdown', markdown);

interface DataCardProps {
  entry: ClipboardEntry;
  onToggleStar: (uuid: string) => void;
}

const getLanguageFromMime = (mimetypes: string): string => {
  const mime = mimetypes.split(',')[0].toLowerCase();
  
  const map: Record<string, string> = {
    'application/json': 'json',
    'text/x-python': 'python',
    'application/x-python-code': 'python',
    'text/javascript': 'javascript',
    'application/javascript': 'javascript',
    'text/typescript': 'typescript',
    'application/typescript': 'typescript',
    'text/css': 'css',
    'text/sql': 'sql',
    'application/sql': 'sql',
    'text/html': 'html',
    'text/markdown': 'markdown',
    'text/x-sh': 'bash',
    'text/plain': 'text'
  };

  // Check for exact matches
  if (map[mime]) return map[mime];
  
  // Heuristics
  if (mime.includes('json')) return 'json';
  if (mime.includes('sql')) return 'sql';
  if (mime.includes('python')) return 'python';
  
  return 'text';
};

const getExtensionFromMime = (mimetype: string): string => {
   const mime = mimetype.split(',')[0].toLowerCase();
   const map: Record<string, string> = {
    'application/json': 'json',
    'text/x-python': 'py',
    'application/x-python-code': 'py',
    'text/javascript': 'js',
    'text/typescript': 'ts',
    'text/css': 'css',
    'text/sql': 'sql',
    'text/html': 'html',
    'text/markdown': 'md',
    'text/x-sh': 'sh',
    'text/plain': 'txt'
  };
  return map[mime] || 'txt';
}

export const DataCard: React.FC<DataCardProps> = ({ entry, onToggleStar }) => {
  const [fontSize, setFontSize] = useState(14);
  const [copied, setCopied] = useState(false);

  const date = new Date(entry.added_time * 1000).toLocaleString();
  const language = getLanguageFromMime(entry.mimetypes);
  const ext = getExtensionFromMime(entry.mimetypes);

  const handleCopy = async () => {
    if (entry.text) {
      await navigator.clipboard.writeText(entry.text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleDownload = () => {
    if (!entry.text) return;
    
    const blob = new Blob([entry.text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `snippet-${entry.uuid.substring(0, 8)}.${ext}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="data-card">
      <div className="dc-header">
        <div className="dc-header-left">
           <span className="dc-type-badge">{language.toUpperCase()}</span>
           <span className="dc-mime-info">{entry.mimetypes.split(',')[0]}</span>
        </div>
        
        <div className="dc-controls">
          <div className="dc-control-group">
            <button 
              className="dc-icon-btn" 
              onClick={() => setFontSize(s => Math.max(10, s - 1))}
              title="Decrease Font Size"
            >
              <ZoomOut size={16} />
            </button>
            <span className="dc-font-size-label">{fontSize}px</span>
            <button 
              className="dc-icon-btn" 
              onClick={() => setFontSize(s => Math.min(24, s + 1))}
              title="Increase Font Size"
            >
              <ZoomIn size={16} />
            </button>
          </div>

          <div className="dc-control-divider" />

          <button 
             className="dc-icon-btn" 
             onClick={handleCopy}
             title="Copy to Clipboard"
          >
            {copied ? <Check size={16} color="var(--color-success)"/> : <Copy size={16} />}
          </button>

          <button 
             className="dc-icon-btn" 
             onClick={handleDownload}
             title="Download"
          >
            <Download size={16} />
          </button>

          <div className="dc-control-divider" />

          <button 
            className={`dc-star-btn ${entry.starred ? 'starred' : ''}`}
            onClick={() => onToggleStar(entry.uuid)}
            aria-label={entry.starred ? "Unstar" : "Star"}
            title={entry.starred ? "Unstar" : "Star"}
          >
            ★
          </button>
        </div>
      </div>
      
      <div className="dc-content-wrapper">
         <SyntaxHighlighter 
            language={language} 
            style={vscDarkPlus}
            customStyle={{ 
                margin: 0, 
                borderRadius: 0,
                fontSize: `${fontSize}px`,
                backgroundColor: 'transparent',
                padding: '1rem',
                minHeight: '100px'
            }}
            wrapLines={true}
            wrapLongLines={true}
         >
          {entry.text || '(No text content)'}
        </SyntaxHighlighter>
      </div>
      
      <div className="dc-footer">
        <span className="dc-uuid" title={entry.uuid}>
          ID: {entry.uuid.substring(0, 8)}...
        </span>
        <span title={`Added: ${date}`}>
          {new Date(entry.added_time * 1000).toLocaleString()}
        </span>
      </div>
    </div>
  );
};
