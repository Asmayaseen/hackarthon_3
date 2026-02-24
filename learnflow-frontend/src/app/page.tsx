import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-950 flex flex-col items-center justify-center p-8">
      <div className="max-w-2xl w-full text-center space-y-8">
        {/* Logo */}
        <div className="flex items-center justify-center gap-3">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-2xl shadow-lg shadow-blue-500/30">
            L
          </div>
          <h1 className="text-4xl font-bold text-white">LearnFlow</h1>
        </div>

        {/* Tagline */}
        <div className="space-y-3">
          <p className="text-xl text-gray-300">AI-Powered Python Tutoring Platform</p>
          <p className="text-gray-500 text-sm max-w-lg mx-auto">
            Learn Python through conversation, hands-on coding, quizzes, and personalized AI feedback.
            Built with FastAPI, Dapr, Kafka, and Next.js.
          </p>
        </div>

        {/* Feature pills */}
        <div className="flex flex-wrap gap-2 justify-center">
          {['🤖 AI Tutor', '💻 Code Editor', '📊 Progress Tracking', '🎯 Quizzes', '🔍 Debug Help', '✅ Code Review'].map(f => (
            <span key={f} className="px-3 py-1 bg-gray-800 border border-gray-700 rounded-full text-xs text-gray-300">
              {f}
            </span>
          ))}
        </div>

        {/* CTA */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Link
            href="/dashboard"
            className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold rounded-xl shadow-lg shadow-blue-500/20 transition-all hover:scale-105"
          >
            Start Learning →
          </Link>
          <a
            href="https://github.com/Asmayaseen/hackarthon_3"
            target="_blank"
            rel="noreferrer"
            className="px-8 py-3 bg-gray-800 border border-gray-700 hover:border-gray-500 text-gray-300 font-semibold rounded-xl transition-all"
          >
            View on GitHub
          </a>
        </div>

        {/* Architecture note */}
        <p className="text-gray-600 text-xs">
          Microservices: Triage · Concepts · Debug · Exercise · Code Review · Progress
          &nbsp;|&nbsp; Kafka · Dapr · Neon PostgreSQL · Kubernetes
        </p>
      </div>
    </main>
  )
}
