import { ChatInputCommandInteraction, SlashCommandBuilder } from "discord.js";
import { CommandHandler, CommandResult } from "../types/commandHandler";

export const helloWorldCommand: CommandHandler<ChatInputCommandInteraction<"cached">> = {
    name: "helloworld",
    interaction: new SlashCommandBuilder()
        .setName("helloworld")
        .setDescription("Says Hello, world!")
        .toJSON(),
    handler: async (interaction) => {
        await interaction.reply("Hello, world!");
        return CommandResult.Success;
    }
}
