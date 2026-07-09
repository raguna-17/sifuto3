import { useState } from "react";
import {
    generateShiftFlow,
    confirmShiftFlow,
} from "./api";

import { getUsers } from "../users/api";

const ShiftFlowCreatePage = () => {
    const [loading, setLoading] = useState(false);

    const [result, setResult] = useState(null);

    const [allUsers, setAllUsers] = useState([]);

    // =========================
    // generate
    // =========================
    const handleGenerate = async () => {
        setLoading(true);

        try {
            const [scheduleRes, usersRes] =
                await Promise.all([
                    generateShiftFlow(),
                    getUsers(),
                ]);

            const assignments =
                scheduleRes.data.assignments ?? {};

            setResult(assignments);
            setAllUsers(usersRes.data);
        } catch (error) {
            console.error(error);
            alert("シフト生成に失敗しました");
        } finally {
            setLoading(false);
        }
    };

    // =========================
    // edit
    // =========================
    const handleUserChange = (
        slotId,
        value
    ) => {
        const userIds = value
            .split(",")
            .map((v) => v.trim())
            .filter((v) => v !== "")
            .map(Number);

        setResult((prev) => ({
            ...prev,
            [slotId]: userIds,
        }));
    };

    // =========================
    // validation
    // =========================
    const validateAssignments = () => {
        const validUserIds = new Set(
            allUsers.map((u) => u.id)
        );

        for (const [
            slotId,
            userIds,
        ] of Object.entries(result)) {
            if (!Array.isArray(userIds)) {
                return `Slot ${slotId} の形式が不正です`;
            }

            for (const userId of userIds) {
                if (
                    !Number.isInteger(userId)
                ) {
                    return `Slot ${slotId} に不正なIDがあります`;
                }

                if (userId <= 0) {
                    return `Slot ${slotId} に不正なIDがあります`;
                }

                if (
                    !validUserIds.has(userId)
                ) {
                    return `Slot ${slotId}: User ${userId} は存在しません`;
                }
            }
        }

        return null;
    };

    // =========================
    // save
    // =========================
    const handleSave = async () => {
        if (!result) return;

        const validationError = validateAssignments();

        if (validationError) {
            alert(validationError);
            return;
        }

        try {
            await confirmShiftFlow(result);

            alert("確定しました");
        } catch (error) {
            console.error(error);
            alert("保存に失敗しました");
        }
    };
    return (
        <div>
            <h2>
                シフト生成（管理者）
            </h2>

            <button
                onClick={handleGenerate}
                disabled={loading}
            >
                {loading
                    ? "生成中..."
                    : "生成する"}
            </button>

            {result && (
                <>
                    <h3>生成結果</h3>

                    <p>
                        ユーザーIDを
                        カンマ区切りで
                        編集できます
                    </p>

                    {Object.entries(result).map(
                        ([slotId, users]) => (
                            <div
                                key={slotId}
                                style={{
                                    marginBottom:
                                        "12px",
                                }}
                            >
                                <strong>
                                    Slot {slotId}
                                </strong>

                                <div>
                                    <input
                                        type="text"
                                        value={users.join(
                                            ","
                                        )}
                                        onChange={(
                                            e
                                        ) =>
                                            handleUserChange(
                                                slotId,
                                                e
                                                    .target
                                                    .value
                                            )
                                        }
                                        placeholder="例: 1,2,3"
                                        style={{
                                            width:
                                                "300px",
                                        }}
                                    />
                                </div>
                            </div>
                        )
                    )}

                    <button
                        onClick={handleSave}
                    >
                        確定保存
                    </button>
                </>
            )}
        </div>
    );
};

export default ShiftFlowCreatePage;