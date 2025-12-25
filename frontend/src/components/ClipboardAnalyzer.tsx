import React, { useState, useEffect, useMemo } from 'react';
import type { ClipboardEntry, FilterState, WorkflowPrediction } from '../types';
import { DataCard } from './DataCard';
import './ClipboardAnalyzer.css';

const API_BASE = 'http://localhost:8000/api';

export const ClipboardAnalyzer: React.FC = () => {
  const [entries, setEntries] = useState<ClipboardEntry[]>([]);
  const [prediction, setPrediction] = useState<WorkflowPrediction | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid');
  const [filters, setFilters] = useState<FilterState>({
    mimetype: 'all',
    starredOnly: false,
    timeRange: 'all'
  });

  const fetchData = async () => {
    try {
      setLoading(true);
      const [entriesRes, predRes] = await Promise.all([
        fetch(`${API_BASE}/entries`),
        fetch(`${API_BASE}/prediction`)
      ]);

      if (!entriesRes.ok) throw new Error('Failed to fetch entries');
      if (!predRes.ok) throw new Error('Failed to fetch prediction');

      const entriesData = await entriesRes.json();
      const predData = await predRes.json();

      setEntries(entriesData);
      setPrediction(predData);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const uniqueMimeTypes = useMemo(() => {
    const types = new Set<string>();
    entries.forEach(e => e.mimetypes.split(',').forEach(t => types.add(t)));
    return Array.from(types).sort();
  }, [entries]);

  const filteredEntries = useMemo(() => {
    return entries.filter(entry => {
      if (filters.starredOnly && !entry.starred) return false;
      if (filters.mimetype !== 'all' && !entry.mimetypes.includes(filters.mimetype)) return false;
      // Time range logic
      const now = new Date();
      const entryDate = new Date(entry.added_time * 1000);
      
      if (filters.timeRange === 'today') {
        const startOfToday = new Date(now.setHours(0, 0, 0, 0));
        if (entryDate < startOfToday) return false;
      } else if (filters.timeRange === 'week') {
        const startOfWeek = new Date(now.setDate(now.getDate() - 7));
        if (entryDate < startOfWeek) return false;
      } else if (filters.timeRange === 'month') {
        const startOfMonth = new Date(now.setMonth(now.getMonth() - 1));
        if (entryDate < startOfMonth) return false;
      }

      return true;
    }).sort((a, b) => b.added_time - a.added_time);
  }, [entries, filters]);

  const toggleStar = async (uuid: string) => {
    // Optimistic update
    setEntries(prev => prev.map(e => 
      e.uuid === uuid ? { ...e, starred: !e.starred } : e
    ));

    try {
      const res = await fetch(`${API_BASE}/entries/${uuid}/star`, { method: 'POST' });
      if (!res.ok) throw new Error('Failed to update star');
    } catch (err) {
      // Revert if failed
      setEntries(prev => prev.map(e => 
        e.uuid === uuid ? { ...e, starred: !e.starred } : e
      ));
      console.error(err);
    }
  };

  if (loading && entries.length === 0) {
    return <div className="clipboard-analyzer loading">Loading analysis...</div>;
  }

  if (error) {
    return (
      <div className="clipboard-analyzer error">
        <h2>Connection Error</h2>
        <p>{error}</p>
        <button onClick={fetchData}>Retry</button>
      </div>
    );
  }

  return (
    <div className="clipboard-analyzer">
      <header className="ca-header">
        <h1 className="ca-title">Clipboard Data Analyzer</h1>
        <p className="ca-subtitle">Connected to MySQL Backend (Port 4448)</p>
        
        {prediction && (
          <div className="ca-prediction-card">
            <div className="cap-label">Predicted Workflow</div>
            <div className="cap-content">
              <span className="cap-name">{prediction.name}</span>
              <span className="cap-confidence">{(prediction.confidence * 100).toFixed(0)}% Confidence</span>
            </div>
            <div className="cap-reasoning">{prediction.reasoning}</div>
          </div>
        )}
      </header>

      <div className="ca-controls">
        <div className="ca-filter-group">
          <select 
            className="ca-select"
            value={filters.mimetype}
            onChange={(e) => setFilters(prev => ({ ...prev, mimetype: e.target.value }))}
          >
            <option value="all">All Types</option>
            {uniqueMimeTypes.map(t => <option key={t} value={t}>{t}</option>)}
          </select>

          <select 
            className="ca-select"
            value={filters.timeRange}
            onChange={(e) => setFilters(prev => ({ ...prev, timeRange: e.target.value as any }))}
          >
            <option value="all">All Time</option>
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
          </select>

          <button 
            className={`ca-toggle-btn ${filters.starredOnly ? 'active' : ''}`}
            onClick={() => setFilters(prev => ({ ...prev, starredOnly: !prev.starredOnly }))}
          >
            ★ Starred Only
          </button>
        </div>

        <div className="ca-view-toggle">
          <button 
            className={`ca-view-btn ${viewMode === 'grid' ? 'active' : ''}`}
            onClick={() => setViewMode('grid')}
          >
            Grid
          </button>
          <button 
            className={`ca-view-btn ${viewMode === 'table' ? 'active' : ''}`}
            onClick={() => setViewMode('table')}
          >
            Table
          </button>
        </div>
      </div>

      {viewMode === 'grid' ? (
        <div className="ca-grid">
          {filteredEntries.map(entry => (
            <DataCard key={entry.uuid} entry={entry} onToggleStar={toggleStar} />
          ))}
        </div>
      ) : (
        <div className="ca-table-container">
          <table className="ca-table">
            <thead>
              <tr>
                <th>UUID</th>
                <th>Type</th>
                <th>Time</th>
                <th>Content</th>
                <th>Starred</th>
              </tr>
            </thead>
            <tbody>
              {filteredEntries.map(entry => (
                <tr key={entry.uuid}>
                  <td className="dc-uuid">{entry.uuid.substring(0, 8)}...</td>
                  <td>{entry.mimetypes}</td>
                  <td>{new Date(entry.added_time * 1000).toLocaleString()}</td>
                  <td>{entry.text?.substring(0, 50)}...</td>
                  <td>
                    <button onClick={() => toggleStar(entry.uuid)}>
                      {entry.starred ? '★' : '☆'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
