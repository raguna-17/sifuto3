import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getMyApplications } from '../api/applications';

export default function Application() {
    const { state } = useLocation();
    const navigate = useNavigate();
    const [application, setApplication] = useState(state || null);

    useEffect(() => {
        if (!state) {
            // ページ直アクセス時に最新応募データを取得
            const fetchApplications = async () => {
                const data = await getMyApplications();
                if (data.length > 0) setApplication(data[data.length - 1]); // 最新の応募を表示
            };
            fetchApplications();
        }
    }, [state]);

    if (!application) {
        return (
            <div>
                <h1>応募情報が見つかりません</h1>
                <button onClick={() => navigate('/home')}>ホームに戻る</button>
            </div>
        );
    }

    const { position, status, created_at, company } = application;

    return (
        <div>
            <h1>応募完了</h1>
            <p>会社名: {company?.name || '情報なし'}</p>
            <p>業界: {company?.industry || '情報なし'}</p>
            <p>ポジション: {position}</p>
            <p>応募日: {created_at}</p>
            <p>ステータス: {status}</p>
            <button onClick={() => navigate('/home')}>ホームに戻る</button>
        </div>
    );
}