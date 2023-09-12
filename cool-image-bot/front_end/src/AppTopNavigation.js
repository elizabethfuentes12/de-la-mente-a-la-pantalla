
import * as React from "react"
import TopNavigation from "@cloudscape-design/components/top-navigation"
import { Auth } from 'aws-amplify'



const AppTopNavigation =  (props) => {

  const userName = props.user ? props.user.attributes.name : "Usuario"
  const userEmail = props.user ? props.user.attributes.naemailme : "email@example.com"

  const logout = async () => {

    console.log('Logout')

    try {
      await Auth.signOut({ global: true })
    } catch (error) {
      console.log('error signing out: ', error)
    }
  }


  return (
    <div>

      <TopNavigation
        identity={{
          href: "/",
          title: "Amazon Lex Front End - Demo",
        }}
        utilities={[
          {
            type: "menu-dropdown",
            text: "Hola " + userName,
            description: "Area de Usuario",
            iconName: "user-profile",
            items: [
              { id: "email", text: userEmail }
            ]
          },
          {
            type: "button",
            text: "Salir",
            onClick: (() => { logout() })
          }
        ]}
        i18nStrings={{
          searchIconAriaLabel: "Search",
          searchDismissIconAriaLabel: "Close search",
          overflowMenuTriggerText: "More",
          overflowMenuTitleText: "All",
          overflowMenuBackIconAriaLabel: "Back",
          overflowMenuDismissIconAriaLabel: "Close menu"
        }}
      />
    </div>

  )
}

export default AppTopNavigation