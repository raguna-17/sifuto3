// components/layout/Header.jsx
import { useNavigate } from "react-router-dom";

export default function Header() {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <header style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "10px 0",   // ヘッダー内の上下余白
            borderBottom: "1px solid #ccc"  // ヘッダーと本文の視覚的区切り
        }}>
            <h1>home</h1>
            <button onClick={handleLogout} style={{ cursor: "pointer" }}>
                Logout
            </button>
        </header>
    );
}