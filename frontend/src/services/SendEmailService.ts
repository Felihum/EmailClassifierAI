import { FormEvent } from "react";
import { SendEmailType } from "../types/EmailTypes";
import { api } from "../apiBaseURL";

// ---------- Função para salvar preferências de envio de email ----------
export function set_preferences(event: FormEvent<HTMLFormElement>){
    const formData = new FormData(event.currentTarget)

    const sender = formData.get("sender") as string
    const password = formData.get("password") as string

    sessionStorage.setItem("sender", sender)
    sessionStorage.setItem("password", password)
}
// -----------------------------------------------------------------------

// ------------------- Função de envio de email --------------------------
export async function send_email(data: SendEmailType){
    try{
        const response = await api.post("/submit", data)

        console.log(response.data)
    } catch(error: any){
        throw error
    }
}

// -----------------------------------------------------------------------