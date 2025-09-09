import { z } from "zod";
export const CredentialsSchema = z.object({
    email: z.string().email(),
    password: z.string().min(6),
});
export const RegisterSchema = CredentialsSchema.extend({
    name: z.string().min(1),
});
export const ProjectCreateSchema = z.object({
    name: z.string().min(1),
    description: z.string().optional(),
});
export const ProjectUpdateSchema = ProjectCreateSchema.partial();
export const TaskCreateSchema = z.object({
    projectId: z.number().int(),
    title: z.string().min(1),
    description: z.string().optional(),
    assigneeId: z.number().int().optional(),
});
export const TaskUpdateSchema = z.object({
    title: z.string().min(1).optional(),
    description: z.string().optional(),
    status: z.enum(["TODO", "IN_PROGRESS", "DONE"]).optional(),
    assigneeId: z.number().int().nullable().optional(),
});
