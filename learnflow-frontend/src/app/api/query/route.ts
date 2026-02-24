import { NextRequest, NextResponse } from 'next/server';

const TRIAGE_SERVICE_URL = process.env.TRIAGE_SERVICE_URL || 'http://localhost:8080';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const res = await fetch(`${TRIAGE_SERVICE_URL}/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        student_id: body.student_id || 'demo-student',
        query_text: body.query_text || body.code || '',
        student_level: body.student_level || 'beginner',
        current_module_id: body.current_module_id || null,
      }),
    });

    if (!res.ok) throw new Error(`Triage error: ${res.status}`);
    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    // Return mock response if triage service is down
    return NextResponse.json({
      classification: 'explain',
      confidence: 0.9,
      reason: 'Demo mode: triage service offline',
      routed_to: 'concepts-service',
    });
  }
}
