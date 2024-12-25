import dotenv from "dotenv";
dotenv.config();
dotenv.config({ path: `.env.local`, override: true });

import { defineConfig } from 'drizzle-kit';

export default defineConfig({
    dialect: 'postgresql',
    schema: './src/db/schema.ts',
    out: './src/db/migrations',
    dbCredentials: {
        url: process.env.DB_URL!,
    },
    verbose: true,
});