import api from "../../lib/axios";

// login
export const login = async (email, password) => {
    const response = await api.post("/users/login", {
        email,
        password,
    });

    return response.data;
};

// register（name追加）
export const register = async (name, email, password) => {
    const response = await api.post("/users/register", {
        name,
        email,
        password,
    });

    return response.data;
};

// me
export const getMe = async () => {
    const response = await api.get("/users/me");
    return response.data;
};