import { FormEvent } from "react"
import { set_preferences } from "../../services/SendEmailService"
import "./index.css"

type PreferencesModalProps = {
    setModalOpen: (modalOpen: boolean) => void
}

export function PreferencesModal(props: PreferencesModalProps){
    const handleSetPreferences = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        set_preferences(event)
        props.setModalOpen(false)
    }

    return(
        <div className="preferencesModalBg">
            <main>
                <div className="modalLabelContainer">
                    <h1>Preferências</h1>
                    <p>Configure suas preferências</p>
                </div>
                <form onSubmit={handleSetPreferences}>
                    <div>
                        <label>Email de Envio</label>
                        <input type="email" defaultValue={sessionStorage.getItem("sender") as string} name="sender" />    
                    </div>
                    <div>
                        <label>Senha de Aplicativo do Email</label>
                        <input type="password" defaultValue={sessionStorage.getItem("password") as string} name="password" />
                    </div>
                    <div style={{display: "flex", flexDirection: "row", justifyContent: "center", alignItems: "center"}}>
                        <button className="cancelPreferenceButton" onClick={() => props.setModalOpen(false)}>Cancelar</button>
                        <button className="savePreferenceButton"type="submit">Salvar Preferências</button>
                    </div>
                </form>
            </main>
        </div>
    )
}