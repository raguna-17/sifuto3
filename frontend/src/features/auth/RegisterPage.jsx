import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register } from "./api";

const RegisterPage = () => {
    const navigate = useNavigate();

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const validate = () => {
        if (!name || !email || !password) {
            return "全て入力してください";
        }

        if (!email.includes("@")) {
            return "メール形式が正しくありません";
        }

        if (password.length < 4) {
            return "パスワードは4文字以上です";
        }

        return "";
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        setError("");

        const errMsg = validate();
        if (errMsg) {
            setError(errMsg);
            return;
        }

        try {
            setLoading(true);

            await register(name, email, password);

            navigate("/login");

        } catch (err) {
            const msg =
                err?.response?.data?.detail ||
                err.message ||
                "登録に失敗しました";

            setError(msg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: "400px", margin: "80px auto" }}>
            <h1>新規登録</h1>

            {error && (
                <p style={{ color: "red" }}>
                    {error}
                </p>
            )}

            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: "12px" }}>
                    <input
                        type="text"
                        placeholder="名前"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        style={{
                            width: "100%",
                            padding: "10px",
                        }}
                    />
                </div>

                <div style={{ marginBottom: "12px" }}>
                    <input
                        type="email"
                        placeholder="メールアドレス"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        style={{
                            width: "100%",
                            padding: "10px",
                        }}
                    />
                </div>

                <div style={{ marginBottom: "12px" }}>
                    <input
                        type="password"
                        placeholder="パスワード"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        style={{
                            width: "100%",
                            padding: "10px",
                        }}
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    style={{
                        width: "100%",
                        padding: "10px",
                    }}
                >
                    {loading ? "登録中..." : "登録"}
                </button>
            </form>

            <p style={{ marginTop: "16px" }}>
                すでにアカウントある？{" "}
                <Link to="/login">ログインはこちら</Link>
            </p>
        </div>
    );
};

export default RegisterPage;