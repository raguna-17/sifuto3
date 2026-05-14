import api from "../../api/axios";


// -------------------------
// カート取得
// -------------------------

export const getCartItems = async () => {
    const response = await api.get("/cart/");
    return response.data;
};


// -------------------------
// カート追加
// -------------------------

export const addToCart = async (productId, quantity = 1) => {
    const response = await api.post("/cart/", {
        product_id: productId,
        quantity,
    });

    return response.data;
};


// -------------------------
// 数量更新
// -------------------------

export const updateCartItem = async (productId, quantity) => {
    const response = await api.patch(`/cart/${productId}`, {
        quantity,
    });

    return response.data;
};


// -------------------------
// 削除
// -------------------------

export const deleteCartItem = async (productId) => {
    const response = await api.delete(`/cart/${productId}`);
    return response.data;
};


// -------------------------
// カート全削除
// -------------------------

export const clearCart = async () => {
    const response = await api.delete("/cart/");
    return response.data;
};