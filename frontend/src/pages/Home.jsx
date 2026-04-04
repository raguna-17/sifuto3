import { useEffect, useState } from "react";
import { getMe } from "../api/users";
import { Link } from "react-router-dom";

export default function Home() {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const data = await getMe();
                setUser(data);
            } catch (err) {
                console.error(err);
            }
        };
        fetchUser();
    }, []);

    if (!user) return <p>Loading...</p>;

    return (
        <div style={{ display: 'flex', flexDirection: 'column', height: '80vh', gap: '20px' }}>
            {/* 上: Company ボタン */}
            <div style={{ flex: 0.6, display: 'flex', alignItems: 'flex-end' }}>
                <Link to="/company" style={{ width: '100%' }}>
                    <button style={{ width: '30%', height: '30%', fontSize: '2rem', cursor: 'pointer' }}>
                        Companyへ
                    </button>
                </Link>
            </div>

            {/* 下: Application ボタン */}
            <div style={{ flex: 1, display: 'flex', alignItems: 'center' }}>
                <Link to="/application" style={{ width: '100%' }}>
                    <button style={{ width: '40%', height: '30%', fontSize: '2rem', cursor: 'pointer' }}>
                        Applicationへ
                    </button>
                </Link>
            </div>
        </div>
    );
}