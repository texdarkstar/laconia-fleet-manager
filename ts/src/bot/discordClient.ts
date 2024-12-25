import { ChatInputCommandInteraction, Client, Events, GatewayIntentBits } from "discord.js";
import { AddEventListeners } from "./interactionHandler";

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        // PRIVILEGED INTENTS - These are not enabled by default, and require whitelisting in the developer portal.
        // GatewayIntentBits.MessageContent
        // GatewayIntentBits.GuildMembers,
        // GatewayIntentBits.GuildPresences
    ]
});

export function GetClient() {
    return client;
}

/**
 * Establishes a connection to the discord gateway, and uses the now active client object to initialise core systems.
 * @param token Discord Bot token, found in the developer portal. DO NOT HARDCODE OR COMMIT. Use .env files!
 * @returns Success state of bot startup.
 */
export async function DiscordConnect(token: string, registerEventListeners = true): Promise<boolean> {
    try {
        await client.login(token);
        console.log("Discord Gateway: Ready");

        // When ready, the bot client is passed to initialisers to set up.
        client.on(Events.ClientReady, async (c) => AddEventListeners(c));

        return true;
    } catch (error) {
        console.error(error);
        return false;
    }
}