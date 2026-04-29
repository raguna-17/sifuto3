import { useState } from "react";
import { Link } from "react-router-dom";
import { useOrganizations } from "./useOrganizations";

const OrganizationPage = () => {
    const { orgs, loading, error, createOrg } = useOrganizations();

    const [form, setForm] = useState({
        name: "",
        industry: "",
        headquarters: "",
        founded_year: "",
    });

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        await createOrg({
            ...form,
            founded_year: form.founded_year
                ? Number(form.founded_year)
                : null,
        });

        setForm({
            name: "",
            industry: "",
            headquarters: "",
            founded_year: "",
        });
    };

    if (loading) return <p>読み込み中...</p>;
    if (error) return <p style={{ color: "red" }}>{error}</p>;

    return (
        <div>

            <div style={{ marginBottom: 10 }}>
                <Link to="/login">
                    ← ログイン画面に戻る
                </Link>
            </div>

            <h1>会社情報の作成</h1>

            {/* =====================
                作成フォーム
            ===================== */}
            <form onSubmit={handleSubmit}>
                <input
                    name="name"
                    placeholder="会社名"
                    value={form.name}
                    onChange={handleChange}
                />

                <input
                    name="industry"
                    placeholder="業界"
                    value={form.industry}
                    onChange={handleChange}
                />

                <input
                    name="headquarters"
                    placeholder="本社"
                    value={form.headquarters}
                    onChange={handleChange}
                />

                <input
                    name="founded_year"
                    placeholder="設立年"
                    value={form.founded_year}
                    onChange={handleChange}
                />

                <button type="submit">作成</button>
            </form>

            {/* =====================
                一覧（リンク化）
            ===================== */}
            <h2>会社一覧</h2>

            <ul>
                {orgs.map((org) => (
                    <li key={org.id}>
                        {/* 👇ここがポイント */}
                        <Link to={`/organizations/${org.id}`}>
                            {org.name}
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default OrganizationPage;