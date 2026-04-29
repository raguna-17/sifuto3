import { useEffect, useState } from "react";
import { getMyApplications, updateApplicationStatus } from "./api";

export default function JobApplicationPage() {
    const [applications, setApplications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [updatingId, setUpdatingId] = useState(null);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const data = await getMyApplications();
            setApplications(Array.isArray(data) ? data : []);
        } catch (error) {
            console.error(error);
            alert("応募一覧の取得に失敗しました");
        } finally {
            setLoading(false);
        }
    };

    const handleStatusChange = async (id, status) => {
        try {
            setUpdatingId(id);

            await updateApplicationStatus(id, { status });

            const data = await getMyApplications();
            setApplications(Array.isArray(data) ? data : []);
        } catch (error) {
            console.error(error);
            alert("ステータス更新に失敗しました");
        } finally {
            setUpdatingId(null);
        }
    };

    if (loading) return <p>読み込み中...</p>;

    return (
        <div style={{ padding: 20 }}>
            <h1>応募一覧</h1>

            {applications.length === 0 ? (
                <p>まだ応募はありません</p>
            ) : (
                applications.map((app) => (
                    <div
                        key={app.id}
                        style={{
                            border: "1px solid #ddd",
                            padding: 12,
                            marginBottom: 10,
                            borderRadius: 6,
                            background: "#fafafa",
                        }}
                    >
                        <p>応募ID: {app.id}</p>
                        <p>求人ID: {app.job_posting_id}</p>

                        {/* ステータス変更 */}
                        <p>
                            ステータス:{" "}
                            <select
                                value={app.status}
                                onChange={(e) =>
                                    handleStatusChange(app.id, e.target.value)
                                }
                               
                            >
                                <option value="applied">応募中</option>
                                <option value="interview">面接中</option>   {/* 追加 */}
                                <option value="offer">内定</option>        {/* 修正 */}
                                <option value="rejected">不採用</option>
                            </select>
                        </p>

                        <p>
                            応募日時:{" "}
                            {new Date(app.created_at).toLocaleString()}
                        </p>

                        {updatingId === app.id && (
                            <p style={{ color: "gray" }}>
                                更新中...
                            </p>
                        )}
                    </div>
                ))
            )}
        </div>
    );
}