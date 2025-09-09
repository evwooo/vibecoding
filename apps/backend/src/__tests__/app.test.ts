import request from "supertest";
import { createApp } from "../app.js";

describe("app", () => {
  it("responds to /health", async () => {
    const app = createApp();
    const res = await request(app).get("/health");
    expect(res.status).toBe(200);
    expect(res.body.status).toBe("ok");
  });
});

