import React from 'react';
import type { ClipboardEntry } from '../types';

interface DataCardProps {
  entry: ClipboardEntry;
  onToggleStar: (uuid: string) => void;
}

export const DataCard: React.FC<DataCardProps> = ({ entry, onToggleStar }) => {
  const date = new Date(entry.added_time * 1000).toLocaleString();
  
  return (
    <div className="data-card">
      <div className="dc-header">
        <span className="dc-type-badge">{entry.mimetypes.split(',')[0]}</span>
        <button 
          className={`dc-star-btn ${entry.starred ? 'starred' : ''}`}
          onClick={() => onToggleStar(entry.uuid)}
          aria-label={entry.starred ? "Unstar" : "Star"}
        >
          ★
        </button>
      </div>
      
      <div className="dc-content">
        {entry.text || '(No text content)'}
      </div>
      
      <div className="dc-footer">
        <span className="dc-uuid" title={entry.uuid}>
          {entry.uuid.substring(0, 8)}...
        </span>
        <span title={`Added: ${date}`}>
          {new Date(entry.added_time * 1000).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
        </span>
      </div>
    </div>
  );
};
