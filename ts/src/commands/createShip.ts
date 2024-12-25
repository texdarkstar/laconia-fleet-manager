import { ChatInputCommandInteraction, SlashCommandBuilder } from "discord.js";
import { CommandHandler, CommandResult } from "../types/commandHandler";
import { db } from "../db/drizzleClient";
import { ShipTable } from "../db/schema";

export const createShipCommand: CommandHandler<ChatInputCommandInteraction<"cached">> = {
    name: "createship",
    interaction: new SlashCommandBuilder()
        .setName("createship")
        .setDescription("Creates a ship")
        .addStringOption(option => option
            .setName("name")
            .setDescription("The name of the ship")
            .setRequired(true))
        .addStringOption(option => option
            .setName("model")
            .setDescription("The model of the ship")
            // This means discord will send an autocomplete request to the bot when the user types the command
            .setAutocomplete(true) 
            .setRequired(true))
        .addStringOption(option => option
            .setName("shipyard")
            .setDescription("The shipyard the ship was built in")
            .setAutocomplete(true)
            .setRequired(true))
        .addUserOption(option => option
            .setName("assignedto")
            .setDescription("The user the ship is assigned to")
            .setRequired(false)) // Optional parameter
        .addStringOption(option => option
            .setName("location")
            .setDescription("The location of the ship")
            .setRequired(false)) // Optional parameter
        .setContexts(0) // This means the command is only available in guilds
        .toJSON(),
    autocomplete: async (interaction) => {
        // We run this when the user types the command to get the list of ship models
        const focusedOption = interaction.options.getFocused(true);
        console.log("createship autocomplete, focusedOption: ", focusedOption);
        console.log(interaction);
        if (focusedOption.name === "model") {
            // We return the list of ship models
            const models = await db.query.ShipModelTable.findMany();
            interaction.respond(models.map(model => ({ name: model.name, value: model.id.toString() })))
            return CommandResult.Success;
        }
        if (focusedOption.name === "shipyard") {
            // We return the list of shipyards
            const shipyards = await db.query.ShipyardTable.findMany();
            interaction.respond(shipyards.map(shipyard => ({ name: shipyard.name, value: shipyard.id.toString() })))
            return CommandResult.Success;
        }
        return CommandResult.Success;
    },
    handler: async (interaction) => {
        const name = interaction.options.getString("name")!;
        const model = interaction.options.getString("model")!;
        const shipyard = interaction.options.getString("shipyard")!;
        const assignedTo = interaction.options.getUser("assignedto");
        const location = interaction.options.getString("location");

        const modelId = Number.parseInt(model);
        const shipyardId = Number.parseInt(shipyard);

        if (Number.isNaN(modelId) || Number.isNaN(shipyardId)) {
            await interaction.reply("Invalid model or shipyard");
            return CommandResult.Failure;
        }

        try {
            await db.insert(ShipTable).values({
                name,
                modelId,
                shipyardId,
                assignedTo: assignedTo?.id,
                location
            })
        } catch (error) {
            console.error("Error creating ship", error);
            interaction.reply({
                content: "An error occurred while creating the ship",
                ephemeral: true
            });
            return CommandResult.Error;
        }

        await interaction.reply(`Ship "${name}" created successfully`);
        return CommandResult.Success;
    }
}
