import { useState } from "react";
import { register } from "../api/users";
import { Link } from "react-router-dom";

export default function Register() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            await register(email, password);
            alert("登録成功");
        } catch (err) {
            alert("登録失敗");
        }
    };

    return (
        <form onSubmit={handleRegister}>
            <h2>Register</h2>

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

            <button type="submit">Register</button>

            <p>
                <Link to="/login">ログインへ</Link>
            </p>
        </form>
    );
}