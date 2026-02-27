import { NextRequest, NextResponse } from 'next/server'
import OpenAI from 'openai'

const SYSTEM_PROMPTS: Record<string, string> = {
  explain: `You are a friendly Python tutor. Explain Python concepts clearly with:
- Simple language for beginners
- Concrete code examples
- Common mistakes to avoid
Keep responses concise (3-5 paragraphs max). Use markdown for code blocks.`,

  debug: `You are a Python debugging expert. Help students fix errors by:
- Identifying the root cause of the error
- Explaining WHY it happened
- Giving a hint (not the full solution) first
- Then showing the fix if they're stuck
Keep responses focused and practical.`,

  exercise: `You are a Python exercise generator. Create coding challenges that:
- Are appropriate for the student's level
- Have clear problem statements
- Include example inputs/outputs
- Build on what they're learning
Format: Problem description, then starter code template.`,

  review: `You are a Python code reviewer. Analyze student code for:
- Correctness and logic errors
- PEP 8 style compliance
- Efficiency improvements
- Readability suggestions
Be encouraging but thorough. Rate code 1-10.`,

  progress: `You are a learning progress coach. Based on the student's question about progress:
- Summarize their learning journey
- Highlight strengths and areas to improve
- Suggest next steps
- Be motivating and specific.`,

  unclassified: `You are a helpful Python tutor. Answer the student's question helpfully and suggest how LearnFlow can help them learn Python better.`,
}

type Classification = 'explain' | 'debug' | 'exercise' | 'review' | 'progress' | 'unclassified'

export async function POST(req: NextRequest) {
  const apiKey = process.env.OPENAI_API_KEY
  if (!apiKey) {
    return NextResponse.json(
      { reply: 'AI tutor is not configured. Please set OPENAI_API_KEY in environment variables.', classification: 'unclassified', confidence: 0 },
      { status: 200 }
    )
  }

  const client = new OpenAI({ apiKey })
  const model = process.env.AI_MODEL || 'gpt-4o-mini'

  try {
    const body = await req.json()
    const { message, student_level = 'beginner', history = [] } = body

    if (!message || typeof message !== 'string') {
      return NextResponse.json({ error: 'No message provided' }, { status: 400 })
    }

    // Step 1: Classify the query
    let classification: Classification = 'unclassified'
    let confidence = 0
    try {
      const classifyRes = await client.chat.completions.create({
        model,
        temperature: 0.1,
        response_format: { type: 'json_object' },
        messages: [
          {
            role: 'system',
            content: `You are a Python programming tutor. Classify student queries into these categories:
- "explain": Student wants to understand a concept
- "debug": Student has an error and needs help fixing it
- "exercise": Student wants practice problems
- "review": Student wants code review
- "progress": Student wants to see their progress

Respond with JSON: {"classification": "explain|debug|exercise|review|progress|unclassified", "confidence": 0.0-1.0, "reason": "brief explanation"}`,
          },
          { role: 'user', content: `Student level: ${student_level}\nQuery: ${message}` },
        ],
      })
      const parsed = JSON.parse(classifyRes.choices[0].message.content || '{}')
      classification = parsed.classification || 'unclassified'
      confidence = parseFloat(parsed.confidence) || 0
    } catch {
      // Classification failed, continue with unclassified
    }

    // Step 2: Generate the tutoring response
    const systemPrompt = SYSTEM_PROMPTS[classification] || SYSTEM_PROMPTS.unclassified
    const messages: OpenAI.Chat.ChatCompletionMessageParam[] = [
      { role: 'system', content: systemPrompt },
      // Include last 6 history messages for context
      ...((history as { role: string; content: string }[]).slice(-6).map((h) => ({
        role: h.role as 'user' | 'assistant',
        content: h.content,
      }))),
      { role: 'user', content: message },
    ]

    const replyRes = await client.chat.completions.create({
      model,
      temperature: 0.7,
      max_tokens: 600,
      messages,
    })

    const reply = replyRes.choices[0].message.content || 'Sorry, I could not generate a response.'
    return NextResponse.json({ reply, classification, confidence })
  } catch (err: unknown) {
    const e = err as { status?: number; message?: string }
    if (e.status === 401) {
      return NextResponse.json(
        { reply: 'AI tutor API key is invalid. Please check OPENAI_API_KEY in Vercel settings.', classification: 'unclassified', confidence: 0 },
        { status: 200 }
      )
    }
    return NextResponse.json(
      { reply: "I'm having trouble connecting to the AI tutor. Please try again in a moment.", classification: 'unclassified', confidence: 0 },
      { status: 200 }
    )
  }
}
