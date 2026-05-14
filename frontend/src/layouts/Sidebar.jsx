import { Link } from "react-router-dom";

const Sidebar = () => {
    const menu = [
        { name: "商品一覧", path: "/products" },
        { name: "商品作成", path: "/products/create" },
        { name: "カート", path: "/cart" },
        { name: "注文履歴", path: "/orders" },
    ];

    return (
        <aside className="sidebar">
            <h2 className="sidebar-title">ECサイト</h2>

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