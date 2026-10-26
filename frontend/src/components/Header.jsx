export default function Header() {
    return (
        <header className="bg-white shadow-sm border-b border-slate-200 h-16 flex items-center justify-between px-8 flex-shrink-0">
            <h1 className="text-xl font-bold text-slate-800">Panel de Control CESFAM</h1>
            <div className="flex items-center space-x-4">
                <span className="bg-green-100 text-green-800 text-xs font-bold px-3 py-1 rounded-full border border-green-200">
                    <i className="fa-solid fa-server mr-1"></i> API FastAPI Conectada
                </span>
                <span className="text-sm text-slate-500">
                    <i className="fa-regular fa-clock mr-1"></i> Octubre 2026
                </span>
            </div>
        </header>
    );
}