# Frontend Plan (4-frontend-integration)

## Scope
In: Monaco workspace, mastery charts, alerts, chat.
Out: Full auth (Better Auth next).

## Key Decisions
- **UI**: Shadcn/Tailwind Dark (dev-friendly); Lucide icons.
- **Editor**: Monaco (VSCode-like).
- **Charts**: Recharts (lightweight).
- **Realtime**: SWR + EventSource (Dapr SSE).
- **Pages**: /workspace (editor+chat), /dashboard (charts+alerts).

## Interfaces
- GET /progress/{id} → {mastery_score, trend}
- POST /query → triage classification
- SSE /struggles → struggle.detected events

## Deployment
Next.js static + API routes proxy to Kong.

Ready for tasks.
