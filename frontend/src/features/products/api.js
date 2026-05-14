import api from "../../api/axios";


// -------------------------
// get all products
// -------------------------

export const getProducts = async () => {
    const response = await api.get(
        "/products"
    );

    return response.data;
};


// -------------------------
// get product by id
// -------------------------

export const getProductById = async (
    productId
) => {
    const response = await api.get(
        `/products/${productId}`
    );

    return response.data;
};


// -------------------------
// create product
// -------------------------

export const createProduct = async (
    payload
) => {
    const response = await api.post(
        "/products",
        payload
    );

    return response.data;
};