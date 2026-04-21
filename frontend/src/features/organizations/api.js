const API_URL = import.meta.env.VITE_API_URL;

export const fetchOrganizations = async (token) => {
    const res = await fetch(`${API_URL}/organizations`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.detail || "Failed to fetch organizations");
    }

    return data;
};