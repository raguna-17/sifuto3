import { useState } from "react";
import { login } from "../api/users";
import { useNavigate, Link } from "react-router-dom";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const data = await login(email, password);
            localStorage.setItem("access_token", data.access_token);
            alert("ログイン成功");
            navigate("/home");
        } catch (err) {
            alert("ログイン失敗");
        }
    };

    return (
        <form onSubmit={handleLogin}>
            <h2>Login</h2>

            <input
                type="email"
                placeholder="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />

            <input
                type="password"
                placeholder="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            <button type="submit">Login</button>

            <p>
                ユーザー登録してない人は{" "}
                <Link to="/register">こちら</Link>
            </p>
        </form>
    );
}