import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./layouts/Layout";

import LoginPage from "./features/auth/LoginPage";
import RegisterPage from "./features/auth/RegisterPage";

import Home from "./pages/Home";
import JobApplicationPage from "./features/job_applications/JobApplicationPage";
import JobPostingPage from "./features/job_postings/JobPostingPage";
import JobPostingDetail from "./features/job_postings/JobPostingDetail";
import OrganizationPage from "./features/organizations/OrganizationPage";
import OrganizationDetail from "./features/organizations/OrganizationDetail";

// 仮の認証チェック
const isAuthenticated = () => {
  return !!localStorage.getItem("token");//!!"abc" → true,!!null → false
};

// 認証ガード
const PrivateRoute = ({ children }) => {
  return isAuthenticated() ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ログイン系（LayoutなしでもOK） */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="organizations" element={<OrganizationPage />} />
        <Route path="/organizations/:id" element={<OrganizationDetail />} />

        {/* 認証後ページ */}
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Layout />
            </PrivateRoute>
          }
        >
          {/* ホーム */}
          <Route index element={<Home />} />

          {/* 各ページ */}
          <Route path="job-applications" element={<JobApplicationPage />} />
          <Route path="job-postings" element={<JobPostingPage />} />   
          <Route path="job-postings/:id" element={<JobPostingDetail />} />      
        </Route>

        {/* それ以外はログインへ */}
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;