import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "../../lib/axios";
import { getShiftSlot } from "./api";

import PreferenceForm from "../shiftPreferences/PreferenceForm";


const getRoleFromToken = () => {
    const token = localStorage.getItem("token");

    if (!token) return null;

    try {
        const payload = JSON.parse(atob(token.split(".")[1]));
        return payload.role || null;
    } catch {
        return null;
    }
};

const ShiftSlotDetailPage = () => {
    const { id } = useParams();

    const [slot, setSlot] = useState(null);
    const [myPreference, setMyPreference] = useState(null);
    const [loading, setLoading] = useState(true);

    const role = getRoleFromToken();

    // -------------------------
    // シフト取得
    // -------------------------
    const fetchSlot = async () => {
        const res = await getShiftSlot(id);
        setSlot(res.data);
    };

    // -------------------------
    // 自分の申請取得
    // -------------------------
    const fetchMyPreference = async () => {
        try {
            const res = await axios.get("/shift-preferences/me", {
                params: {
                    shift_slot_id: id,
                },
            });

            setMyPreference(res.data[0] ?? null);
        } catch {
            setMyPreference(null);
        }
    };

    useEffect(() => {
        const load = async () => {
            setLoading(true);
            await Promise.all([fetchSlot(), fetchMyPreference()]);
            setLoading(false);
        };

        load();
    }, [id]);

    if (loading) return <div>loading...</div>;
    if (!slot) return <div>not found</div>;

    return (
        <div style={{ padding: "20px" }}>
            <h2>シフト詳細</h2>

            <p>開始: {slot.start_at}</p>
            <p>終了: {slot.end_at}</p>
            <p>必要人数: {slot.required_staff_count}</p>

            <hr />

            {(role === "user" || role === "admin") && (
                <div style={{ marginTop: "20px" }}>
                    <h3>シフト申請</h3>

                    {/* 申請済み */}
                    {myPreference ? (
                        <div
                            style={{
                                padding: "10px",
                                background: "#f3f4f6",
                                borderRadius: "6px",
                            }}
                        >
                            <p>申請済み</p>
                            <p>希望度: {myPreference.priority}</p>
                            <p>メモ: {myPreference.note}</p>
                        </div>
                    ) : (
                        <PreferenceForm
                            shiftSlotId={id}
                            onSuccess={(data) => setMyPreference(data)}
                        />
                    )}
                </div>
            )}
        </div>
    );
};

export default ShiftSlotDetailPage;