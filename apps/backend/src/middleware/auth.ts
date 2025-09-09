import type { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";

export interface AuthRequest extends Request {
  userId?: number;
}

export function requireAuth(req: AuthRequest, res: Response, next: NextFunction) {
  const header = req.headers.authorization;
  if (!header || !header.startsWith("Bearer ")) {
    return res.status(401).json({ error: "Missing token" });
  }
  const token = header.slice("Bearer ".length);
  const secret = process.env.JWT_SECRET ?? "dev-secret";
  try {
    const payload = jwt.verify(token, secret) as { userId: number };
    req.userId = payload.userId;
    next();
  } catch {
    res.status(401).json({ error: "Invalid token" });
  }
}

export function signToken(userId: number): string {
  const secret = process.env.JWT_SECRET ?? "dev-secret";
  return jwt.sign({ userId }, secret, { expiresIn: "7d" });
}

