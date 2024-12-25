import { AutocompleteInteraction, Interaction, RESTPostAPIChatInputApplicationCommandsJSONBody } from "discord.js";

export type CommandHandler<T extends Interaction> = {
    name: string,
    interaction: RESTPostAPIChatInputApplicationCommandsJSONBody,
    autocomplete?: (interaction: AutocompleteInteraction<"cached">) => Promise<CommandResult>,
    handler: (interaction: T) => Promise<CommandResult>
}

export enum CommandResult {
    Success, // Command was successful
    Failure, // Command was rejected
    Error // Error occurred while processing command
}