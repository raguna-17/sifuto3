import client from './client';

// 単体応募取得
export const getApplication = async (id) => {
    try {
        const res = await client.get(`/applications/${id}`);
        return res.data; // ApplicationRead の形で返る
    } catch (err) {
        if (err.response) {
            if (err.response.status === 404) {
                throw new Error('Application not found');
            }
            console.error(`Failed to fetch application (status ${err.response.status})`, err.response.data);
        } else {
            console.error('Failed to fetch application', err);
        }
        throw err;
    }
};

// 応募一覧取得
export const getMyApplications = async () => {
    try {
        const res = await client.get('/applications');
        return res.data;
    } catch (err) {
        if (err.response) {
            console.error(`Failed to fetch applications (status ${err.response.status})`, err.response.data);
        } else {
            console.error('Failed to fetch applications', err);
        }
        throw err;
    }
};

// 応募作成
export const createApplication = async (payload) => {
    try {
        const res = await client.post('/applications', payload);
        return res.data; // ApplicationRead の形で返る
    } catch (err) {
        if (err.response) {
            // バリデーションエラーやその他
            if (err.response.status === 422) {
                throw new Error('Invalid application payload');
            }
            console.error(`Failed to create application (status ${err.response.status})`, err.response.data);
        } else {
            console.error('Failed to create application', err);
        }
        throw err;
    }
};

// 応募削除
export const deleteApplication = async (id) => {
    try {
        await client.delete(`/applications/${id}`);
    } catch (err) {
        if (err.response) {
            if (err.response.status === 404) {
                throw new Error('Application not found');
            }
            console.error(`Failed to delete application (status ${err.response.status})`, err.response.data);
        } else {
            console.error('Failed to delete application', err);
        }
        throw err;
    }
};


// 応募ステータス更新
export const updateApplicationStatus = async (id, status) => {
    try {
        const res = await client.patch(`/applications/${id}`, { status });
        return res.data; // 更新後のApplication
    } catch (err) {
        if (err.response) {
            console.error(`Failed to update status (status ${err.response.status})`, err.response.data);
        } else {
            console.error('Failed to update status', err);
        }
        throw err;
    }
};