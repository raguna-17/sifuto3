import axios from "../../lib/axios";

// シフト生成
export const generateShiftFlow = () =>
    axios.post("/scheduler/generate");

// シフト確定
export const confirmShiftFlow = (assignments) =>
    axios.post("/scheduler/confirm", {
        assignments,
    });

// 一覧
export const getShiftAssignments = () =>
    axios.get("/shift-assignments");

// 自分の確定シフト
export const getMyShiftAssignments = () =>
    axios.get("/shift-assignments/me");