import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getJobPosting } from "./api";
import { getOrganizations } from "../organizations/api";
import { createJobApplication, getMyApplications } from "../job_applications/api";

export default function JobPostingDetail() {
    const { id } = useParams();

    const [job, setJob] = useState(null);
    const [org, setOrg] = useState(null);
    const [applications, setApplications] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchData();
    }, [id]);

    const fetchData = async () => {
        const jobData = await getJobPosting(id);
        setJob(jobData);

        const orgs = await getOrganizations();
        const found = orgs.find(
            (o) => o.id === jobData.organization_id
        );
        setOrg(found);

        const apps = await getMyApplications();

        // 🔥 防御
        setApplications(Array.isArray(apps) ? apps : []);
    };

    const myApplication = applications.find(
        (app) => app.job_posting_id === Number(id)
    );

    const handleApply = async () => {
        try {
            setLoading(true);

            await createJobApplication({
                job_posting_id: job.id,
            });

            alert("応募に成功しました");

            // 再取得（状態更新）
            const apps = await getMyApplications();
            setApplications(apps);

        } catch (error) {
            console.error(error);
            alert("応募に失敗しました");
        } finally {
            setLoading(false);
        }
    };

    if (!job) return <p>読み込み中...</p>;

    return (
        <div style={{ padding: 20 }}>
            <h1>{job.title}</h1>

            <p>企業：{org ? org.name : "不明"}</p>
            <p>勤務地：{job.location}</p>
            <p>給与：{job.salary}</p>
            <p>雇用形態：{job.employment_type}</p>

            <hr />

            <p>{job.description}</p>

            <hr />

            {/* 🧠 応募ステータス表示 */}
            {myApplication ? (
                <div style={{ marginBottom: 10 }}>
                    <p>
                        応募ステータス：
                        <strong>{myApplication.status}</strong>
                    </p>
                </div>
            ) : (
                <p>まだ応募していません</p>
            )}

            {/* 🧠 ボタン制御 */}
            <button
                onClick={handleApply}
                disabled={loading || myApplication}
                style={{
                    padding: "10px 16px",
                    cursor:
                        loading || myApplication
                            ? "not-allowed"
                            : "pointer",
                    opacity: myApplication ? 0.5 : 1,
                }}
            >
                {myApplication
                    ? "応募済み"
                    : loading
                        ? "応募中..."
                        : "応募する"}
            </button>
        </div>
    );
}