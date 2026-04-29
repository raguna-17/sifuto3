import axios from "axios";

const API = import.meta.env.VITE_API_URL;

const authHeader = () => ({
    headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
});

export const getOrganizations = async () => {
    const res = await axios.get(`${API}/organizations/`, authHeader());
    return res.data;
};

export const createOrganization = async (data) => {
    const res = await axios.post(`${API}/organizations/`, data, authHeader());
    return res.data;
};

export const updateOrganization = async (id, data) => {
    const res = await axios.patch(`${API}/organizations/${id}`, data, authHeader());
    return res.data;
};

export const deleteOrganization = async (id) => {
    await axios.delete(`${API}/organizations/${id}`, authHeader());
};