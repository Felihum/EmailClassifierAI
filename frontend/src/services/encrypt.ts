import { api } from "../apiBaseURL";
import JSEncrypt from "jsencrypt";

// --- Função de Criptografia para envio da senha de app do email ao backend ---

export async function encrypt(password: string){
    try{
        const response = await api.get("/public-key")

        const publicKey = response.data.publicKey

        const encryptor = new JSEncrypt();
        encryptor.setPublicKey(publicKey);

        const encrypted = encryptor.encrypt(password);

        if (!encrypted) {
            alert("Erro ao criptografar");
            return;
        }

        return encrypted
    } catch(error: any){
        throw error
    }
}

// -----------------------------------------------------------------------------