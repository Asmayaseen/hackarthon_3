import { NextRequest, NextResponse } from 'next/server'

const QUIZ_QUESTIONS = [
  { id: 1,  question: "What is the output of: print(type([]))?",                          options: ["<class 'list'>", "<class 'array'>", "<class 'tuple'>", "None"],                             answer: 0, topic: "Data Structures" },
  { id: 2,  question: "Which keyword defines a function in Python?",                       options: ["function", "fun", "def", "define"],                                                          answer: 2, topic: "Functions" },
  { id: 3,  question: "What does range(3) produce?",                                       options: ["[1, 2, 3]", "[0, 1, 2]", "[0, 1, 2, 3]", "[1, 2]"],                                        answer: 1, topic: "Loops" },
  { id: 4,  question: "How do you start a comment in Python?",                             options: ["//", "/*", "#", "--"],                                                                       answer: 2, topic: "Basics" },
  { id: 5,  question: "What is the correct way to check if a key exists in a dict?",      options: ["dict.has(key)", "key in dict", "dict.contains(key)", "dict[key] exists"],                   answer: 1, topic: "Data Structures" },
  { id: 6,  question: "Which of these creates an empty list?",                             options: ["list()", "[]", "Both A and B", "{}"],                                                        answer: 2, topic: "Data Structures" },
  { id: 7,  question: "What does len('Python') return?",                                   options: ["5", "6", "7", "Error"],                                                                      answer: 1, topic: "Strings" },
  { id: 8,  question: "Which loop guarantees at least one execution?",                     options: ["for loop", "while loop", "do-while loop", "Python has no such loop"],                       answer: 3, topic: "Loops" },
  { id: 9,  question: "What is the output of: print(2 ** 3)?",                             options: ["6", "8", "9", "Error"],                                                                     answer: 1, topic: "Basics" },
  { id: 10, question: "How do you access the last element of a list named 'lst'?",        options: ["lst[-1]", "lst[last]", "lst[len(lst)]", "lst.last()"],                                      answer: 0, topic: "Data Structures" },
  { id: 11, question: "What keyword is used to handle exceptions in Python?",              options: ["catch", "except", "error", "handle"],                                                        answer: 1, topic: "Error Handling" },
  { id: 12, question: "Which method adds an item to the end of a list?",                   options: ["add()", "push()", "append()", "insert()"],                                                   answer: 2, topic: "Data Structures" },
  { id: 13, question: "What is the correct syntax for a class in Python?",                 options: ["class MyClass:", "Class MyClass:", "def MyClass():", "create MyClass:"],                    answer: 0, topic: "OOP" },
  { id: 14, question: "What does the 'self' parameter refer to in a class method?",        options: ["The class itself", "The current instance", "A parent class", "Nothing special"],            answer: 1, topic: "OOP" },
  { id: 15, question: "How do you open a file for reading in Python?",                     options: ["open('file.txt')", "open('file.txt', 'r')", "Both A and B", "read('file.txt')"],            answer: 2, topic: "File I/O" },
]

export async function GET() {
  const shuffled = [...QUIZ_QUESTIONS].sort(() => Math.random() - 0.5)
  return NextResponse.json({ questions: shuffled.slice(0, 5), total: QUIZ_QUESTIONS.length })
}

export async function POST(req: NextRequest) {
  try {
    const { answers, questionIds } = await req.json()
    const answeredQuestions = QUIZ_QUESTIONS.filter(q => questionIds?.includes(q.id) || answers[q.id] !== undefined)

    let correct = 0
    const results: Record<string, unknown>[] = []

    for (const q of answeredQuestions) {
      const selected = answers[q.id]
      if (selected === undefined) continue
      const isCorrect = selected === q.answer
      if (isCorrect) correct++
      results.push({
        id: q.id,
        question: q.question,
        selected,
        correctAnswer: q.answer,
        correctLabel: q.options[q.answer],
        selectedLabel: q.options[selected] ?? 'Not answered',
        isCorrect,
        topic: q.topic,
      })
    }

    const total = results.length
    const score = total > 0 ? Math.round((correct / total) * 100) : 0
    const struggleDetected = score < 50

    return NextResponse.json({ score, correct, total, results, struggleDetected })
  } catch {
    return NextResponse.json({ error: 'Quiz grading failed' }, { status: 500 })
  }
}
