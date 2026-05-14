import api from "../../api/axios";


// -------------------------
// login
// -------------------------

export const login = async (
    email,
    password
) => {
    const response = await api.post(
        "/users/login",
        {
            email,
            password,
        }
    );

    return response.data;
};


// -------------------------
// register
// -------------------------

export const register = async (
    email,
    password
) => {
    const response = await api.post(
        "/users/register",
        {
            email,
            password,
        }
    );

    return response.data;
};


// -------------------------
// current user
// -------------------------

export const getMe = async () => {
    const response = await api.get(
        "/users/me"
    );

    return response.data;
};