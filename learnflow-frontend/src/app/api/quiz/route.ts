import { NextRequest, NextResponse } from 'next/server'

const QUIZ_QUESTIONS = [
  {
    id: 1,
    question: "What is the output of: `print(type([]))`?",
    options: ["<class 'list'>", "<class 'array'>", "<class 'tuple'>", "None"],
    answer: 0,
    topic: "Data Structures",
  },
  {
    id: 2,
    question: "Which keyword is used to define a function in Python?",
    options: ["function", "fun", "def", "define"],
    answer: 2,
    topic: "Functions",
  },
  {
    id: 3,
    question: "What does `range(3)` produce?",
    options: ["[1, 2, 3]", "[0, 1, 2]", "[0, 1, 2, 3]", "[1, 2]"],
    answer: 1,
    topic: "Loops",
  },
  {
    id: 4,
    question: "How do you start a comment in Python?",
    options: ["//", "/*", "#", "--"],
    answer: 2,
    topic: "Basics",
  },
  {
    id: 5,
    question: "What is the correct way to check if a key exists in a dict?",
    options: ["dict.has(key)", "key in dict", "dict.contains(key)", "dict[key] exists"],
    answer: 1,
    topic: "Data Structures",
  },
]

export async function GET() {
  // Return 3 random questions
  const shuffled = [...QUIZ_QUESTIONS].sort(() => Math.random() - 0.5)
  return NextResponse.json({ questions: shuffled.slice(0, 3) })
}

export async function POST(req: NextRequest) {
  try {
    const { answers } = await req.json()
    // answers: { [questionId]: selectedIndex }
    let correct = 0
    const results: any[] = []

    for (const q of QUIZ_QUESTIONS) {
      const selected = answers[q.id]
      const isCorrect = selected === q.answer
      if (isCorrect) correct++
      results.push({
        id: q.id,
        question: q.question,
        selected,
        correct: q.answer,
        isCorrect,
        topic: q.topic,
      })
    }

    const score = Math.round((correct / Object.keys(answers).length) * 100)
    const struggleDetected = score < 50

    return NextResponse.json({ score, correct, total: Object.keys(answers).length, results, struggleDetected })
  } catch {
    return NextResponse.json({ error: 'Quiz grading failed' }, { status: 500 })
  }
}
