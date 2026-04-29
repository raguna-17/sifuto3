import { Link, useLocation } from "react-router-dom";

const Sidebar = () => {
    const location = useLocation();

    const menu = [
        { name: "ホーム", path: "/" },
        { name: "応募履歴", path: "/job-applications" },
        { name: "求人応募", path: "/job-postings" },
    ];

    return (
        <div style={styles.sidebar}>
            <h2 style={styles.title}>求人アプリ</h2>

            <nav>
                {menu.map((item) => {
                    const isActive = location.pathname === item.path;

                    return (
                        <Link
                            key={item.path}
                            to={item.path}
                            style={{
                                ...styles.link,
                                ...(isActive ? styles.active : {}),
                            }}
                        >
                            {item.name}
                        </Link>
                    );
                })}
            </nav>
        </div>
    );
};

const styles = {
    sidebar: {
        width: "200px",
        height: "100vh",
        background: "#1e293b",
        color: "#fff",
        padding: "20px",
    },
    title: {
        marginBottom: "20px",
    },
    link: {
        display: "block",
        padding: "10px",
        color: "#cbd5f5",
        textDecoration: "none",
        borderRadius: "6px",
        marginBottom: "8px",
    },
    active: {
        background: "#3b82f6",
        color: "#fff",
    },
};

export default Sidebar;