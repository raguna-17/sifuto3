import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Layout from "./layouts/Layout";

import LoginPage from "./features/auth/LoginPage";
import RegisterPage from "./features/auth/RegisterPage";

import ShiftSlotListPage from "./features/shiftSlots/ShiftSlotListPage";
import ShiftSlotDetailPage from "./features/shiftSlots/ShiftSlotDetailPage";
import ShiftSlotCreatePage from "./features/shiftSlots/ShiftSlotCreatePage";

import ShiftFlowCreatePage from "./features/shiftFlow/ShiftFlowCreatePage";
import ShiftFlowViewPage from "./features/shiftFlow/ShiftFlowViewPage";

import UsersPage from "./features/users/UsersPage";

// -------------------------
// 共通JWT解析
// -------------------------
const getRoleFromToken = () => {
  const token = localStorage.getItem("token");

  if (!token) return null;

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.role || null;
  } catch {
    return null;
  }
};

const isAuthenticated = () => {
  return !!localStorage.getItem("token");
};

// -------------------------
// Guards
// -------------------------
const PrivateRoute = ({ children }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

// 複数ロール対応に拡張
const RoleRoute = ({ roles = [], children }) => {
  const userRole = getRoleFromToken();

  if (!userRole) {
    return <Navigate to="/login" replace />;
  }

  if (!roles.includes(userRole)) {
    return <Navigate to="/" replace />;
  }

  return children;
};

// -------------------------
// App
// -------------------------
function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* public */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* private layout */}
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Layout />
            </PrivateRoute>
          }
        >

          <Route index element={<ShiftSlotListPage />} />

          {/* shift slots */}
          <Route path="shift-slots" element={<ShiftSlotListPage />} />

          <Route
            path="shift-slots/:id"
            element={<ShiftSlotDetailPage />}
          />

          <Route
            path="shift-slots/create"
            element={
              <RoleRoute roles={["admin"]}>
                <ShiftSlotCreatePage />
              </RoleRoute>
            }
          />

          {/* shift flow */}
          <Route
            path="shift-flow/create"
            element={
              <RoleRoute roles={["admin"]}>
                <ShiftFlowCreatePage />
              </RoleRoute>
            }
          />

          <Route
            path="shift-flow/view"
            element={<ShiftFlowViewPage />}
          />

          {/* users */}
          <Route
            path="users"
            element={
              <RoleRoute roles={["admin"]}>
                <UsersPage />
              </RoleRoute>
            }
          />

        </Route>

        {/* fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;