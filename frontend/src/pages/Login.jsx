import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import Swal from 'sweetalert2';

export default function Login() {
    const [rut, setRut] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [cargando, setCargando] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setCargando(true);
        setError('');
        
        try {
            const response = await api.post(`/api/auth/login?rut=${rut}&password=${password}`);
            
            localStorage.setItem('token', response.data.access_token);
            localStorage.setItem('rol', response.data.id_rol);
            
            // --- LÓGICA DE REDIRECCIÓN POR ROLES ---
            const idRol = parseInt(response.data.id_rol, 10);
            
            if (idRol === 1) navigate('/directora');
            else if (idRol === 2) navigate('/jefe-programa');
            else if (idRol === 3) navigate('/gestor');
            else if (idRol === 4) navigate('/subdireccion');
            else {
                alert("Rol no reconocido");
                navigate('/');
            }

        } catch (err) {
            setError('RUT o contraseña incorrectos');
            setCargando(false);
        }
    };

    // --- NUEVA LÓGICA DE RECUPERACIÓN DE CONTRASEÑA ---
    const handleRecuperarPassword = async () => {
        // 1. Pedir el RUT
        const { value: rutRecuperacion } = await Swal.fire({
            title: 'Recuperar Contraseña',
            input: 'text',
            inputLabel: 'Ingresa tu RUT (ej: 12345678-9)',
            showCancelButton: true,
            confirmButtonText: 'Enviar Código',
            confirmButtonColor: '#1e40af',
        });

        if (!rutRecuperacion) return;

        try {
            // Solicitar código al backend
            await api.post(`/api/auth/recuperar-password?rut=${rutRecuperacion}`);
            
            // 2. Pedir el Código
            const { value: codigo } = await Swal.fire({
                title: 'Ingresa el Código',
                text: 'Revisa la terminal de tu backend (Simulador de correo)',
                input: 'text',
                showCancelButton: true,
                confirmButtonText: 'Validar Código',
                confirmButtonColor: '#1e40af',
            });

            if (!codigo) return;

            // 3. Pedir la nueva contraseña
            const { value: nuevaPassword } = await Swal.fire({
                title: 'Nueva Contraseña',
                input: 'password',
                showCancelButton: true,
                confirmButtonText: 'Guardar Contraseña',
                confirmButtonColor: '#10b981',
            });

            if (!nuevaPassword) return;

            // Enviar datos finales al backend
            await api.post('/api/auth/reset-password', {
                rut: rutRecuperacion,
                codigo: codigo,
                nueva_password: nuevaPassword
            });

            Swal.fire('¡Éxito!', 'Tu contraseña ha sido actualizada. Ya puedes iniciar sesión.', 'success');

        } catch (err) {
            Swal.fire('Error', err.response?.data?.detail || 'Hubo un problema al procesar la solicitud', 'error');
        }
    };

    return (
        <div className="absolute inset-0 bg-slate-100 z-50 flex items-center justify-center">
            
            <div className="bg-white p-10 rounded-2xl shadow-2xl w-96 max-w-md transform transition-all">
                
                <div className="text-center mb-8">
                    <div className="bg-brand-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4 shadow-inner">
                        <i className="fa-solid fa-hospital text-brand-800 text-4xl"></i>
                    </div>
                    <h2 className="text-2xl font-bold text-slate-800">CESFAM Santa Rosa</h2>
                    <p className="text-sm text-slate-500 mt-1">Plataforma de Metas e IAAPS</p>
                </div>
                
                <form onSubmit={handleLogin} className="space-y-4">
                    
                    <div>
                        <label className="block text-sm font-semibold text-slate-600 mb-1">RUT Funcionario</label>
                        <div className="relative">
                            <i className="fa-solid fa-id-card absolute left-3 top-3.5 text-slate-400"></i>
                            <input 
                                type="text" 
                                className="w-full pl-10 pr-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-colors" 
                                placeholder="12345678-9" 
                                value={rut} 
                                onChange={(e) => setRut(e.target.value)} 
                                required 
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-semibold text-slate-600 mb-1">Contraseña</label>
                        <div className="relative">
                            <i className="fa-solid fa-lock absolute left-3 top-3.5 text-slate-400"></i>
                            <input 
                                type="password" 
                                className="w-full pl-10 pr-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-colors" 
                                placeholder="••••••••" 
                                value={password} 
                                onChange={(e) => setPassword(e.target.value)} 
                                required 
                            />
                        </div>
                    </div>
                    
                    {error && (
                        <div className="text-center p-2 bg-red-50 text-red-600 border border-red-200 rounded text-sm font-semibold">
                            <i className="fa-solid fa-circle-exclamation mr-1"></i> {error}
                        </div>
                    )}

                    <div className="text-right">
                        <button 
                            type="button" 
                            onClick={handleRecuperarPassword}
                            className="text-xs text-brand-800 hover:text-brand-900 font-semibold hover:underline"
                        >
                            ¿Olvidaste tu contraseña?
                        </button>
                    </div>

                    <button 
                        type="submit" 
                        disabled={cargando}
                        className="w-full bg-brand-800 hover:bg-brand-900 text-white font-bold py-3 px-4 rounded-lg shadow-md transition-all transform hover:scale-[1.02] disabled:opacity-70 disabled:transform-none"
                    >
                        {cargando ? (
                            <span><i className="fa-solid fa-spinner fa-spin mr-2"></i> Autenticando...</span>
                        ) : (
                            <span><i className="fa-solid fa-right-to-bracket mr-2"></i> Iniciar Sesión</span>
                        )}
                    </button>
                </form>
            </div>
        </div>
    );
}