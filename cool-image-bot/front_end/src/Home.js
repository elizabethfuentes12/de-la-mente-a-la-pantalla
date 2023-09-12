import * as React from "react"
import "@cloudscape-design/global-styles/index.css"
import Grid from "@cloudscape-design/components/grid"
import Box from "@cloudscape-design/components/box"
import { Interactions } from 'aws-amplify'
import { deleteSession } from './botsAPI'
import "./Home.css"
import ChatbotSelector from "./ChatbotSelector"
import ChatConversation from "./ChatConversation"
import awsconfig from './aws-exports'


//console.log(Interactions)

const Home = ({ user, bots }) => {

    const [currentBot, setCurrentBot] = React.useState({ label: "NAME", value: {} })
    const [sessionId, setSessionId] = React.useState(null)

    const conversationRef = React.useRef(null)

    const changeBot = (bot) => {
        console.log("bot changed to:", bot)
        if (sessionId) {
            deleteSession({
                bot: currentBot.value,
                sessionId: sessionId,
                region: awsconfig.aws_cognito_region
            }).then(data => console.log("deletesession:", data)).catch(e => console.log(e))
            console.log("borrando sesion")
            setSessionId(null)
        }
        setCurrentBot({ ...bot })

    }

    React.useEffect(() => {
        if (currentBot.label !== "NAME") {
            console.log("useEffect", currentBot)
            console.log("session:", sessionId)

            if (conversationRef.current)
                if (currentBot.value.botLocaleDescription !== undefined) return
                    conversationRef.current.sendAutoText(currentBot.value.botLocaleDescription)
        }
        // eslint-disable-next-line
    }, [currentBot])

    const sendAutoText = async (text) => {
        conversationRef.current.sendAutoText(text)
    }


    const obtieneRespuesta = async (text) => {
        const response = await Interactions.send(currentBot.label, text)
        setSessionId(response.sessionId)
        console.log("sessionId", response.sessionId)
        return { text: response.messages[0].content, sender: "bot", name: currentBot.label }
    }

    return [
        <Grid key={2}
            disableGutters
            gridDefinition={[

                { colspan: { default: 12, s: 4, m: 3, l: 3 }, offset: { default: 0, s: 1, l: 2 } },
                { colspan: { default: 12, s: 6, m: 7, l: 5 } },
            ]}
        >
            <Box margin={{ top: "xl", right: "xl" }}><ChatbotSelector bots={bots} postText={sendAutoText} changeInteraction={changeBot} /></Box>
            <Box margin={{ top: "xl", right: "xl" }} ><ChatConversation ref={conversationRef} postText={obtieneRespuesta} user={user} /></Box>

        </Grid>
    ]

}


export default Home

