import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login } from "./api";

const LoginPage = () => {
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const validate = () => {
        if (!email || !password) {
            return "全て入力してください";
        }

        if (!email.includes("@")) {
            return "正しいメール形式で入力してください";
        }

        if (password.length < 4) {
            return "パスワードは4文字以上";
        }

        return "";
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const errMsg = validate();
        if (errMsg) {
            setError(errMsg);
            return;
        }

        try {
            const data = await login(email, password);
            localStorage.setItem("token", data.access_token);
            navigate("/");
        } catch (err) {
            setError("メールまたはパスワードが違います");
        }
    };

    return (
        <div>
            <h1>ログイン</h1>

            {error && <p style={{ color: "red" }}>{error}</p>}

            <form onSubmit={handleSubmit}>
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

                <button type="submit">ログイン</button>
            </form>

            <p>
                アカウントがない？{" "}
                <Link to="/register">新規登録はこちら</Link>
            </p>
        </div>
    );
};

export default LoginPage;