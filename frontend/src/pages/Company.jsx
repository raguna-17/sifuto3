import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createApplication } from '../api/applications';

export default function Company() {
    const [companyName, setCompanyName] = useState('');
    const [industry, setIndustry] = useState('');
    const [position, setPosition] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async () => {
        if (!companyName || !position) {
            alert('会社名とポジションは必須です');
            return;
        }

        const payload = {
            company_name: companyName,  // string
            industry: industry || "",   // 空文字でも送る
            position: position          // string
        };

        try {
            const data = await createApplication(payload);
            console.log('応募データ:', data);  // ← ここで company が入っているか確認
            alert('応募が完了しました');
            navigate('/application', { state: data });
        } catch (err) {
            console.error(err);
            alert('応募に失敗しました');
        }
    };

    return (
        <div>
            <h1>応募フォーム</h1>

            <div style={{ marginBottom: '10px' }}>
                <label>会社名:</label><br />
                <input
                    type="text"
                    value={companyName}
                    onChange={e => setCompanyName(e.target.value)}
                    placeholder="株式会社Example"
                />
            </div>

            <div style={{ marginBottom: '10px' }}>
                <label>業界:</label><br />
                <input
                    type="text"
                    value={industry}
                    onChange={e => setIndustry(e.target.value)}
                    placeholder="IT"
                />
            </div>

            <div style={{ marginBottom: '10px' }}>
                <label>ポジション:</label><br />
                <input
                    type="text"
                    value={position}
                    onChange={e => setPosition(e.target.value)}
                    placeholder="エンジニア"
                />
            </div>

            <div>
                <button onClick={handleSubmit}>応募する</button>
                <button onClick={() => navigate('/home')} style={{ marginLeft: '10px' }}>
                    ホームに戻る
                </button>
            </div>
        </div>
    );
}