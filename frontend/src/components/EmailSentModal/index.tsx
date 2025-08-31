import { ElementType } from "react";
import "./index.css"
import { CiCircleCheck } from "react-icons/ci";
import { MdOutlineErrorOutline } from "react-icons/md";

const CheckIcon: ElementType = CiCircleCheck as ElementType;
const ErrorIcon: ElementType = MdOutlineErrorOutline as ElementType;

type EmailSentModalProps = {
    sent: boolean
}

export function EmailSentModal(props: EmailSentModalProps){
    return(
        <div className="emailSentModal">
            {
                props.sent ?
                    <div className="labelModalContainer">
                        <div style={{color: "rgb(106, 255, 106)"}}>
                            <CheckIcon />
                        </div>
                        
                        <p style={{color: "rgb(106, 255, 106)"}}>Email enviado com sucesso</p>
                    </div>
                :
                    <div className="labelModalContainer">
                        <div style={{color: "red"}}>
                            <ErrorIcon />
                        </div>
                        
                        <p style={{color: "red"}}>Informações de envio de email incorretas</p>
                    </div>
            }
            
        </div>
    )
}