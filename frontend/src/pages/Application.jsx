import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import {
    getMyApplications,
    deleteApplication,
    updateApplicationStatus
} from '../api/applications';

export default function Application() {
    const { state } = useLocation();
    const navigate = useNavigate();
    const [applications, setApplications] = useState([]);

    // 日付フォーマット（人間用）
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleString('ja-JP', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    // 初期データ取得
    useEffect(() => {
        const fetchApplications = async () => {
            try {
                const data = await getMyApplications();
                if (data) {
                    const sorted = data.sort(
                        (a, b) => new Date(b.created_at) - new Date(a.created_at)
                    );
                    setApplications(sorted);
                }
            } catch (err) {
                console.error(err);
            }
        };
        fetchApplications();
    }, []);

    // Company.jsxから来た最新応募を追加
    useEffect(() => {
        if (state) {
            setApplications(prev => {
                const exists = prev.some(app => app.id === state.id);
                if (exists) return prev;

                const newList = [state, ...prev];
                return newList.sort(
                    (a, b) => new Date(b.created_at) - new Date(a.created_at)
                );
            });
        }
    }, [state]);

    // 削除
    const handleDelete = async (id) => {
        try {
            await deleteApplication(id);
            setApplications(prev => prev.filter(app => app.id !== id));
        } catch (err) {
            console.error(err);
            alert('削除に失敗しました');
        }
    };

    // ステータス更新
    const handleStatusChange = async (id, newStatus) => {
        try {
            const updated = await updateApplicationStatus(id, newStatus);

            setApplications(prev =>
                prev.map(app =>
                    app.id === id ? { ...app, status: updated.status } : app
                )
            );
        } catch (err) {
            console.error(err);
            alert('ステータス更新に失敗しました');
        }
    };

    if (applications.length === 0) {
        return (
            <div>
                <h1>応募情報が見つかりません</h1>
                <button onClick={() => navigate('/home')}>
                    ホームに戻る
                </button>
            </div>
        );
    }

    return (
        <div>
            <h1>応募履歴</h1>

            {applications.map((app) => {
                const { id, position, status, created_at, company } = app;

                return (
                    <div
                        key={id}
                        style={{
                            border: '1px solid #ccc',
                            marginBottom: '10px',
                            padding: '10px'
                        }}
                    >
                        <p>会社名: {company?.name || '情報なし'}</p>
                        <p>業界: {company?.industry || '情報なし'}</p>
                        <p>ポジション: {position}</p>

                        {/* ここ修正 */}
                        <p>応募日: {formatDate(created_at)}</p>

                        <p>
                            ステータス:
                            <select
                                value={status}
                                onChange={(e) =>
                                    handleStatusChange(id, e.target.value)
                                }
                                style={{ marginLeft: '10px' }}
                            >
                                <option value="applied">応募済み</option>
                                <option value="interview">面接中</option>
                                <option value="rejected">不採用</option>
                                <option value="accepted">内定</option>
                            </select>
                        </p>

                        <button onClick={() => handleDelete(id)}>
                            削除
                        </button>
                    </div>
                );
            })}

            <button onClick={() => navigate('/home')}>
                ホームに戻る
            </button>
        </div>
    );
}