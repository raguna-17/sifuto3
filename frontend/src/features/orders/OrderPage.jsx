import { useEffect, useState } from "react";

import {
    getOrders,
    cancelOrder,
} from "./api";

export default function OrderPage() {

    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);

    // -------------------------
    // 注文取得
    // -------------------------
    const fetchOrders = async () => {
        try {
            const data = await getOrders();
            setOrders(data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchOrders();
    }, []);

    // -------------------------
    // キャンセル
    // -------------------------
    const handleCancel = async (orderId) => {
        const ok = window.confirm("注文をキャンセルしますか？");
        if (!ok) return;

        try {
            await cancelOrder(orderId);

            setOrders((prev) =>
                prev.filter((order) => order.id !== orderId)
            );
        } catch (error) {
            console.error(error);
            alert(error.response?.data?.detail || "キャンセル失敗");
        }
    };

    if (loading) {
        return <p>Loading...</p>;
    }

    return (
        <div>
            <h1>注文履歴</h1>

            {orders.length === 0 ? (
                <p>注文履歴がありません</p>
            ) : (
                orders.map((order) => (
                    <div
                        key={order.id}
                        style={{
                            border: "1px solid #ccc",
                            padding: "16px",
                            marginBottom: "16px",
                        }}
                    >
                        <p>注文ID: {order.id}</p>

                        <p>ステータス: {order.status}</p>

                        <p>合計金額: ¥{order.total_price}</p>

                        <p>
                            注文日時:{" "}
                            {new Date(order.created_at).toLocaleString()}
                        </p>

                        {/* -------------------------
                            注文明細（ここが重要）
                        ------------------------- */}
                        <div style={{ marginTop: "12px" }}>
                            <p>商品一覧:</p>

                            {order.items?.map((item) => (
                                <div
                                    key={item.id}
                                    style={{
                                        paddingLeft: "12px",
                                        marginBottom: "6px",
                                    }}
                                >
                                    <p>商品ID: {item.product_id}</p>
                                    <p>数量: {item.quantity}</p>
                                    <p>
                                        単価: ¥{item.price_at_purchase}
                                    </p>
                                </div>
                            ))}
                        </div>

                        {/* キャンセルボタン */}
                        {order.status === "pending" && (
                            <button
                                onClick={() => handleCancel(order.id)}
                                style={{
                                    marginTop: "12px",
                                    padding: "8px 12px",
                                }}
                            >
                                キャンセル
                            </button>
                        )}
                    </div>
                ))
            )}
        </div>
    );
}