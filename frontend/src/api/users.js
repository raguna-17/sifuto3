import client from "./client";

export const register = async (email, password) => {
    const res = await client.post("/users/register", {
        email,
        password,
    });
    return res.data;
};

export const login = async (email, password) => {
    const res = await client.post("/users/login", {
        email,
        password,
    });
    return res.data;
};

export const getMe = async () => {
    const res = await client.get("/users/me");
    return res.data;
};