import client from './client';

// 応募作成
export const createApplication = async (payload) => {
    const res = await client.post('/applications', payload);
    return res.data; // ApplicationRead の形で返る
};

// 応募一覧取得（必要なら）
export const getMyApplications = async () => {
    const res = await client.get('/applications');
    return res.data;
};