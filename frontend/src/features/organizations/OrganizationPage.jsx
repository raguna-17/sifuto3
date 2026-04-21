import { useState } from "react";
import { createJobApplication } from "../job_applications/api";
import Button from "../../components/Button";
import Input from "../../components/Input";

const API_URL = import.meta.env.VITE_API_URL;

const OrganizationPage = () => {
    const [companyName, setCompanyName] = useState("");
    const [jobTitle, setJobTitle] = useState("");
    const [loading, setLoading] = useState(false);

    const token = localStorage.getItem("token");

    const handleApply = async () => {
        if (!companyName || !jobTitle) {
            alert("会社名と職種を入力してください");
            return;
        }

        setLoading(true);

        try {
            // ① organization作成
            const orgRes = await fetch(`${API_URL}/organizations`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    name: companyName,
                    industry: null,
                }),
            });

            const orgData = await orgRes.json();

            if (!orgRes.ok) {
                throw new Error(orgData.detail || "Organization作成失敗");
            }

            // ② job application作成
            const jobRes = await createJobApplication(
                {
                    organization_id: orgData.id,
                    job_title: jobTitle,
                },
                token
            );

            alert("応募成功しました");

            // reset
            setCompanyName("");
            setJobTitle("");

        } catch (err) {
            console.error(err);
            alert("応募に失敗しました");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: "350px" }}>
            <h1>応募フォーム</h1>

            <Input
                placeholder="会社名"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
            />

            <Input
                placeholder="職種"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
            />

            <Button onClick={handleApply} disabled={loading}>
                {loading ? "処理中..." : "応募する"}
            </Button>
        </div>
    );
};

export default OrganizationPage;