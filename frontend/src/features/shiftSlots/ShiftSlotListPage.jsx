import { useEffect, useState } from "react";
import { getShiftSlots, deleteShiftSlot } from "./api";
import { Link } from "react-router-dom";

const ShiftSlotListPage = () => {
    const [slots, setSlots] = useState([]);

    const role = localStorage.getItem("role");

    const fetchSlots = async () => {
        const res = await getShiftSlots();
        setSlots(res.data);
    };

    useEffect(() => {
        fetchSlots();
    }, []);

    const handleDelete = async (id) => {
        await deleteShiftSlot(id);
        fetchSlots();
    };

    return (
        <div>
            <h2>シフトスロット一覧</h2>

            <ul>
                {slots.map((slot) => (
                    <li key={slot.id}>
                        <Link to={`/shift-slots/${slot.id}`}>
                            {slot.start_at} - {slot.end_at}
                        </Link>

                        {role === "admin" && (
                            <button onClick={() => handleDelete(slot.id)}>
                                削除
                            </button>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ShiftSlotListPage;