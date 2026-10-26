import { useNavigate } from 'react-router-dom';

export default function Sidebar() {
    const navigate = useNavigate();
    const rolActual = parseInt(localStorage.getItem('rol'), 10);

    const cerrarSesion = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('rol');
        navigate('/');
    };

    return (
        <div className="w-72 bg-sidebar text-slate-300 flex-shrink-0 flex flex-col h-full">
            <div className="p-6 border-b border-slate-700 flex items-center space-x-3">
                <i className="fa-solid fa-notes-medical text-brand-500 text-2xl"></i>
                <span className="text-lg font-bold text-white tracking-wider">CESFAM APP</span>
            </div>
            
            <div className="overflow-y-auto flex-grow p-4 space-y-6">
                
                {/* 1. Menú Directora */}
                {rolActual === 1 && (
                    <div>
                        <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 ml-3">Directorio</p>
                        <button onClick={() => navigate('/directora')} className="w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-white bg-slate-800 hover:bg-slate-700 transition-colors">
                            <i className="fa-solid fa-chart-pie w-5 text-center"></i> <span>Dashboard Global</span>
                        </button>
                    </div>
                )}

                {/* 2. Menú Jefe Programa */}
                {rolActual === 2 && (
                    <div>
                        <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 ml-3">Áreas Clínicas</p>
                        <button onClick={() => navigate('/jefe-programa')} className="w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-white bg-slate-800 hover:bg-slate-700 transition-colors">
                            <i className="fa-solid fa-heart-pulse w-5 text-center"></i> <span>Mi Programa</span>
                        </button>
                    </div>
                )}

                {/* 4. Menú Subdirección */}
                {rolActual === 4 && (
                    <div>
                        <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 ml-3">Operaciones</p>
                        <button onClick={() => navigate('/subdireccion')} className="w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-white bg-slate-800 hover:bg-slate-700 transition-colors">
                            <i className="fa-solid fa-file-excel w-5 text-center"></i> <span>Carga REM (.xlsm)</span>
                        </button>
                    </div>
                )}

                {/* 3. Menú Gestor (Core) */}
                {rolActual === 3 && (
                    <div>
                        <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 ml-3">Administración Core</p>
                        <button onClick={() => navigate('/gestor')} className="w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-white bg-slate-800 hover:bg-slate-700 transition-colors mb-1">
                            <i className="fa-solid fa-cogs w-5 text-center"></i> <span>Parametrización y PIV</span>
                        </button>
                    </div>
                )}
            </div>

            <div className="p-4 border-t border-slate-700">
                <div className="flex items-center space-x-3 mb-4 px-2">
                    <div className="w-8 h-8 rounded-full bg-brand-500 flex items-center justify-center text-white font-bold text-sm">US</div>
                    <div>
                        <p className="text-sm font-semibold text-white">Usuario Activo</p>
                        <p className="text-xs text-slate-400">Rol ID: {rolActual}</p>
                    </div>
                </div>
                <button onClick={cerrarSesion} className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-slate-800 hover:bg-red-600 hover:text-white rounded-lg transition-colors text-sm font-semibold">
                    <i className="fa-solid fa-power-off"></i> <span>Cerrar Sesión</span>
                </button>
            </div>
        </div>
    );
}