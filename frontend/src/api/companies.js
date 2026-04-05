import client from './client';

// 単体会社取得
export const getCompany = async (id) => {
    try {
        const res = await client.get(`/companies/${id}`);
        return res.data;
    } catch (err) {
        if (err.response) {
            // サーバーから返されたエラー
            console.error(`Failed to fetch company (status ${err.response.status})`, err.response.data);
        } else {
            // ネットワークエラーなど
            console.error('Failed to fetch company', err);
        }
        throw err;
    }
};

// 会社一覧取得
export const getCompanies = async () => {
    try {
        const res = await client.get('/companies');
        return res.data; // CompanyRead の配列
    } catch (err) {
        if (err.response) {
            console.error(`Failed to fetch companies (status ${err.response.status})`, err.response.data);
        } else {
            console.error('Failed to fetch companies', err);
        }
        throw err;
    }
};

// 会社作成（管理者用）
export const createCompany = async (payload) => {
    try {
        const res = await client.post('/companies', payload);
        return res.data;
    } catch (err) {
        if (err.response) {
            // 重複作成などの想定エラー
            if (err.response.status === 409) {
                throw new Error('Company already exists');
            }
            console.error(`Failed to create company (status ${err.response.status})`, err.response.data);
        } else {
            console.error('Failed to create company', err);
        }
        throw err;
    }
};