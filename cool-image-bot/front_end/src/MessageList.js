import * as React from "react"


import Container from "@cloudscape-design/components/container"
import Grid from "@cloudscape-design/components/grid"
import { Box } from "@cloudscape-design/components"


const UserMessage = ({ msg }) =>
    <Grid
        disableGutters
        gridDefinition={[{ colspan: 11, offset: 1 }, { colspan: 5, offset: 7 }]}>
        <Container  data-sender="user"
        >
            {msg.text}</Container>
        <Box float="right" padding={{ right: "l" }} ><em>{msg.name}</em></Box>
    </Grid>

const BotMessage = ({ msg }) =>
    <Grid
        disableGutters
        gridDefinition={[{ colspan: 11, }, { colspan: 5, }]}>
        <Container       variant="stacked"
        data-sender="bot"
        >
            <div  className="bot-message" dangerouslySetInnerHTML={{ __html: msg.text }} />
            </Container>
        <Box padding={{ left: "l" }} ><em>{msg.name}</em></Box>
    </Grid>


const SystemMessage = ({ msg }) =>
    <Grid
        disableGutters
        gridDefinition={[{ colspan: 10, }, { colspan: 5 }]}>
        <Container data-sender="system"
        >            <div dangerouslySetInnerHTML={{ __html: msg.text }} />
        </Container>
        <Box float="right" padding={{ right: "l" }} ><em>{msg.name}</em></Box>
    </Grid>

const ChatMessage = ({ msg }) => {
    const sender = msg.sender
    if (sender === "user") return <UserMessage msg={msg} />
    if (sender === "bot") return <BotMessage msg={msg} />
    if (sender === "system") return <SystemMessage msg={msg} />
}


const MessageList =  ({ messages }) => {
    return messages.map(msg => <ChatMessage key={msg.text} msg={msg} />)
}

export default MessageList