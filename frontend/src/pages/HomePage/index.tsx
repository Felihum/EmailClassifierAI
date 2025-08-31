import { useState } from "react";
import { EmailType } from "../../types/EmailTypes";
import "./index.css"
import { submit_email_text, upload_email_file } from "../../services/EmailClassificationService";

type HomePageProps = {
    setFile: (file: File | null) => void,
    setText: (text: string) => void,
    setResponse: (response: EmailType[] | undefined) => void,
    setCurrentType: (currentType: string) => void,
    currentType: string,
    file: File | null,
    text: string
}

export function HomePage(props: HomePageProps){
    const [isLoading, setIsLoading] = useState<boolean>(false)

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
          props.setFile(event.target.files[0]);
        }
    };
    
    const handleSubmitText = async () => {
        setIsLoading(true)
        try {
            const data = await submit_email_text(props.text)

            props.setResponse(data);
        } catch (error) {
            console.error("Erro no envio:", error);
        }
        setIsLoading(false)
    }

    const handleUpload = async () => {
        if (!props.file) {
            alert("Selecione um arquivo .txt antes de enviar!");
            return;
        }

        const formData = new FormData();
        formData.append("file", props.file);

        setIsLoading(true)

        try {
            const data = await upload_email_file(formData)

            props.setResponse(data);
        } catch (error) {
            console.error("Erro no upload:", error);
        }

        setIsLoading(false)
    };

    const handleChangeType = (event: React.ChangeEvent<HTMLSelectElement>) => {
        props.setCurrentType(event.target.value)
    }

    return(
        <div className='mainContent'>
            <section className='descriptionContainer'>
                <h1>
                    Envie seus email para categorização
                </h1>
                <p>A seguir um exemplo de como devem estar formatados os emails:</p>
                <p style={{color: "#868686ff", fontSize: ".8125rem"}}>De: exemploremetente1@gmail.com<br/>Assunto: Ajuda com um dos produto<br/>Mensagem: Preciso de ajuda com um dos produtos da empresa...</p>
                <p style={{color: "#868686ff", fontSize: ".8125rem"}}>De: exemploremetente2@gmail.com<br/>Assunto: Ajuda com um dos produto<br/>Mensagem: Preciso de ajuda com um dos produtos da empresa...</p>
            </section>
            <section className='formContainer'>
            <div className='typeInput'>
                <select name="type" onChange={handleChangeType} value={props.currentType}>
                <option value="file">Arquivo PDF ou TXT</option>
                <option value="text">Texto</option>
                </select>
            </div>
            {
                props.currentType === "file" ?
                    <div className='inputContainer'>
                        <label className='fileInput'>
                        {
                            props.file?.name === undefined ?
                                "Selecione o arquivo..."
                            :
                                props.file.name
                        }
                        <input type="file" accept=".txt, .pdf" onChange={handleFileChange} />
                        </label>
                    </div>
                :
                    <div className='inputContainer'>
                        <textarea placeholder='Escreva seus emails aqui...' onChange={(event) => props.setText(event.target.value)}></textarea>
                    </div>
            }
            {
                !isLoading ?
                    props.currentType === "file" ?
                        <button onClick={handleUpload}>
                            Enviar
                        </button>
                    :
                        <button onClick={handleSubmitText}>
                            Enviar
                        </button>
                :
                <button style={{backgroundColor:"var(--color-button-hover)", cursor:"default"}} onClick={handleSubmitText}>
                    Carregando...
                </button>
            }
            
            </section>
        </div>
    )
}