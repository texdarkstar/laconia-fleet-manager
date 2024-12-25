import { ChatInputCommandInteraction, SlashCommandBuilder } from "discord.js";
import { CommandHandler, CommandResult } from "../types/commandHandler";
import { db } from "../db/drizzleClient";
import { ShipyardTable } from "../db/schema";

export const createShipyardCommand: CommandHandler<ChatInputCommandInteraction<"cached">> = {
    name: "createshipyard",
    interaction: new SlashCommandBuilder()
        .setName("createshipyard")
        .setDescription("Creates a shipyard")
        .addStringOption(option => option
            .setName("name")
            .setDescription("The name of the shipyard")
            .setRequired(true))
        .addUserOption(option => option
            .setName("owner")
            .setDescription("The owner of the shipyard")
            .setRequired(false)) // Optional parameter, defaults to the user who invoked the command if not provided
        .setContexts(0) // This means the command is only available in guilds
        .toJSON(),
    handler: async (interaction) => {
        const name = interaction.options.getString("name")!; // The ! is used to assert that the value is not null, since the parameter is required
        const owner = interaction.options.getUser("owner") || interaction.user; // If the owner option is null, use the user who invoked the command

        try {
            await db.insert(ShipyardTable).values({
                name, // You can also type "name: name" but this is a shorthand when the variable name is the same as the key
                owner: owner.id
            });
        } catch (error) {
            console.error("Error creating shipyard", error);
            interaction.reply({
                content: "An error occurred while creating the shipyard",
                ephemeral: true
            });
            return CommandResult.Error;
        }

        await interaction.reply(`Shipyard "${name}" created successfully`);
        return CommandResult.Success;
    }
}