import { Client, Events } from "discord.js";
import { helloWorldCommand } from "../commands/helloWorld";
import { createShipCommand } from "../commands/createShip";
import { createShipModelCommand } from "../commands/createShipModel";
import { createShipyardCommand } from "../commands/createShipyard";

export const commands = [
    helloWorldCommand,
    createShipCommand,
    createShipModelCommand,
    createShipyardCommand
    // Add more command handlers here as you create them
]

export function AddEventListeners(client: Client<true>) {
    // Registering routes for handling incoming discord events.
    client.on(Events.InteractionCreate, async (interaction) => {
        if (interaction.inCachedGuild() && (interaction.isChatInputCommand() || interaction.isAutocomplete())) {
            const command = commands.find(c => c.name === interaction.commandName);
            console.log(`Command: ${interaction.commandName}`);
            if (!command) {
                console.error(`Command not found: ${interaction.commandName}`);
                if (interaction.isRepliable()) {
                    interaction.reply({ content: "Command not found.", ephemeral: true });
                }
                return;
            }

            if (interaction.isChatInputCommand()) {
                console.log(`Chat command: ${interaction.commandName}`);
                await command.handler(interaction);
            } else if (interaction.isAutocomplete() && command.autocomplete) {
                console.log(`Autocomplete: ${interaction.commandName}`);
                await command.autocomplete(interaction);
            }
        };
    });

    console.log("Bot Status: Ready");
}