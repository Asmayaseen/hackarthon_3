import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold">Welcome to Learnflow</h1>
      <p className="mt-4 text-xl">AI-powered learning dashboard</p>
      <Link href="/dashboard" className="mt-8 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Go to Dashboard
      </Link>
    </main>
  )
}