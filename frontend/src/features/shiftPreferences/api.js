import axios from "../../lib/axios";

// 作成
export const createShiftPreference = (data) =>
    axios.post("/shift-preferences", data);

// 自分の申請（特定slot）
export const getMyPreferenceBySlot = (shift_slot_id) =>
    axios.get("/shift-preferences/me", {
        params: { shift_slot_id },
    });

// 全取得（admin用）
export const getAllPreferences = () =>
    axios.get("/shift-preferences");

// 詳細（admin用）
export const getPreference = (id) =>
    axios.get(`/shift-preferences/${id}`);

// 更新
export const updatePreference = (id, data) =>
    axios.patch(`/shift-preferences/${id}`, data);

// 削除
export const deletePreference = (id) =>
    axios.delete(`/shift-preferences/${id}`);