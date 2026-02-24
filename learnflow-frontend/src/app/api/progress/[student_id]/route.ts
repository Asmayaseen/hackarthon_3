import { NextRequest, NextResponse } from 'next/server';

const PROGRESS_SERVICE_URL = process.env.PROGRESS_SERVICE_URL || 'http://localhost:8005';

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ student_id: string }> }
) {
  const { student_id } = await params;

  try {
    const res = await fetch(`${PROGRESS_SERVICE_URL}/progress/${student_id}`, {
      headers: { 'Content-Type': 'application/json' },
      cache: 'no-store',
    });

    if (!res.ok) throw new Error(`Progress service error: ${res.status}`);
    const data = await res.json();

    // Transform to frontend format
    const history = Object.entries(data.topics || {}).map(([topic, score], i) => ({
      week: `Week ${i + 1} (${topic})`,
      mastery: typeof score === 'number' ? Math.round(score) : 0,
    }));

    // If no topics yet, return sample data
    if (history.length === 0) {
      return NextResponse.json({
        history: [
          { week: 'Week 1 (Variables)', mastery: 85 },
          { week: 'Week 2 (Loops)', mastery: 68 },
          { week: 'Week 3 (Functions)', mastery: 52 },
          { week: 'Week 4 (OOP)', mastery: 40 },
        ],
        struggleDetected: data.struggle_detected || false,
      });
    }

    return NextResponse.json({
      history,
      struggleDetected: data.struggle_detected || false,
    });
  } catch {
    // Return demo data if progress service unreachable
    return NextResponse.json({
      history: [
        { week: 'Week 1 (Variables)', mastery: 85 },
        { week: 'Week 2 (Loops)', mastery: 68 },
        { week: 'Week 3 (Functions)', mastery: 52 },
        { week: 'Week 4 (OOP)', mastery: 40 },
        { week: 'Week 5 (Files)', mastery: 30 },
      ],
      struggleDetected: false,
    });
  }
}
