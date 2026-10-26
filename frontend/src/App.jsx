import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout'; // Importamos el Layout

import DashboardDirectora from './pages/directora/DashboardDirectora';
import PanelSubdireccion from './pages/subdireccion/PanelSubdireccion';
import PanelGestor from './pages/gestor/PanelGestor';
import PanelJefe from './pages/jefe_programa/PanelJefe';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />

        {/* Envolvemos todas las rutas protegidas dentro de Layout */}
        <Route element={<Layout />}>
          
            <Route element={<ProtectedRoute rolesPermitidos={[1]} />}>
                <Route path="/directora" element={<DashboardDirectora />} />
            </Route>

            <Route element={<ProtectedRoute rolesPermitidos={[2]} />}>
                <Route path="/jefe-programa" element={<PanelJefe />} />
            </Route>

            <Route element={<ProtectedRoute rolesPermitidos={[3]} />}>
                <Route path="/gestor" element={<PanelGestor />} />
            </Route>

            <Route element={<ProtectedRoute rolesPermitidos={[4]} />}>
                <Route path="/subdireccion" element={<PanelSubdireccion />} />
            </Route>
            
        </Route>
      </Routes>
    </BrowserRouter>
  );
}