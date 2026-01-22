import React from 'react'
import UploadForm from './components/UploadForm'
import './App.css'

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h1>PPT Generator - Phase 1</h1>
                <p>Dummy Mode: No real AI calls yet.</p>
            </header>
            <main>
                <UploadForm />
            </main>
        </div>
    )
}

export default App
