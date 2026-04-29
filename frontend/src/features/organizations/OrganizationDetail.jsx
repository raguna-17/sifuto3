import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import axios from "axios";

const API = import.meta.env.VITE_API_URL;

const OrganizationDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    const [org, setOrg] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);

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
            const res = await axios.get(`${API}/organizations/${id}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            });

            setOrg(res.data);
            setForm(res.data);
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
    // 入力変更
    // =====================
    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    // =====================
    // 更新
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

    // =====================
    // 削除（確認なし）
    // =====================
    const handleDelete = async () => {
        if (isDeleting) return;

        setIsDeleting(true);

        try {
            await axios.delete(`${API}/organizations/${id}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            });

            navigate("/organizations");
        } catch (err) {
            console.error("DELETE ERROR:", err.response?.data || err);
            setIsDeleting(false);
        }
    };

    if (loading) return <p>読み込み中...</p>;
    if (!org) return <p>データなし</p>;

    return (
        <div>
            <h1>会社詳細</h1>

            {!isEditing ? (
                <div>
                    <h2>{org.name}</h2>
                    <p>業界: {org.industry}</p>
                    <p>本社: {org.headquarters}</p>
                    <p>設立年: {org.founded_year}</p>

                    <button onClick={() => setIsEditing(true)}>
                        編集
                    </button>

                    <button
                        onClick={handleDelete}
                        disabled={isDeleting}
                        style={{
                            marginLeft: "10px",
                            backgroundColor: "red",
                            color: "white",
                        }}
                    >
                        {isDeleting ? "削除中..." : "削除"}
                    </button>
                </div>
            ) : (
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

            <br />

            <Link to="/organizations">
                ← 一覧へ戻る
            </Link>
        </div>
    );
};

export default OrganizationDetail;