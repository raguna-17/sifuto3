const BASE_URL = import.meta.env.VITE_API_URL;

// =====================
// 一覧取得
// =====================
export const getJobPostings = async () => {
    const res = await fetch(`${BASE_URL}/job_postings/`);

    if (!res.ok) {
        throw new Error("求人一覧の取得に失敗しました");
    }

    return res.json();
};

// =====================
// 詳細取得
// =====================
export const getJobPosting = async (id) => {
    const res = await fetch(`${BASE_URL}/job_postings/${id}`);

    if (!res.ok) {
        throw new Error("求人詳細の取得に失敗しました");
    }

    return res.json();
};

// =====================
// 作成（認証あり）
// =====================
export const createJobPosting = async (data) => {
    const token = localStorage.getItem("token");

    const res = await fetch(`${BASE_URL}/job_postings/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(data),
    });

    const json = await res.json();

    if (!res.ok) {
        throw new Error(json.detail || "求人作成に失敗しました");
    }

    return json;
};

// =====================
// 更新（認証あり）
// =====================
export const updateJobPosting = async (id, data) => {
    const token = localStorage.getItem("token");

    const res = await fetch(`${BASE_URL}/job_postings/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(data),
    });

    const json = await res.json();

    if (!res.ok) {
        throw new Error(json.detail || "求人更新に失敗しました");
    }

    return json;
};

// =====================
// 削除（論理削除）
// =====================
export const deleteJobPosting = async (id) => {
    const token = localStorage.getItem("token");

    const res = await fetch(`${BASE_URL}/job_postings/${id}`, {
        method: "DELETE",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    if (!res.ok) {
        throw new Error("求人削除に失敗しました");
    }

    return true;
};