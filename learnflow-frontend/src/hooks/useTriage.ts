'use client';

import { useState } from 'react';
import { triageQuery } from '@/lib/api-client';

export function useTriage(setFeedback: (feedback: string) => void) {
  const [loading, setLoading] = useState(false);

  const submitCode = async (code: string) => {
    setLoading(true);
    try {
      const response = await triageQuery(code);
      setFeedback(JSON.stringify(response, null, 2));
    } catch (error) {
      setFeedback(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return { submitCode, loading };
}
