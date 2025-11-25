import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function App() {
  const [query, setQuery] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [context, setContext] = useState({})
  const [showContextEditor, setShowContextEditor] = useState(false)
  const [contextInput, setContextInput] = useState('')
  const [presets, setPresets] = useState([])
  const [selectedPreset, setSelectedPreset] = useState('')
  const [sessionId, setSessionId] = useState(null)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    loadPresets()
    loadCurrentContext()
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const loadPresets = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/presets`)
      setPresets(response.data)
    } catch (error) {
      console.error('Failed to load presets:', error)
    }
  }

  const loadCurrentContext = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/context`)
      setContext(response.data.context)
      setContextInput(JSON.stringify(response.data.context, null, 2))
    } catch (error) {
      console.error('Failed to load context:', error)
    }
  }

  const handlePresetChange = async (presetName) => {
    if (!presetName) return
    
    try {
      const response = await axios.post(`${API_BASE_URL}/api/presets/${presetName}/apply`)
      setContext(response.data.context)
      setContextInput(JSON.stringify(response.data.context, null, 2))
      setSelectedPreset(presetName)
      
      // Add system message showing context change
      setMessages(prev => [...prev, {
        role: 'system',
        content: `Context changed to "${presetName}" mode`
      }])
    } catch (error) {
      console.error('Failed to apply preset:', error)
      alert('Failed to apply preset')
    }
  }

  const handleContextUpdate = async () => {
    try {
      const contextData = JSON.parse(contextInput)
      await axios.post(`${API_BASE_URL}/api/context`, {
        context: contextData,
        merge: true
      })
      setContext(contextData)
      setShowContextEditor(false)
      alert('Context updated successfully')
    } catch (error) {
      alert('Invalid JSON or failed to update context')
      console.error('Context update error:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!query.trim() || loading) return

    const userMessage = query.trim()
    setQuery('')
    setLoading(true)

    // Add user message to UI
    const newMessages = [...messages, { role: 'user', content: userMessage }]
    setMessages(newMessages)

    try {
      // Determine context override (if context editor was used)
      const contextOverride = showContextEditor && contextInput ? 
        (() => {
          try {
            return JSON.parse(contextInput)
          } catch {
            return null
          }
        })() : null

      const response = await axios.post(`${API_BASE_URL}/api/query`, {
        query: userMessage,
        context: contextOverride,
        session_id: sessionId
      })

      setSessionId(response.data.session_id)
      setMessages(prev => [...prev, { role: 'assistant', content: response.data.response }])
    } catch (error) {
      console.error('Query error:', error)
      setMessages(prev => [...prev, {
        role: 'error',
        content: 'Sorry, I encountered an error. Please try again.'
      }])
    } finally {
      setLoading(false)
    }
  }

  const clearContext = async () => {
    try {
      await axios.delete(`${API_BASE_URL}/api/context`)
      setContext({})
      setContextInput('{}')
      setSelectedPreset('')
    } catch (error) {
      console.error('Failed to clear context:', error)
    }
  }

  const clearMessages = () => {
    setMessages([])
  }

  return (
    <div className="app-container">
      <div className="chat-container">
        <div className="header">
          <h1>SmartAdvisor</h1>
          <div className="header-actions">
            <select
              value={selectedPreset}
              onChange={(e) => handlePresetChange(e.target.value)}
              className="preset-selector"
            >
              <option value="">Select Mode...</option>
              {presets.map(preset => (
                <option key={preset.id} value={preset.name}>
                  {preset.name.charAt(0).toUpperCase() + preset.name.slice(1)} - {preset.description}
                </option>
              ))}
            </select>
            <button
              onClick={() => setShowContextEditor(!showContextEditor)}
              className="btn btn-secondary"
            >
              {showContextEditor ? 'Hide' : 'Edit'} Context
            </button>
            <button onClick={clearContext} className="btn btn-secondary">
              Clear Context
            </button>
          </div>
        </div>

        {showContextEditor && (
          <div className="context-editor">
            <h3>Business Context</h3>
            <textarea
              value={contextInput}
              onChange={(e) => setContextInput(e.target.value)}
              placeholder='{"role": "Advisor", "mode": "General", "instructions": ["Be helpful"]}'
              rows="6"
            />
            <button onClick={handleContextUpdate} className="btn btn-primary">
              Update Context
            </button>
          </div>
        )}

        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="welcome-message">
              <h2>Welcome to SmartAdvisor</h2>
              <p>Ask me anything, and I'll help you with your business needs.</p>
              <p>You can select a mode or customize the context to tailor my responses.</p>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                {msg.role === 'user' && <div className="message-label">You</div>}
                {msg.role === 'assistant' && <div className="message-label">SmartAdvisor</div>}
                {msg.role === 'system' && <div className="message-label">System</div>}
                <div className="message-content">{msg.content}</div>
              </div>
            ))
          )}
          {loading && (
            <div className="message assistant">
              <div className="message-label">SmartAdvisor</div>
              <div className="message-content loading">Thinking...</div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask your question..."
            disabled={loading}
            className="query-input"
          />
          <button type="submit" disabled={loading || !query.trim()} className="btn btn-primary">
            Send
          </button>
          {messages.length > 0 && (
            <button type="button" onClick={clearMessages} className="btn btn-secondary">
              Clear
            </button>
          )}
        </form>
      </div>
    </div>
  )
}

export default App

