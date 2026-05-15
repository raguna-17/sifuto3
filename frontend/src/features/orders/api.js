import api from "../../api/axios";


// -------------------------
// 注文一覧取得
// -------------------------

export const getOrders = async () => {
    const response = await api.get("/orders/");
    return response.data;
};


// -------------------------
// 注文詳細
// -------------------------

export const getOrderDetail = async (orderId) => {
    const response = await api.get(`/orders/${orderId}`);
    return response.data;
};


// -------------------------
// 注文作成
// -------------------------

export const createOrder = async (productId, quantity) => {
    const response = await api.post("/orders/", {
        items: [
            {
                product_id: productId,
                quantity,
            },
        ],
    });

    return response.data;
};


// -------------------------
// 注文キャンセル
// -------------------------

export const cancelOrder = async (orderId) => {
    const response = await api.delete(
        `/orders/${orderId}`
    );

    return response.data;
};