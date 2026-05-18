import React, { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts'
import './style.css'

const API = 'http://127.0.0.1:8000/api/v1'

function App() {
  const [rates, setRates] = useState([])
  const [msg, setMsg] = useState('')

  async function load() {
    const r = await axios.get(`${API}/rates/latest`)
    setRates(r.data)
  }

  async function collect() {
    setMsg('Coletando moedas...')
    await axios.get(`${API}/rates/collect`)
    await load()
    setMsg('Coleta concluída.')
  }

  async function ai() {
    setMsg('Rodando IA avançada...')
    await axios.get(`${API}/ml/forecast-all`)
    await axios.get(`${API}/recommendations/all`)
    setMsg('Previsões e recomendações geradas.')
  }

  async function enterprise() {
    setMsg('Rodando ciclo enterprise...')
    await axios.post(`${API}/agents/run-enterprise-cycle`)
    await load()
    setMsg('Ciclo finalizado. Relatório em backend/reports.')
  }

  useEffect(() => { load() }, [])

  return (
    <main>
      <section className="hero">
        <p className="tag">AI Advanced Currency Intelligence</p>
        <h1>FX AI Hub V3</h1>
        <p>Previsão cambial, risco, recomendação de compra e integração ERP/Smart Factory.</p>
        <button onClick={collect}>Coletar</button>
        <button onClick={ai}>Rodar IA</button>
        <button onClick={enterprise}>Ciclo Enterprise</button>
        <p>{msg}</p>
      </section>
      <section className="card">
        <h2>Cotações recentes</h2>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={rates.slice(0, 20)}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="pair" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="bid" />
          </BarChart>
        </ResponsiveContainer>
      </section>
      <section className="grid">
        {rates.slice(0, 12).map((r, i) => (
          <div className="mini" key={i}>
            <strong>{r.pair}</strong>
            <span>{Number(r.bid).toFixed(6)}</span>
            <small>{r.reliability}</small>
          </div>
        ))}
      </section>
    </main>
  )
}

createRoot(document.getElementById('root')).render(<App />)
