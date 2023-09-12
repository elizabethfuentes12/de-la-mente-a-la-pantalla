import {
    LexModelsV2Client,
    ListBotsCommand,
    ListBotLocalesCommand,
    ListBotAliasesCommand,
} from "@aws-sdk/client-lex-models-v2";

import { LexRuntimeV2Client, DeleteSessionCommand } from "@aws-sdk/client-lex-runtime-v2"; // ES Modules import
import { Auth } from 'aws-amplify';


export const listBots = async ({ region }) => {
    const creds = await Auth.currentUserCredentials()
    const lexclient = new LexModelsV2Client({ region: region, credentials: creds })
    const input = { sortBy: { attribute: "BotName", order: "Ascending" } }
    const command = new ListBotsCommand(input)
    const response = await lexclient.send(command)
    const bots = response.botSummaries.filter(bot => bot.botStatus === "Available" && bot.botName.includes("cool"))

    const botsWithAliases = await Promise.all(bots.map(async bot => {
        const aliases = await getBotAliases({ client: lexclient, botId: bot.botId })
        bot.aliases = aliases
        return bot
    }))
    //console.log(bots)
    //console.log("BotsWA", botsWithAliases)

    const botsFlatten = []

    botsWithAliases.forEach(bot => {
        bot.aliases.forEach(alias => {
            alias.locales.forEach(loc => {
                botsFlatten.push(
                    {
                        botId: bot.botId,
                        botName: bot.botName,
                        botDescription: bot.description,
                        botAliasId: alias.botAliasId,
                        botAliasName: alias.botAliasName,
                        botAliasBotVersion: alias.botVersion,
                        botAliasDescription: alias.description,
                        botLocaleDescription: loc.description,
                        localeId: loc.localeId,
                        localeName: loc.localeName
                    })
            })
        })
    })

    return botsFlatten
}


const getBotAliases = async ({ botId, client }) => {
    const command = new ListBotAliasesCommand({ botId: botId })
    const response = await client.send(command)
    const aliases = response.botAliasSummaries.filter(alias => alias.botAliasStatus === "Available")

    const aliasesWithLocales = await Promise.all(aliases.map(async alias => {
        const locales = await getBotLocales({ client: client, botId: botId, botVersion: alias.botVersion })
        alias.locales = locales
        return alias
    }))
    return aliasesWithLocales
}

const getBotLocales = async ({ botId, botVersion, client }) => {
    const command = new ListBotLocalesCommand({ botId: botId, botVersion: botVersion })
    const response = await client.send(command)
    const locales = response.botLocaleSummaries.filter(loc => loc.botLocaleStatus === "Built")
    return locales
}



// https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/client/lex-runtime-v2/command/DeleteSessionCommand/

export const deleteSession = async ({ region, bot, sessionId }) => {
    const creds = await Auth.currentUserCredentials()
    const client = new LexRuntimeV2Client({ region: region, credentials: creds })


    const input = { // DeleteSessionRequest
        botId: bot.botId, // required
        botAliasId: bot.botAliasId, // required
        localeId: bot.localeId, // required
        sessionId: sessionId, // required
    };
    const command = new DeleteSessionCommand(input);
    const response = await client.send(command);
    return response
}

