// dotenv imported first to make sure environment variables are loaded before drizzle.
import dotenv from "dotenv";
dotenv.config();
dotenv.config({ path: `.env.local`, override: true });

import { Client, GatewayIntentBits, REST, RESTPostAPIApplicationCommandsJSONBody, Routes } from "discord.js";
import { helloWorldCommand } from "../commands/helloWorld";
import { createShipModelCommand } from "../commands/createShipModel";
import { createShipyardCommand } from "../commands/createShipyard";
import { createShipCommand } from "../commands/createShip";
import { commands } from "./interactionHandler";

async function RegisterCommands() {
    console.log("Registering commands...");
    const client = new Client({
        intents: [GatewayIntentBits.Guilds]
    });

    await client.login(process.env.DISCORD_BOT_TOKEN!);
    const rest = new REST({ version: "10" }).setToken(process.env.DISCORD_BOT_TOKEN!);

    const commandsJson: RESTPostAPIApplicationCommandsJSONBody[] = commands.map(command => command.interaction);

    if (client?.user?.id) {
        await rest.put(Routes.applicationCommands(client.user.id), { body: commandsJson });
        console.log("Successfully registered commands");
        process.exit(1);
    } else {
        console.error("Could not register commands - client not ready");
    }
}

RegisterCommands();