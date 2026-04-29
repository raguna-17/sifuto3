import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
    getJobPostings,
    createJobPosting,
} from "./api";
import { getOrganizations } from "../organizations/api";

export default function JobPostingPage() {
    const [jobs, setJobs] = useState([]);
    const [organizations, setOrganizations] = useState([]);

    const [form, setForm] = useState({
        title: "",
        organization_id: "",
        description: "",
        location: "",
        salary: "",
        employment_type: "",
    });

    const [error, setError] = useState(null);

    // =====================
    // 初期取得
    // =====================
    useEffect(() => {
        fetchJobs();
        fetchOrganizations();
    }, []);

    const fetchJobs = async () => {
        try {
            const data = await getJobPostings();
            setJobs(data);
        } catch (err) {
            setError("求人取得に失敗");
        }
    };

    const fetchOrganizations = async () => {
        try {
            const data = await getOrganizations();
            setOrganizations(data);
        } catch (err) {
            console.error(err);
        }
    };

    // =====================
    // 入力処理
    // =====================
    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    // =====================
    // 作成
    // =====================
    const handleCreate = async () => {
        try {
            if (!form.title || !form.organization_id) {
                alert("タイトルと企業は必須です");
                return;
            }

            const created = await createJobPosting({
                ...form,
                organization_id: Number(form.organization_id),
            });

            setJobs((prev) => [...prev, created]);

            // フォームリセット
            setForm({
                title: "",
                organization_id: "",
                description: "",
                location: "",
                salary: "",
                employment_type: "",
            });
        } catch (err) {
            alert(err.message);
        }
    };

    if (error) return <p>{error}</p>;

    return (
        <div style={{ padding: 20 }}>
            <h1>求人票作成</h1>

            {/* =====================
                作成フォーム（全部項目）
            ===================== */}
            <div style={{ marginBottom: 20 }}>
                <input
                    name="title"
                    placeholder="タイトル"
                    value={form.title}
                    onChange={handleChange}
                />

                <select
                    name="organization_id"
                    value={form.organization_id}
                    onChange={handleChange}
                >
                    <option value="">企業を選択</option>
                    {organizations.map((org) => (
                        <option key={org.id} value={org.id}>
                            {org.name}
                        </option>
                    ))}
                </select>

                <input
                    name="location"
                    placeholder="勤務地"
                    value={form.location}
                    onChange={handleChange}
                />

                <input
                    name="salary"
                    placeholder="給与"
                    value={form.salary}
                    onChange={handleChange}
                />

                <input
                    name="employment_type"
                    placeholder="雇用形態"
                    value={form.employment_type}
                    onChange={handleChange}
                />

                <textarea
                    name="description"
                    placeholder="仕事内容"
                    value={form.description}
                    onChange={handleChange}
                />

                <button onClick={handleCreate}>作成</button>
            </div>

            <hr />

            <h2 style={{ marginTop: 30 }}>求人一覧</h2>
            
            {/* =====================
                一覧（タイトル＋企業名だけ）
            ===================== */}
            <ul>
                {jobs.map((job) => {
                    const org = organizations.find(
                        (o) => o.id === job.organization_id
                    );

                    return (
                        <li key={job.id}>
                            <Link to={`/job-postings/${job.id}`}>
                                {job.title}（{org ? org.name : "不明"}）
                            </Link>
                        </li>
                    );
                })}
            </ul>
        </div>
    );
}