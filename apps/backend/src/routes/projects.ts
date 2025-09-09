import { Router } from "express";
import { ProjectCreateSchema, ProjectUpdateSchema } from "@intern/shared";
import prisma from "../prisma.js";
import { requireAuth, type AuthRequest } from "../middleware/auth.js";

const router = Router();


router.use(requireAuth);

router.get("/", async (req: AuthRequest, res) => {
  const projects = await prisma.project.findMany({
    where: { ownerId: req.userId! },
    orderBy: { createdAt: "desc" },
  });
  res.json(projects);
});

router.post("/", async (req: AuthRequest, res) => {
  const parsed = ProjectCreateSchema.safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ error: "Invalid input" });
  const project = await prisma.project.create({
    data: { ...parsed.data, ownerId: req.userId! },
  });
  res.status(201).json(project);
});

router.put(":id", async (req: AuthRequest, res) => {
  const id = Number(req.params.id);
  const parsed = ProjectUpdateSchema.safeParse(req.body);
  if (!parsed.success || Number.isNaN(id)) return res.status(400).json({ error: "Invalid input" });
  const project = await prisma.project.update({
    where: { id, ownerId: req.userId! },
    data: parsed.data,
  }).catch(() => null);
  if (!project) return res.status(404).json({ error: "Not found" });
  res.json(project);
});

router.delete(":id", async (req: AuthRequest, res) => {
  const id = Number(req.params.id);
  if (Number.isNaN(id)) return res.status(400).json({ error: "Invalid input" });
  const project = await prisma.project.delete({ where: { id, ownerId: req.userId! } }).catch(() => null);
  if (!project) return res.status(404).json({ error: "Not found" });
  res.status(204).end();
});

export default router;

