import { useEffect, useState } from "react";
import { getMe, registerUser } from "./api";

const UsersPage = () => {
    const [me, setMe] = useState(null);

    const [form, setForm] = useState({
        email: "",
        password: "",
    });

    useEffect(() => {
        getMe().then((res) => {
            setMe(res.data);
        });
    }, []);

    const handleCreate = async () => {
        await registerUser(form);
        alert("ユーザー作成完了");
    };

    return (
        <div>
            <h2>ユーザー情報</h2>

            {me && (
                <div>
                    <p>ID: {me.id}</p>
                    <p>Email: {me.email}</p>
                    <p>Role: {me.role}</p>
                </div>
            )}

            <hr />

            <h3>ユーザー作成（管理者用）</h3>

            <input
                placeholder="email"
                onChange={(e) =>
                    setForm({ ...form, email: e.target.value })
                }
            />

            <input
                placeholder="password"
                type="password"
                onChange={(e) =>
                    setForm({ ...form, password: e.target.value })
                }
            />

            <button onClick={handleCreate}>
                作成
            </button>
        </div>
    );
};

export default UsersPage;