import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

const API = import.meta.env.VITE_API_URL;

const OrganizationDetail = () => {
    const { id } = useParams();

    const [org, setOrg] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);

    // 編集用フォーム
    const [form, setForm] = useState({
        name: "",
        industry: "",
        headquarters: "",
        founded_year: "",
    });

    // =====================
    // データ取得
    // =====================
    const fetchOrg = async () => {
        try {
            const res = await axios.get(
                `${API}/organizations/${id}`,
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,
                    },
                }
            );

            setOrg(res.data);
            setForm(res.data); // 編集用にセット
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchOrg();
    }, [id]);

    // =====================
    // input変更
    // =====================
    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    // =====================
    // 更新処理（PATCH）
    // =====================
    const handleUpdate = async () => {
        try {
            const payload = {
                name: form.name || null,
                industry: form.industry || null,
                headquarters: form.headquarters || null,
                founded_year:
                    form.founded_year !== ""
                        ? Number(form.founded_year)
                        : null,
            };

            console.log("PATCH PAYLOAD:", payload);

            const res = await axios.patch(
                `${API}/organizations/${id}`,
                payload,
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,
                    },
                }
            );

            setOrg(res.data);
            setIsEditing(false);
        } catch (err) {
            console.error("PATCH ERROR:", err.response?.data || err);
        }
    };

    if (loading) return <p>読み込み中...</p>;
    if (!org) return <p>データなし</p>;

    return (
        <div>
            <h1>会社詳細</h1>

            {/* =====================
                表示モード
            ===================== */}
            {!isEditing ? (
                <div>
                    <h2>{org.name}</h2>
                    <p>業界: {org.industry}</p>
                    <p>本社: {org.headquarters}</p>
                    <p>設立年: {org.founded_year}</p>

                    <button onClick={() => setIsEditing(true)}>
                        編集
                    </button>
                </div>
            ) : (
                /* =====================
                    編集モード
                ===================== */
                <div>
                    <h2>編集</h2>

                    <input
                        name="name"
                        value={form.name || ""}
                        onChange={handleChange}
                    />

                    <input
                        name="industry"
                        value={form.industry || ""}
                        onChange={handleChange}
                    />

                    <input
                        name="headquarters"
                        value={form.headquarters || ""}
                        onChange={handleChange}
                    />

                    <input
                        name="founded_year"
                        value={form.founded_year || ""}
                        onChange={handleChange}
                    />

                    <button onClick={handleUpdate}>保存</button>
                    <button onClick={() => setIsEditing(false)}>
                        キャンセル
                    </button>
                </div>
            )}

            {/* =====================
                戻る
            ===================== */}
            <br />
            <Link to="/organizations">
                ← 一覧へ戻る
            </Link>
        </div>
    );
};

export default OrganizationDetail;