import * as React from "react"


import Container from "@cloudscape-design/components/container"
import Header from "@cloudscape-design/components/header"
import Input from "@cloudscape-design/components/input"
import Grid from "@cloudscape-design/components/grid"

import Button from "@cloudscape-design/components/button"
import { Box } from "@cloudscape-design/components";
import MessageList from "./MessageList";

export default React.forwardRef(({ user, postText }, ref) => {
    const [chat, setChat] = React.useState([]);
    const [inputValue, setInputValue] = React.useState("");
    const [sending, setSending] = React.useState(false);

    const sendText = async () => {
        //console.log(inputValue)
        setChat(prev => [...prev, { text: inputValue, sender: "user", name: "Demo User" }])
        setInputValue("")
        setSending(true)
        const respuesta = await postText(inputValue)
        setSending(false)

        setChat(prev => [...prev, respuesta])
    }

    const sendAutoText = async (text) => {
        //console.log(inputValue)
        setChat(prev => [...prev, { text: text, sender: "user", name: "Demo User" }])
        setSending(true)
        const respuesta = await postText(text)
        setSending(false)
        setChat(prev => [...prev, respuesta])
    }
    React.useImperativeHandle(ref, () => ({
        sendAutoText,
    }))


    React.useEffect(() => {
        const element = document.querySelector('[data-id="chat-window"]')
        element.firstChild.firstChild.firstChild.scrollTop = element.firstChild.firstChild.firstChild.scrollHeight
    }, [chat])


    React.useEffect(() => {
        if (sending === false) {
            const element = document.querySelector('[data-id="chat-input"] > input')
            if (element) {
                element.focus()
            }
        }

    }, [sending])

    const processKeyUp = (keyCode) => {
        //console.log(keyCode)
        if (keyCode === 13) {
            sendText()
        }

    }

    return (
        <Container
            header={<Header variant="h2">Conversacion</Header>}>
            <Box margin={{ bottom: "m" }} data-id="chat-window">
                <Container fitHeight>
                    <MessageList messages={chat} />
                </Container>
            </Box>

            <Grid
                gridDefinition={[{ colspan: {default:11,   } }, { colspan: { default:1, } }]}
            >
                <Input value={inputValue} data-id="chat-input"
                    onKeyUp={event => processKeyUp(event.detail.keyCode)}
                    onChange={event => setInputValue(event.detail.value)}
                    disabled={sending}
                    
                />
                <Button disabled={sending} onClick={sendText} iconName="angle-up" variant="primary"></Button>
            </Grid>
        </Container>
    )
})

