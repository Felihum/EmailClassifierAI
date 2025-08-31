import { useEffect, useState } from "react"
import { PreferencesModal } from "../../components/PreferencesModal"
import { EmailType } from "../../types/EmailTypes"
import "./index.css"
import { BackToHomeModal } from "../../components/BackToHomeModal"

type EmailsTablePageProps = {
    emails: EmailType[],
    backFunction: () => void,
    handleSelectEmail: (email: EmailType) => void
}

export function EmailsTablePage(props: EmailsTablePageProps){
    const filters = ["Todos", "Produtivo", "Improdutivo"]
    const [selectedFilter, setSelectedFilter] = useState<string>(filters[0])
    const [modalOpen, setModalOpen] = useState<boolean>(false)
    const [backModalOpen, setBackModalOpen] = useState<boolean>(false)
    const [emails, setEmails] = useState<EmailType[]>()

    useEffect(() => {
        if(selectedFilter === "Todos"){
            setEmails(props.emails)
        } else{
            setEmails(props.emails.filter(e => e.classification === selectedFilter))
        }
        
    }, [selectedFilter])

    return(
        <div className='tableContainer'>
            {
                modalOpen && <PreferencesModal setModalOpen={setModalOpen} />
            }
            {
                backModalOpen && <BackToHomeModal setModalOpen={setBackModalOpen} backFunction={props.backFunction} />
            }
            <label className="openModalButton" onClick={() => setModalOpen(true)}>Configurar Preferências</label>
            <label onClick={() => setBackModalOpen(true)} className='backButton'>Voltar</label>
            <h1>Emails analisados</h1>
            <p>Veja a lista dos emails analisados pela inteligência artificial, sua classificação e a resposta sugerida.<br /> Clique para ver mais detalhes.</p>
            <div className="filterContainer">
                 <div className="filterInputsContainer">
                    {
                        filters.map((filter) => (
                            <div>
                                <input
                                    type="radio"
                                    name="filtro"
                                    value={filter}
                                    checked={filter === selectedFilter}
                                    onChange={(e) => setSelectedFilter(e.target.value)}
                                />
                                <label>{filter}</label>
                            </div>
                            
                        ))
                    }
                </div>
            </div>
            <table>
                <thead>
                    <tr>
                    <th>Remetente</th>
                    <th>Resposta Sugerida</th>
                    <th>Mensagem</th>
                    <th>Categoria</th>
                    </tr>
                </thead>
                <tbody>
                    {
                    emails && emails.map((email) => (
                        <tr onClick={() => props.handleSelectEmail(email)}>
                            <td>{email.sender}</td>
                            <td>{email.suggestion}</td>
                            <td>{email.message}</td>
                            {
                                email.classification === "Improdutivo" ?
                                <td style={{backgroundColor: "var(--color-red)"}}>{email.classification.toUpperCase()}</td>
                                :
                                <td style={{backgroundColor: "var(--color-green)"}}>{email.classification.toUpperCase()}</td>
                            }
                        </tr>
                    ))
                    }
                </tbody>
            </table>
        </div>
    )
}