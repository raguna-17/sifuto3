import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL;

// 応募作成
export const createJobApplication = async (data) => {
    const token = localStorage.getItem("token");

    const res = await axios.post(
        `${BASE_URL}/job_applications/`,
        data,
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return res.data;
};

// 自分の応募一覧
export const getMyApplications = async () => {
    const token = localStorage.getItem("token");

    const res = await axios.get(
        `${BASE_URL}/job_applications/me`,
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return res.data;
};


export const updateApplicationStatus = async (id, data) => {
    const token = localStorage.getItem("token");

    const res = await axios.put(
        `${BASE_URL}/job_applications/${id}`,
        data,
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return res.data;
};