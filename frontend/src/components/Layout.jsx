import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

export default function Layout() {
    return (
        <div className="bg-slate-50 font-sans text-slate-800 h-screen overflow-hidden flex">
            <Sidebar />
            
            <div className="flex-grow flex flex-col h-full overflow-hidden">
                <Header />
                <main className="flex-grow p-8 overflow-y-auto">
                    {/* Aquí es donde React renderiza el Dashboard, PanelGestor, etc. */}
                    <Outlet />
                </main>
            </div>
        </div>
    );
}