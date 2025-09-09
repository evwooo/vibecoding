import prisma from "../src/prisma.js";
import bcrypt from "bcryptjs";

async function main() {
  const email = "demo@example.com";
  const passwordHash = await bcrypt.hash("password123", 10);
  const user = await prisma.user.upsert({
    where: { email },
    update: {},
    create: { email, password: passwordHash, name: "Demo User" },
  });

  const project = await prisma.project.upsert({
    where: { id: 1 },
    update: {},
    create: { name: "Demo Project", description: "Seeded project", ownerId: user.id },
  });

  await prisma.task.createMany({
    data: [
      { title: "Set up repo", description: "Initialize monorepo", projectId: project.id, assigneeId: user.id },
      { title: "Build backend", description: "Express + Prisma", projectId: project.id, assigneeId: user.id },
      { title: "Build frontend", description: "React + Vite", projectId: project.id, assigneeId: user.id },
    ],
    skipDuplicates: true,
  });
}

main().finally(async () => {
  await prisma.$disconnect();
});

