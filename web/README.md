# Web Dashboard (Vercel deploy only)

This folder contains the React dashboard for visualizing `summary.json`.  
Local development (`npm run dev`) is not used — deploy via Vercel only.

## Vercel settings

| Setting | Value |
|---------|-------|
| Root Directory | `web` |
| Build Command | `npm run build` |
| Output Directory | `dist` |

`prebuild` copies `../summary.json` into `public/` automatically.
