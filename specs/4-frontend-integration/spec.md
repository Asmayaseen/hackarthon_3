# Frontend Integration Specification (4-frontend-integration)

**Feature ID**: 4-frontend-integration
**Status**: Specification Complete
**Branch**: 4-frontend-integration

## Overview
Next.js 14+ App Router frontend integrating backend services (Progress, Triage, Debug, Review). Modern UI with Tailwind CSS, Shadcn UI (Dark Mode default), Lucide Icons, Monaco Editor. Realtime mastery dashboard, alerts, AI sidekick chat.

## User Scenarios

### US1: Code Workspace (P1)
**Flow**: Student types Python in Monaco Editor → Auto-submit to triage-service → Route to Debug/Review/Exercise.
**Acceptance**: Monaco syntax highlighting/autocomplete; realtime backend response.

### US2: Mastery Visualizer (P1)
**Flow**: Poll/fetch /progress/{student_id} → Recharts graph (mastery over time, trend line).
**Acceptance**: Dark mode charts; realtime updates (SWR/React Query).

### US3: Struggle Alerts (P2)
**Flow**: Subscribe struggle.detected (WebSocket/Dapr SSE) → Shadcn Toast popup (empathetic: "Struggling? Let's review!").
**Acceptance**: Non-intrusive; dismissible; links to hints.

### US4: AI Sidekick Chat (P2)
**Flow**: Chat UI (Shadcn) → Debug hints (progressive levels); Monaco integration.
**Acceptance**: Message history; typing indicators.

## Functional Requirements
**FR1**: Monaco Editor (react-monaco-editor) in /workspace; POST code to triage-service/query.
**FR2**: Dashboard /progress → Recharts LineChart (mastery_scores, trends).
**FR3**: Toasts via sonner/react-hot-toast on struggle events (EventSource /struggles).
**FR4**: Chat via /debug-hints endpoint; Lucide icons (send, history).

## Tech Stack (plan.md)
- Next.js 14 App Router
- Tailwind CSS + Shadcn UI (Dark default)
- Monaco Editor
- Recharts
- SWR (fetching)
- Lucide React Icons
- TypeScript

## NFRs
- Perf: <100ms chart updates
- UX: Dark mode, responsive, accessible

## Data Flow
Frontend → Kong Gateway → Services (JWT auth)

Ready for /sp.plan → /sp.tasks → /sp.implement
