import { useEffect, useState } from "react";
import Button from "../components/Button";
import Modal from "../components/Modal";
import Spinner from "../components/Spinner";

const API_URL = import.meta.env.VITE_API_URL;

const JobApplicationPage = () => {
    const [applications, setApplications] = useState([]);
    const [loading, setLoading] = useState(false);

    const [deleteTarget, setDeleteTarget] = useState(null); // 削除対象
    const token = localStorage.getItem("token");

    const fetchApplications = async () => {
        setLoading(true);

        try {
            const res = await fetch(`${API_URL}/job-applications`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            const data = await res.json();

            if (!res.ok || !Array.isArray(data)) {
                setApplications([]);
                return;
            }

            const sorted = [...data].sort(
                (a, b) => new Date(b.created_at) - new Date(a.created_at)
            );

            setApplications(sorted);
        } catch (err) {
            console.error(err);
            setApplications([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchApplications();
    }, []);

    const handleDelete = async (id) => {
        try {
            await fetch(`${API_URL}/job-applications/${id}`, {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            setDeleteTarget(null);
            fetchApplications();
        } catch (err) {
            console.error(err);
        }
    };

    if (loading) return <Spinner />;

    return (
        <div>
            <h1>応募履歴</h1>

            {applications.length === 0 ? (
                <p>応募なし</p>
            ) : (
                applications.map((app) => (
                    <div
                        key={app.id}
                        style={{
                            border: "1px solid #ddd",
                            padding: "10px",
                            marginBottom: "10px",
                        }}
                    >
                        <h3>{app.organization_name}</h3>

                        <p>職種: {app.job_title}</p>

                        <p>
                            応募日時:{" "}
                            {app.created_at
                                ? new Date(app.created_at).toLocaleString()
                                : "不明"}
                        </p>

                        <Button
                            onClick={() => setDeleteTarget(app)}
                            variant="danger"
                        >
                            削除
                        </Button>
                    </div>
                ))
            )}

            {/* 削除確認モーダル */}
            {deleteTarget && (
                <Modal onClose={() => setDeleteTarget(null)}>
                    <h3>削除しますか？</h3>

                    <p>{deleteTarget.organization_name}</p>

                    <div style={{ display: "flex", gap: "10px" }}>
                        <Button
                            variant="danger"
                            onClick={() => handleDelete(deleteTarget.id)}
                        >
                            削除する
                        </Button>

                        <Button
                            variant="secondary"
                            onClick={() => setDeleteTarget(null)}
                        >
                            キャンセル
                        </Button>
                    </div>
                </Modal>
            )}
        </div>
    );
};

export default JobApplicationPage;