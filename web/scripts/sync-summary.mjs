import { copyFileSync, existsSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const webRoot = join(dirname(fileURLToPath(import.meta.url)), '..')
const repoSummary = join(webRoot, '..', 'summary.json')
const publicSummary = join(webRoot, 'public', 'summary.json')

if (!existsSync(repoSummary)) {
  if (existsSync(publicSummary)) {
    console.warn('[sync-summary] ../summary.json not found; keeping public/summary.json')
    process.exit(0)
  }
  console.error('[sync-summary] error: summary.json not found at repo root or in public/')
  process.exit(1)
}

copyFileSync(repoSummary, publicSummary)

const data = JSON.parse(readFileSync(publicSummary, 'utf8'))
const ncCount = (data.problems ?? []).filter((p) => /^nc\d{3}$/.test(p.id)).length
console.log(`[sync-summary] copied summary.json (${ncCount} nc problems) -> public/summary.json`)
