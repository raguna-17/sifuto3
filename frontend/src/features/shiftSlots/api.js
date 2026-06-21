import axios from "../../lib/axios";

// 一覧
export const getShiftSlots = () =>
    axios.get("/shift-slots");

// 詳細
export const getShiftSlot = (id) =>
    axios.get(`/shift-slots/${id}`);

// 作成（admin）
export const createShiftSlot = (data) =>
    axios.post("/shift-slots", data);

// 更新（admin）
export const updateShiftSlot = (id, data) =>
    axios.patch(`/shift-slots/${id}`, data);

// 削除（admin）
export const deleteShiftSlot = (id) =>
    axios.delete(`/shift-slots/${id}`);