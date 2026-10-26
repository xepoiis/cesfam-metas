import { Navigate, Outlet } from 'react-router-dom';

export default function ProtectedRoute({ rolesPermitidos }) {
    const token = localStorage.getItem('token');
    const rolActual = parseInt(localStorage.getItem('rol'), 10);

    if (!token) return <Navigate to="/" replace />;
    
    if (rolesPermitidos && !rolesPermitidos.includes(rolActual)) {
        alert("Acceso denegado");
        return <Navigate to="/" replace />; 
    }
    return <Outlet />;
}