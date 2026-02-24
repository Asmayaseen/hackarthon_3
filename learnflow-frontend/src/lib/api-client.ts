import { SWRConfiguration } from 'swr';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8080';  // Triage proxy

export async function triageQuery(code: string, student_id: string = 'test') {
  const res = await fetch(`${API_BASE}/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query_text: code, student_id }),
  });
  if (!res.ok) throw new Error('Triage failed');
  return res.json();
}

export const swrConfig: SWRConfiguration = {
  revalidateOnFocus: false,
  revalidateIfStale: true,
};
