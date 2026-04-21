import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register } from "./api";

const RegisterPage = () => {
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
        setError(""); // リセット

        const errMsg = validate();
        if (errMsg) {
            setError(errMsg);
            return;
        }

        try {
            await register(email, password);

            alert("登録成功！ログインしてください");
            navigate("/login");

        } catch (err) {
            // 👇 ここがポイント
            if (err.message.includes("already") || err.message.includes("exists")) {
                setError("このメールアドレスは既に登録されています");
            } else {
                setError("登録に失敗しました");
            }
        }
    };

    return (
        <div>
            <h1>新規登録</h1>

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

                <button type="submit">登録</button>
            </form>

            <p>
                すでにアカウントある？{" "}
                <Link to="/login">ログインはこちら</Link>
            </p>
        </div>
    );
};

export default RegisterPage;