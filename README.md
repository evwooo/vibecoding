## Internship-Ready Full-Stack Monorepo

Modern full-stack application demonstrating production-grade patterns.

- Backend: Node.js, TypeScript, Express 5, Prisma (SQLite), JWT, Zod
- Frontend: React (Vite + TypeScript), Tailwind CSS, React Router, React Query
- Monorepo: npm workspaces, shared package with Zod schemas

### Getting Started

Prereqs: Node.js >= 18 and npm.

Install all dependencies:

```bash
npm install
```

Run both apps in dev mode:

```bash
npm run dev
```

- Backend: `http://localhost:4000` (health: `/health`)
- Frontend: `http://localhost:5173` (proxies `/api` to backend)

Optional seed:

```bash
cd apps/backend && npm run db:seed
```

### Structure

- `apps/backend`: Express + Prisma API server
- `apps/frontend`: Vite React TS client
- `packages/shared`: Shared Zod schemas/types

### Backend scripts

```bash
npm run dev        # watch mode
npm run build      # compile
npm start          # run compiled
npm run db:migrate # prisma migrate dev
npm run db:reset   # reset DB
npm run db:seed    # seed DB
```

Env (`apps/backend/.env`):

```
DATABASE_URL="file:./dev.db"
JWT_SECRET=dev-secret
```

API:
- POST `/api/auth/register` { name, email, password }
- POST `/api/auth/login` { email, password } -> { token }
- GET `/api/projects`
- POST `/api/projects` { name, description? }
- PUT `/api/projects/:id`
- DELETE `/api/projects/:id`
- GET `/api/tasks`
- POST `/api/tasks` { projectId, title, description?, assigneeId? }
- PUT `/api/tasks/:id`
- DELETE `/api/tasks/:id`

### Frontend

Run from `apps/frontend`:

```bash
npm run dev
```

Features: auth (JWT localStorage), list/create projects, list tasks.

### Notes

- SQLite for simplicity; swap datasource in Prisma to PostgreSQL if needed.
- Extend with RBAC, CI, tests, and deployment for production.

