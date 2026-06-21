import axios from "../../lib/axios";

// シフト生成
export const generateShiftFlow = () =>
    axios.post("/scheduler/generate");

export const saveShiftAssignments = (userId, slotIds) =>
    axios.post(`/shift-assignments/bulk/${userId}`,
        slotIds.map((slotId) => ({
            slot_id: slotId,
        }))
    );

// 一覧
export const getShiftAssignments = () =>
    axios.get("/shift-assignments");

// 自分の確定シフト
export const getMyShiftAssignments = () =>
    axios.get("/shift-assignments/me");