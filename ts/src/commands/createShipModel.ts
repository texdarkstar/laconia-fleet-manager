import { ChatInputCommandInteraction, SlashCommandBuilder } from "discord.js";
import { CommandHandler, CommandResult } from "../types/commandHandler";
import { shipClassifications } from "../types/shipClassification";
import { db } from "../db/drizzleClient";
import { ShipModelTable } from "../db/schema";

export const createShipModelCommand: CommandHandler<ChatInputCommandInteraction<"cached">> = {
    name: "createshipmodel",
    interaction: new SlashCommandBuilder()
        .setName("createshipmodel")
        .setDescription("Creates a ship model")
        .addStringOption(option => option
            .setName("name")
            .setDescription("The name of the ship model")
            .setRequired(true))
        .addStringOption(option => option
            .setName("classification")
            .setDescription("The classification of the ship model")
            .setChoices(shipClassifications.map(classification => ({name: `${classification.name} (${classification.acronym})`, value: classification.acronym})))
            .setRequired(true)
        )
        .addUserOption(option => option
            .setName("designer")
            .setDescription("The designer of the ship model")
            .setRequired(false)) // Optional parameter, defaults to the user who invoked the command if not provided
        .setContexts(0) // This means the command is only available in guilds
        .toJSON(),
    handler: async (interaction) => {
        const name = interaction.options.getString("name")!; // The ! is used to assert that the value is not null, since the parameter is required
        const classification = interaction.options.getString("classification")!;
        const designer = interaction.options.getUser("designer") || interaction.user; // If the designer option is null, use the user who invoked the command

        try {
            await db.insert(ShipModelTable).values({
                name, // You can also type "name: name" but this is a shorthand when the variable name is the same as the key
                classification,
                designer: designer.id
            });
        } catch (error) {
            console.error("Error creating ship model", error);
            interaction.reply({
                content: "An error occurred while creating the ship model",
                ephemeral: true
            });
            return CommandResult.Error;
        }

        await interaction.reply(`Ship model "${name}" created successfully`);
        return CommandResult.Success;
    }
}