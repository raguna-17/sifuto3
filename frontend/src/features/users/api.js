import axios from "../../lib/axios";

// 自分の情報
export const getMe = () => axios.get("/users/me");

export const getUsers = () =>
    axios.get("/users");

// ユーザー作成（register流用）
export const registerUser = (data) =>
    axios.post("/users/register", data);

// login（必要ならここでも使う）
export const login = (data) =>
    axios.post("/users/login", data);