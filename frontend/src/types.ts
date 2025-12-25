export interface ClipboardEntry {
  uuid: string;
  added_time: number;
  last_used_time?: number;
  mimetypes: string;
  text?: string;
  starred: boolean;
}

export interface FilterState {
  mimetype: string;
  starredOnly: boolean;
  timeRange: 'all' | 'today' | 'week' | 'month';
}

export interface WorkflowPrediction {
  name: string;
  confidence: number;
  reasoning: string;
}
