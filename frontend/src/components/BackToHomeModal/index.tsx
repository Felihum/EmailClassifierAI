import "./index.css"

type BackToHomeModalProps = {
    backFunction: () => void,
    setModalOpen: (modalOpen: boolean) => void
}

export function BackToHomeModal(props: BackToHomeModalProps){
    return(
        <div className="backToHomeModal">
            <div className="modalContainer">
                <div className="labelContainer">
                    <h1>Voltar para o início</h1>
                    <p>Ao confirmar, a listagem de emails atual será perdida.</p>
                </div>
                
                <div>
                    <button className="cancelButton" onClick={() => props.setModalOpen(false)}>Cancelar</button>
                    <button className="backToHomeButton" onClick={props.backFunction}>Sair</button>
                </div>
            </div>
        </div>
    )
}