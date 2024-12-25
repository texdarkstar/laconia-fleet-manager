import { drizzle } from "drizzle-orm/postgres-js";
import { migrate } from "drizzle-orm/postgres-js/migrator";
import postgres from "postgres";
import { exit } from "process";
import * as schema from "./schema";

const connectionString = process.env.DB_URL;

if (!connectionString) {
    throw new Error("Please provide a DB_URL environment variable");
    exit(1);
}

const client = postgres(connectionString, {prepare: false});
export const db = drizzle(client, { schema });

export const migrateDatabase = async () => {
    await migrate(db, { migrationsFolder: "./src/db/migrations" })
}
