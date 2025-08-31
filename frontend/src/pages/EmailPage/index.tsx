import { useState } from "react"
import { encrypt } from "../../services/encrypt"
import { send_email } from "../../services/SendEmailService"
import { EmailType, SendEmailType } from "../../types/EmailTypes"
import "./index.css"
import { EmailSentModal } from "../../components/EmailSentModal"

type EmailPageProps = {
    email: EmailType
}

export function EmailPage(props: EmailPageProps){

    const [isSendingEmail, setIsSendingEmail] = useState<boolean>(false)
    const [sentConfirmed, setSentConfirmed] = useState<boolean>(false)
    const [sentRejected, setSentRejected] = useState<boolean>(false)
    const [message, setMessage] = useState<string>(props.email.suggestion)

    async function handleSendEmail(){
        try{
            setIsSendingEmail(true)

            const sendEmailData: SendEmailType = {
                recipient: props.email.sender,
                sender: localStorage.getItem("sender") as string,
                password: await encrypt(localStorage.getItem("password") as string) as string,
                message: message
            }

            await send_email(sendEmailData)
            setIsSendingEmail(false)

            setSentConfirmed(true)

            setTimeout(() => {
                setSentConfirmed(false)
            }, 5000)
        } catch(error: any){
            if(error.status === 500){
                setIsSendingEmail(false)

                setSentRejected(true)

                setTimeout(() => {
                    setSentRejected(false)
                }, 5000)
            }
        }
        
    }

    return(
        <div className="emailPageContainer">
            {
                sentConfirmed && <EmailSentModal sent={true} />
            }
            {
                sentRejected && <EmailSentModal sent={false} />
            }
            <div className="headerContainer">
                <h1>Visualização de Email</h1>
                {
                    props.email.classification === "Produtivo" ?
                        <label style={{backgroundColor: "var(--color-green)", padding: ".9375rem", borderRadius: ".3125rem", border: "none"}}>Produtivo</label>
                    :
                        <label style={{backgroundColor: "var(--color-red)", padding: ".9375rem", borderRadius: ".3125rem", border: "none"}}>Improdutivo</label>
                }
            </div>
            <p>Remetente: {props.email.sender}</p>
            <div className="textAreaField">
                <label>Resposta Sugerida:</label>
                <textarea name="" id="" defaultValue={props.email.suggestion} onChange={(event) => setMessage(event.target.value)}/>
            </div>

            <div className="textAreaField">
                <label>Mensagem Analisada:</label>
                <textarea name="" id="" value={props.email.message} readOnly />
            </div>
            {
                isSendingEmail ?
                    <button style={{backgroundColor: "var(--color-button-hover)"}}>Enviando Email...</button>
                :
                    <button onClick={handleSendEmail}>Enviar Email</button>
            }
        </div>
    )
}