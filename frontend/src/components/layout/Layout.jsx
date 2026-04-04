// components/layout/Layout.jsx
import Header from "./Header";

export default function Layout({ children }) {
    return (
        <div style={{
            display: "flex",
            flexDirection: "column",
            minHeight: "100vh",
            padding: "20px",    // ページ全体の余白
            gap: "20px"          // ヘッダーと本文の間の隙間
        }}>
            <Header />
            <main style={{ flex: 1 }}>
                {children}
            </main>
        </div>
    );
}