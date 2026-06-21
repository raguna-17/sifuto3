import { useState } from "react";
import { createShiftPreference } from "./api";

const PreferenceForm = ({ shiftSlotId, onSuccess }) => {
    const [priority, setPriority] = useState("neutral");
    const [note, setNote] = useState("");
    const [loading, setLoading] = useState(false);
    const [open, setOpen] = useState(false);

    const handleSubmit = async () => {
        try {
            setLoading(true);

            const res = await createShiftPreference({
                shift_slot_id: Number(shiftSlotId),
                priority,
                note,
            });

            onSuccess?.(res.data);
            setOpen(false);

        } catch (err) {
            if (err.response?.status === 409) {
                alert("すでに申請済みです");
            } else {
                alert("エラーが発生しました");
            }
        } finally {
            setLoading(false);
        }
    };

    if (!open) {
        return (
            <button
                onClick={() => setOpen(true)}
                style={{
                    padding: "10px 16px",
                    background: "#2563eb",
                    color: "white",
                    border: "none",
                    borderRadius: "6px",
                }}
            >
                シフト申請する
            </button>
        );
    }

    return (
        <div style={{ marginTop: "10px", padding: "10px", border: "1px solid #ddd" }}>
            <h4>申請内容</h4>

            <div>
                <label>希望度：</label>
                <select
                    value={priority}
                    onChange={(e) => setPriority(e.target.value)}
                >
                    <option value="required">必須</option>
                    <option value="preferred">希望</option>
                    <option value="neutral">普通</option>
                    <option value="avoid">避けたい</option>
                    <option value="unavailable">不可</option>
                </select>
            </div>

            <div style={{ marginTop: "8px" }}>
                <label>メモ：</label>
                <input
                    value={note}
                    onChange={(e) => setNote(e.target.value)}
                    placeholder="任意"
                    style={{ marginLeft: "8px" }}
                />
            </div>

            <div style={{ marginTop: "12px" }}>
                <button
                    onClick={handleSubmit}
                    disabled={loading}
                >
                    {loading ? "送信中..." : "申請する"}
                </button>

                <button
                    onClick={() => setOpen(false)}
                    style={{ marginLeft: "10px" }}
                >
                    キャンセル
                </button>
            </div>
        </div>
    );
};

export default PreferenceForm;