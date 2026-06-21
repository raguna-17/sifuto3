import { Link } from "react-router-dom";

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

const Sidebar = () => {
    const role = getRoleFromToken();

    if (!role) return null;

    const adminMenu = [
        { name: "シフトスロット一覧", path: "/shift-slots" },
        { name: "シフトスロット作成", path: "/shift-slots/create" },
        { name: "シフト生成・編集", path: "/shift-flow/create" },
        { name: "確定シフト確認", path: "/shift-flow/view" },
        { name: "ユーザー管理", path: "/users" },
    ];

    const userMenu = [
        { name: "シフトスロット一覧", path: "/shift-slots" },
        { name: "確定シフト確認", path: "/shift-flow/view" },
    ];

    const menu = role === "admin" ? adminMenu : userMenu;

    return (
        <aside className="sidebar">
            <h2 className="sidebar-title">シフト管理</h2>

            <nav className="sidebar-nav">
                {menu.map((item) => (
                    <Link
                        key={item.path}
                        to={item.path}
                        className="sidebar-link"
                    >
                        {item.name}
                    </Link>
                ))}
            </nav>
        </aside>
    );
};

export default Sidebar;