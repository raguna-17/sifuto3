import { useState } from "react";
import { createShiftSlot } from "./api";

const ShiftSlotCreatePage = () => {
    const [form, setForm] = useState({
        start_at: "",
        end_at: "",
        required_staff_count: 1,
    });

    const handleSubmit = async () => {
        await createShiftSlot(form);
        alert("作成完了");
    };

    return (
        <div>
            <h2>シフト作成（管理者）</h2>

            <input
                type="datetime-local"
                onChange={(e) =>
                    setForm({ ...form, start_at: e.target.value })
                }
            />

            <input
                type="datetime-local"
                onChange={(e) =>
                    setForm({ ...form, end_at: e.target.value })
                }
            />

            <input
                type="number"
                value={form.required_staff_count}
                onChange={(e) =>
                    setForm({
                        ...form,
                        required_staff_count: Number(e.target.value),
                    })
                }
            />

            <button onClick={handleSubmit}>
                作成
            </button>
        </div>
    );
};

export default ShiftSlotCreatePage;