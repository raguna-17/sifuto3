import { useState } from "react";

import {
    useNavigate,
    Link,
} from "react-router-dom";

import {
    login,
    getMe,
} from "./api";

import Input from "../../components/Input";
import Button from "../../components/Button";
import Spinner from "../../components/Spinner";

const TOKEN_KEY = "token";
const REFRESH_KEY = "refresh";
const USER_KEY = "user";

const LoginPage = () => {
    const navigate = useNavigate();

    const [email, setEmail] =
        useState("");

    const [password, setPassword] =
        useState("");

    const [error, setError] =
        useState("");

    const [loading, setLoading] =
        useState(false);

    // -------------------------
    // validate
    // -------------------------

    const validate = () => {
        if (!email || !password) {
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

    // -------------------------
    // submit
    // -------------------------

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

            // login
            const data = await login(
                email,
                password
            );

            // token save
            localStorage.setItem(
                TOKEN_KEY,
                data.access_token
            );

            localStorage.setItem(
                REFRESH_KEY,
                data.refresh_token
            );

            // current user
            const me = await getMe();

            localStorage.setItem(
                USER_KEY,
                JSON.stringify(me)
            );

            console.log(
                "ログインユーザー:",
                me
            );

            // home
            navigate("/");

        } catch (err) {
            setError(
                err.response?.data?.detail ||
                err.message ||
                "ログイン失敗"
            );

        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>ログイン</h1>

            {error && (
                <p>{error}</p>
            )}

            <form onSubmit={handleSubmit}>
                <div>
                    <Input
                        type="email"
                        placeholder="メールアドレス"
                        value={email}
                        onChange={(e) =>
                            setEmail(
                                e.target.value
                            )
                        }
                    />
                </div>

                <div>
                    <Input
                        type="password"
                        placeholder="パスワード"
                        value={password}
                        onChange={(e) =>
                            setPassword(
                                e.target.value
                            )
                        }
                    />
                </div>

                <Button
                    type="submit"
                    disabled={loading}
                >
                    {loading
                        ? <Spinner />
                        : "ログイン"}
                </Button>
            </form>

            <p>
                アカウントがない？
                {" "}
                <Link to="/register">
                    新規登録はこちら
                </Link>
            </p>
        </div>
    );
};

export default LoginPage;