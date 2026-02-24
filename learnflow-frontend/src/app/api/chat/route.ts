import { NextRequest, NextResponse } from 'next/server'

const TRIAGE_URL = process.env.TRIAGE_SERVICE_URL || 'http://localhost:8080'

export async function POST(req: NextRequest) {
  try {
    const body = await req.json()
    const { message, student_id = 'demo-student', student_level = 'beginner', history = [] } = body

    const res = await fetch(`${TRIAGE_URL}/answer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        student_id,
        message,
        student_level,
        conversation_history: history,
      }),
    })

    if (!res.ok) throw new Error(`Triage error: ${res.status}`)
    const data = await res.json()
    return NextResponse.json(data)
  } catch {
    return NextResponse.json(
      { reply: "I'm having trouble connecting to the AI tutor. Please try again in a moment.", classification: 'unclassified', confidence: 0 },
      { status: 200 }
    )
  }
}
