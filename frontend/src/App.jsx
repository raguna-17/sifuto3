import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Application from "./pages/Application";
import Company from "./pages/Company";
import Layout from "./components/layout/Layout";

// ログインチェック
const isAuthenticated = () => !!localStorage.getItem("access_token");

// 保護ルート
const ProtectedRoute = ({ children }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" />;
  }
  return children;
};

// 公開ページ用ルート（ログイン済みならホームにリダイレクト）
const PublicRoute = ({ children }) => {
  if (isAuthenticated()) {
    return <Navigate to="/home" />;
  }
  return children;
};

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ルートアクセス時 */}
        <Route path="/" element={<Navigate to="/home" />} />

        {/* 公開ページ */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute>
              <Register />
            </PublicRoute>
          }
        />

        {/* 保護ページ */}
        <Route
          path="/home"
          element={
            <ProtectedRoute>
              <Layout>
                <Home />
              </Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/company"
          element={
            <ProtectedRoute>
              <Layout>
                <Company />
              </Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/application"
          element={
            <ProtectedRoute>
              <Layout>
                <Application />
              </Layout>
            </ProtectedRoute>
          }
        />

        {/* 不正URL対策 */}
        <Route
          path="*"
          element={
            isAuthenticated() ? <Navigate to="/home" /> : <Navigate to="/login" />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}