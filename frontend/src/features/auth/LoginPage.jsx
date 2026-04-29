import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login } from "./api";

const LoginPage = () => {//ログインページそのもの
    const navigate = useNavigate();//ページ遷移用の関数

    const [email, setEmail] = useState("");//入力されたメール
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");//エラーメッセージ

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

        return "";//OKなら「空文字」
    };

    const handleSubmit = async (e) => {//ログイン処理の本体
        e.preventDefault();//form送信時のページリロードを防ぎ、React側で制御するため

        const errMsg = validate();
        if (errMsg) {
            setError(errMsg);
            return;//エラーがあれば止める
        }

        try {
            const data = await login(email, password);//login APIに対してHTTPリクエスト（通常はPOST）を送り、認証結果としてアクセストークンを受け
            localStorage.setItem("token", data.access_token);//次のAPIでAuthorizationヘッダーに使う
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
            <p>
                法人の方は{" "}
                <Link to="/organizations">こちら</Link>
            </p>
        </div>
    );
};

export default LoginPage;