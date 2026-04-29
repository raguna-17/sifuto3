import { useEffect, useState } from "react";
import {
    getOrganizations,
    createOrganization,
    updateOrganization,
    deleteOrganization,
} from "./api";

export const useOrganizations = () => {
    const [orgs, setOrgs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // ===== 初期取得 =====
    useEffect(() => {
        fetchOrganizations();
    }, []);

    const fetchOrganizations = async () => {
        try {
            setLoading(true);
            const data = await getOrganizations();
            setOrgs(data);
        } catch (err) {
            setError("取得に失敗しました");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    // ===== 作成 =====
    const createOrg = async (data) => {
        try {
            const newOrg = await createOrganization(data);
            setOrgs((prev) => [...prev, newOrg]);
            return newOrg;
        } catch (err) {
            console.error(err);
            throw err;
        }
    };

    // ===== 更新 =====
    const updateOrg = async (id, data) => {
        try {
            const updated = await updateOrganization(id, data);

            setOrgs((prev) =>
                prev.map((o) => (o.id === updated.id ? updated : o))
            );

            return updated;
        } catch (err) {
            console.error(err);
            throw err;
        }
    };

    // ===== 削除 =====
    const deleteOrg = async (id) => {
        try {
            await deleteOrganization(id);
            setOrgs((prev) => prev.filter((o) => o.id !== id));
        } catch (err) {
            console.error(err);
            throw err;
        }
    };

    return {
        orgs,
        loading,
        error,
        createOrg,
        updateOrg,
        deleteOrg,
        refetch: fetchOrganizations,
    };
};