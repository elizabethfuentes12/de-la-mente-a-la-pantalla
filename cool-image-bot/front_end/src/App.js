
import './App.css';
import * as React from "react"
import {
  Routes,
  Route,
  Outlet,

} from "react-router-dom"
import { Amplify} from 'aws-amplify';
import { AWSLexV2Provider } from '@aws-amplify/interactions';
import awsconfig from './aws-exports';


import Home from './Home'
import AppLayout from "@cloudscape-design/components/app-layout"
import AppTopNavigation from "./AppTopNavigation"


import { listBots } from './botsAPI'

Amplify.configure(awsconfig)


const convert_bot_dict = (botList) => {
  let bot_dict = {}
  botList.forEach(bot => {
    bot_dict[`${bot.botName}_${bot.botAliasName}_${bot.localeId}`] = {
      name: `${bot.botName}_${bot.botAliasName}_${bot.localeId}`,
      aliasId: bot.botAliasId,
      botId: bot.botId,
      localeId: bot.localeId,
      region: awsconfig.aws_cognito_region,
      providerName: "AWSLexV2Provider"
    }

  })
  return bot_dict
}

Amplify.addPluggable(new AWSLexV2Provider());


const App = ({ signOut, user }) => {
  const [bots, setBots] = React.useState([]);


  React.useEffect(() => {
    listBots({ region:awsconfig.aws_cognito_region }).then(bots => {
      setBots([...bots])
      const bot_dict = convert_bot_dict(bots)
      
      const interactionsConfig = {
        Auth: { identityPoolId: awsconfig.aws_cognito_identity_pool_id, region: awsconfig.aws_cognito_region },
        Interactions: { bots: bot_dict }
      }
      Amplify.configure(interactionsConfig)

    }).catch(err => console.log("error:", err))
  

  }, [user])



  return (

    <Routes>
      <Route path="/" element={<Layout signOut={signOut} user={user} />}>

        <Route index element={<Home user={user} bots={bots} />} />

      </Route>
    </Routes>

  )

}


const Layout = (props) => [

  <AppTopNavigation key={1} signOut={props.signOut} user={props.user ? props.user:null} />,
  <AppLayout key={2}
    headerSelector="#h"
    toolsHide={true}
    disableContentPaddings={true}
    navigationHide={true}
    footerSelector="#f"
    content={<Outlet />}

  />

]

//export default withAuthenticator(App)
export default App