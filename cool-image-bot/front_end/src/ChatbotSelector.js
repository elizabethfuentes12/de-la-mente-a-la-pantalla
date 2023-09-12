import * as React from "react"
import Box from "@cloudscape-design/components/box"
import Button from "@cloudscape-design/components/button"
import Select from "@cloudscape-design/components/select"
import FormField from "@cloudscape-design/components/form-field"
import Container from "@cloudscape-design/components/container"
import Header from "@cloudscape-design/components/header"

const bot_label = (bot) => `${bot.botName}_${bot.botAliasName}_${bot.localeId}`

const ChatbotSelector = ({ bots, changeInteraction, postText }) => {

    const [selectedBot, setSelectedBot] = React.useState({ label: "BOT ALIAS LOCALE", value: {} });

    const changeBot = (to_bot) => {
        setSelectedBot(to_bot)
        changeInteraction(to_bot)
    }

    const sendText = async () => {
        postText(selectedBot.value.botLocaleDescription)
    }

    React.useEffect(() => {
        if (bots.length > 0) {
            let first = bots[0]
            let label = bot_label(first)
            setSelectedBot({ label: label, value: first })
            changeInteraction({label:bot_label(first), value:first})
        }
        // eslint-disable-next-line
    }, [bots])


    return (
        <Container
            header={<Header variant="h2"> Selector de Bots Activos</Header>}>
            <FormField description="Elija Amazon Lex Bot desde su cuenta" label="Seleccione Bot"    >
                <Select selectedOption={selectedBot}
                    onChange={({ detail }) => changeBot(detail.selectedOption)}
                    options={bots.map(bot => { return { label: bot_label(bot), value: bot } })}
                />
            </FormField>
            <Box variant="p" margin={{top:"m"}}>
                {selectedBot.value.botDescription}
            </Box>
            <Box variant="p" margin={{top:"m"}}>
            Intenta con: <Button onClick={sendText} variant="primary">{selectedBot.value.botLocaleDescription}</Button>
                
            </Box>
        </Container>
    )
}



export default ChatbotSelector