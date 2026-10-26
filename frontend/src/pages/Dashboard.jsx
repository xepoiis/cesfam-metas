import { useNavigate } from 'react-router-dom';
import CargaREM from '../components/CargaREM';

export default function Dashboard() {
    const navigate = useNavigate();
    const rol = localStorage.getItem('rol');

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('rol');
        navigate('/');
    };

    return (
        <div style={{ padding: '50px', maxWidth: '800px', margin: '0 auto' }}>
            <h2>Panel de Control CESFAM</h2>
            <p>ID de Rol actual: {rol}</p>
            
            <CargaREM />

            <button 
                onClick={handleLogout} 
                style={{ marginTop: '20px', backgroundColor: '#dc3545', color: 'white', padding: '10px' }}
            >
                Cerrar Sesión
            </button>
        </div>
    );
}