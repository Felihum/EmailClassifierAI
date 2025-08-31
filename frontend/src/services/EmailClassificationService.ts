import { api } from "../apiBaseURL";


// -------------- Função de upload de arquivos ------------------

export async function upload_email_file(formData: any){
    const res = await api.post("/email/upload", formData);
    
    return res.data.emails;
}

// --------------------------------------------------------------

// ------- Função de envio de email escritos na textarea --------

export async function submit_email_text(text: string){
    const res = await api.post("/email/", {"email": text});

    return res.data.emails
}

// --------------------------------------------------------------