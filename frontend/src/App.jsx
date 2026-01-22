import React from 'react'
import UploadForm from './components/UploadForm'
import './App.css'

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h1>AI PowerPoint Generator</h1>
                <p>Turn bulk text into structured PowerPoint presentations.</p>
            </header>
            <main>
                <UploadForm />
            </main>
        </div>
    )
}

export default App
