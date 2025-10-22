import { db } from "@/lib/db";
import { evaluationData } from "@/lib/db/schema";

async function testDbConnection() {
  try {
    // Attempt to fetch a small amount of data to verify connection
    const result = await db.select().from(evaluationData).limit(1);
    console.log("Database connection successful!");
    console.log("Example data fetched:", result);
  } catch (error) {
    console.error("Database connection failed:", error);
    process.exit(1);
  }
  process.exit(0);
}

testDbConnection();