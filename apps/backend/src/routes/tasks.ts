import { Router } from "express";
import { TaskCreateSchema, TaskUpdateSchema } from "@intern/shared";
import prisma from "../prisma.js";
import { requireAuth, type AuthRequest } from "../middleware/auth.js";

const router = Router();


router.use(requireAuth);

router.get("/", async (req: AuthRequest, res) => {
  const tasks = await prisma.task.findMany({
    where: { project: { ownerId: req.userId! } },
    orderBy: { createdAt: "desc" },
  });
  res.json(tasks);
});

router.post("/", async (req: AuthRequest, res) => {
  const parsed = TaskCreateSchema.safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ error: "Invalid input" });
  const { projectId, assigneeId, ...rest } = parsed.data;
  const project = await prisma.project.findFirst({ where: { id: projectId, ownerId: req.userId! } });
  if (!project) return res.status(403).json({ error: "No access to project" });
  const task = await prisma.task.create({ data: { ...rest, projectId, assigneeId: assigneeId ?? null } });
  res.status(201).json(task);
});

router.put(":id", async (req: AuthRequest, res) => {
  const id = Number(req.params.id);
  const parsed = TaskUpdateSchema.safeParse(req.body);
  if (!parsed.success || Number.isNaN(id)) return res.status(400).json({ error: "Invalid input" });
  const task = await prisma.task.update({
    where: { id },
    data: parsed.data,
  }).catch(() => null);
  if (!task) return res.status(404).json({ error: "Not found" });
  res.json(task);
});

router.delete(":id", async (req: AuthRequest, res) => {
  const id = Number(req.params.id);
  if (Number.isNaN(id)) return res.status(400).json({ error: "Invalid input" });
  const task = await prisma.task.delete({ where: { id } }).catch(() => null);
  if (!task) return res.status(404).json({ error: "Not found" });
  res.status(204).end();
});

export default router;

