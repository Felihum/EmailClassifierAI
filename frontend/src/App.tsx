import { ChangeEventHandler, useState } from 'react';
import './App.css';
import { api } from './apiBaseURL';
import { EmailPage } from './pages/EmailPage';
import { EmailType } from './types/EmailTypes';
import { EmailsTablePage } from './pages/EmailsTablePage';
import { HomePage } from './pages/HomePage';

function App() {
  const [text, setText] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);
  const [response, setResponse] = useState<EmailType[] | undefined>();
  const [currentType, setCurrentType] = useState<string>("file")
  const [selectedEmail, setSelectedEmail] = useState<EmailType>()

  const handleSelectEmail = (email: EmailType) => {
    setSelectedEmail(email)
    console.log(email)
  }

  const backToHome = () => {
    setResponse(undefined)
  }

  const backToEmailsList = () => {
    setSelectedEmail(undefined)
  }

  if(response === undefined){
    return(
      <HomePage 
        setFile={setFile}
        setText={setText}
        setResponse={setResponse}
        setCurrentType={setCurrentType}
        currentType={currentType}
        file={file}
        text={text}
      />
    )
  } else if(response !== undefined && selectedEmail === undefined){
    return(
      <EmailsTablePage 
        emails={response}
        handleSelectEmail={handleSelectEmail}
        backFunction={backToHome}
      />
    )
  } else if(response !== undefined && selectedEmail !== undefined){
    return(
      <div className='emailPage'>
        <label onClick={() => backToEmailsList()} className='backButton'>Voltar</label>
        <EmailPage 
          email={selectedEmail}
        />
      </div>
      
    )
  } else{
    return null
  }
  
}

export default App;
