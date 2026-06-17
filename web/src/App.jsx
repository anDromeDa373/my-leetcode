import { useEffect, useState } from 'react'
import { fetchSummary } from './lib/summary'

function pointsClass(points) {
  if (points >= 3) return 'bg-yellow-500 shadow-[0_0_16px_rgba(234,179,8,0.55)]'
  if (points === 2) return 'bg-green-600 shadow-[0_0_14px_rgba(22,163,74,0.5)]'
  if (points === 1) return 'bg-green-400 shadow-[0_0_12px_rgba(74,222,128,0.4)]'
  if (points === 0) return 'bg-gray-800 shadow-[0_0_6px_rgba(75,85,99,0.3)]'
  if (points === -1) return 'bg-red-400 shadow-[0_0_12px_rgba(248,113,113,0.45)]'
  return 'bg-red-700 shadow-[0_0_14px_rgba(185,28,28,0.55)]'
}

function formatLastAttempt(ts) {
  if (ts == null || ts === 0) return '—'
  return new Date(ts * 1000).toLocaleDateString('ja-JP', {
    year: '2-digit',
    month: '2-digit',
    day: '2-digit',
  })
}

function Tile({ problem }) {
  const points = problem.points ?? 0
  const textColor =
    points === 0 ? 'text-gray-500' : points >= 3 ? 'text-gray-900' : 'text-white'

  return (
    <div
      title={`${problem.id} — ${problem.title}\npoints: ${points}`}
      className={`group relative flex aspect-square flex-col items-center justify-center rounded-md border border-white/10 transition-transform hover:scale-105 hover:z-10 ${pointsClass(points)} ${textColor}`}
    >
      <span className="font-mono text-[10px] font-bold tracking-tight sm:text-xs">
        {problem.id}
      </span>
      <span className="mt-1 font-mono text-[8px] opacity-80 sm:text-[10px]">
        {formatLastAttempt(problem.last_attempt)}
      </span>
    </div>
  )
}

function App() {
  const [problems, setProblems] = useState([])
  const [updatedAt, setUpdatedAt] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false

    fetchSummary()
      .then(({ problems: loadedProblems, updatedAt: loadedUpdatedAt }) => {
        if (cancelled) return
        setProblems(loadedProblems)
        setUpdatedAt(loadedUpdatedAt)
        setError(null)
      })
      .catch((err) => {
        if (cancelled) return
        setProblems([])
        setUpdatedAt(null)
        setError(err.message)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [])

  const greenCount = problems.filter((p) => (p.points ?? 0) >= 1).length
  const goldCount = problems.filter((p) => (p.points ?? 0) >= 3).length

  return (
    <div className="min-h-screen bg-[#1a1a1a] px-4 py-10 text-green-100">
      <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(ellipse_at_top,rgba(0,255,136,0.07),transparent_55%)]" />
      <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(ellipse_at_bottom_right,rgba(255,60,80,0.05),transparent_50%)]" />

      <main className="relative mx-auto max-w-5xl">
        <header className="mb-8 text-center">
          <p className="mb-2 font-mono text-sm text-green-500/80">
            <span className="text-green-400">&gt;</span> progress_tracker.init()
          </p>
          <h1 className="font-mono text-2xl font-bold tracking-wide text-green-50 sm:text-3xl">
            LCT: NeetCode 150 Mastery
          </h1>
          <p className="mt-2 font-mono text-xs text-gray-500">
            {loading
              ? 'loading summary.json...'
              : updatedAt
                ? `last sync: ${formatLastAttempt(updatedAt)}`
                : 'ready'}
          </p>
          {!loading && !error && (
            <p className="mt-1 font-mono text-xs text-gray-600">
              {problems.length} / 150 | green+: {greenCount} | gold: {goldCount}
            </p>
          )}
        </header>

        {error && (
          <p className="mb-6 rounded border border-red-900/60 bg-red-950/40 px-4 py-3 text-center font-mono text-sm text-red-400">
            {error}
          </p>
        )}

        <section
          className="mx-auto grid max-w-4xl gap-1.5 sm:gap-2"
          style={{ gridTemplateColumns: 'repeat(15, minmax(0, 1fr))' }}
          aria-label="NeetCode 150 progress grid"
        >
          {loading
            ? Array.from({ length: 150 }, (_, i) => (
                <div
                  key={`skel-${i}`}
                  className="aspect-square animate-pulse rounded-md bg-gray-800/60"
                />
              ))
            : problems.map((problem) => (
                <Tile key={problem.id} problem={problem} />
              ))}
        </section>

        <footer className="mt-10 flex flex-wrap justify-center gap-3 font-mono text-[10px] text-gray-500">
          <LegendItem color="bg-yellow-500" label="≥3" />
          <LegendItem color="bg-green-600" label="2" />
          <LegendItem color="bg-green-400" label="1" />
          <LegendItem color="bg-gray-800" label="0" />
          <LegendItem color="bg-red-400" label="-1" />
          <LegendItem color="bg-red-700" label="≤-2" />
        </footer>
      </main>
    </div>
  )
}

function LegendItem({ color, label }) {
  return (
    <span className="flex items-center gap-1.5">
      <span className={`inline-block h-3 w-3 rounded-sm ${color}`} />
      {label}
    </span>
  )
}

export default App
