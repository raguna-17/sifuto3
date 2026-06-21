import { useEffect, useState } from "react";
import {
    getShiftAssignments,
    getMyShiftAssignments,
} from "./api";

const ShiftFlowViewPage = () => {
    const [data, setData] = useState([]);
    const role = localStorage.getItem("role");

    useEffect(() => {
        const fetchData = async () => {
            const res =
                role === "admin"
                    ? await getShiftAssignments()
                    : await getMyShiftAssignments();

            setData(res.data);
        };

        fetchData();
    }, [role]);

    return (
        <div>
            <h2>確定シフト</h2>

            {data.length === 0 && <p>まだありません</p>}

            <ul>
                {data.map((a) => (
                    <li key={a.id}>
                        Slot: {a.slot_id} / User: {a.user_id}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ShiftFlowViewPage;