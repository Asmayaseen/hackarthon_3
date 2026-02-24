# Frontend Data Models (TS Interfaces)

interface Progress {
  mastery_score: number;
  trend: 'Improving' | 'Declining' | 'Stable';
  recent_scores: number[];
}

interface StruggleAlert {
  type: string;
  severity: 'low' | 'medium' | 'high';
  message: string;
  recommendations: string[];
}

interface DebugHint {
  level: 1 | 2 | 3;
  hint: string;
}
