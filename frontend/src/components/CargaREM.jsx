import { useState } from 'react';
import api from '../services/api';

export default function CargaREM() {
    const [archivo, setArchivo] = useState(null);
    // Estados para las celdas (les ponemos un valor por defecto para ayudar al usuario)
    const [celdaPob, setCeldaPob] = useState('J25');
    const [celdaComp, setCeldaComp] = useState('M40');
    
    const [resultado, setResultado] = useState(null);
    const [cargando, setCargando] = useState(false);
    const [error, setError] = useState('');

    const manejarSubida = async (e) => {
        e.preventDefault();
        if (!archivo) return setError('Selecciona un archivo Excel.');

        // Empaquetamos el archivo Y las celdas
        const formData = new FormData();
        formData.append('archivo', archivo);
        formData.append('celda_pob', celdaPob.toUpperCase());
        formData.append('celda_comp', celdaComp.toUpperCase());

        setCargando(true);
        setError('');
        
        try {
            const response = await api.post('/api/rem/carga', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            setResultado(response.data);
        } catch (err) {
            setError('Error al procesar el archivo. Revisa las celdas y el formato.');
        } finally {
            setCargando(false);
        }
    };

    return (
        <div style={{ marginTop: '20px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
            <h3>Parametrización y Carga REM</h3>
            <form onSubmit={manejarSubida} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                
                <div>
                    <label>Celda Población Diabética (Total): </label>
                    <input 
                        type="text" 
                        value={celdaPob} 
                        onChange={(e) => setCeldaPob(e.target.value)} 
                        maxLength={4}
                        required 
                    />
                </div>

                <div>
                    <label>Celda Pacientes Compensados (Logro): </label>
                    <input 
                        type="text" 
                        value={celdaComp} 
                        onChange={(e) => setCeldaComp(e.target.value)} 
                        maxLength={4}
                        required 
                    />
                </div>

                <input 
                    type="file" 
                    accept=".xlsx, .xlsm" 
                    onChange={(e) => setArchivo(e.target.files[0])} 
                />
                
                <button type="submit" disabled={cargando} style={{ padding: '10px', backgroundColor: '#0d6efd', color: 'white', border: 'none' }}>
                    {cargando ? 'Procesando Motor...' : 'Subir y Calcular IAAPS'}
                </button>
            </form>

            {error && <p style={{ color: 'red', marginTop: '15px' }}>{error}</p>}
            
            {resultado && (
                <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#d1e7dd', border: '1px solid #badbcc', borderRadius: '5px' }}>
                    <h4 style={{ color: '#0f5132', margin: '0 0 10px 0' }}>✅ {resultado.mensaje}</h4>
                    <p><strong>Población Total leída:</strong> {resultado.data.poblacion_diabetica}</p>
                    <p><strong>Logro leido:</strong> {resultado.data.pacientes_compensados}</p>
                    <hr />
                    <h3 style={{ margin: '10px 0 0 0' }}>Cumplimiento IAAPS: {resultado.data.cumplimiento_porcentual}%</h3>
                </div>
            )}
        </div>
    );
}