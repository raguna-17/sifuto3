import client from './client';

// 会社一覧取得
export const getCompanies = async () => {
    const res = await client.get('/companies');
    return res.data; // CompanyRead の配列
};

// 会社作成（管理者用）
export const createCompany = async (payload) => {
    const res = await client.post('/companies', payload);
    return res.data;
};