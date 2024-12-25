// dotenv imported first to make sure environment variables are loaded before drizzle.
import dotenv from "dotenv";
dotenv.config();
dotenv.config({ path: `.env.local`, override: true });

import { migrateDatabase } from "./db/drizzleClient";
import { DiscordConnect } from "./bot/discordClient";

async function Start() {
    // This is the entry point for your application.

    await migrateDatabase(); // This will run the migrations to create the database schema if it doesn't exist
    
    if (!process.env.DISCORD_BOT_TOKEN) {
        throw new Error("Please provide a DISCORD_BOT_TOKEN environment variable");
    }
    await DiscordConnect(process.env.DISCORD_BOT_TOKEN); // This will connect the bot to discord
}

Start();