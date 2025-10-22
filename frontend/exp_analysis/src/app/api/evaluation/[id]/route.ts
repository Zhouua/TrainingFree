import { db } from "@/lib/db";
import { evaluationData } from "@/lib/db/schema";
import { NextResponse } from "next/server";
import { eq } from "drizzle-orm";

export async function GET(
  req: Request
) {
  const url = new URL(req.url);
  const pathSegments = url.pathname.split('/');
  // Assuming the path is /api/evaluation/[id]
  const id = parseInt(pathSegments[pathSegments.length - 1], 10);

  if (isNaN(id)) {
    return NextResponse.json({ error: "Invalid ID" }, { status: 400 });
  }

  const data = await db
    .select()
    .from(evaluationData)
    .where(eq(evaluationData.id, id))
    .limit(1);

  if (data.length === 0) {
    return NextResponse.json({ error: "Evaluation not found" }, { status: 404 });
  }

  return NextResponse.json(data[0]);
}
