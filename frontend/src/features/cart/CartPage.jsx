import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    getCartItems,
    updateCartItem,
    deleteCartItem,
    clearCart,
} from "./api";

import { createOrder } from "../orders/api";

export default function CartPage() {
    const navigate = useNavigate();

    const [cartItems, setCartItems] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchCart = async () => {
        try {
            const data = await getCartItems();
            setCartItems(data);
        } catch (error) {
            console.log(error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCart();
    }, []);

    const handleQuantityChange = async (productId, quantity) => {
        if (quantity < 1) return;

        try {
            await updateCartItem(productId, quantity);

            setCartItems((prev) =>
                prev.map((item) =>
                    item.product_id === productId
                        ? { ...item, quantity }
                        : item
                )
            );
        } catch (error) {
            console.log(error);
        }
    };

    const handleDelete = async (productId) => {
        try {
            await deleteCartItem(productId);

            setCartItems((prev) =>
                prev.filter(
                    (item) => item.product_id !== productId
                )
            );
        } catch (error) {
            console.log(error);
        }
    };

    const handleClear = async () => {
        try {
            await clearCart();
            setCartItems([]);
        } catch (error) {
            console.log(error);
        }
    };

    const handleOrder = async () => {
        try {
            for (const item of cartItems) {
                await createOrder(
                    item.product_id,
                    item.quantity
                );
            }

            await clearCart();
            setCartItems([]);

            navigate("/orders");
        } catch (error) {
            console.log(error);
        }
    };

    if (loading) {
        return <p>Loading...</p>;
    }

    return (
        <div>
            <h1>Cart</h1>

            {cartItems.length === 0 ? (
                <p>カートが空です</p>
            ) : (
                <>
                    {cartItems.map((item) => (
                        <div
                            key={item.id}
                            style={{
                                border: "1px solid #ccc",
                                padding: "12px",
                                marginBottom: "12px",
                            }}
                        >
                            <p>
                                Product ID: {item.product_id}
                            </p>

                            <p>
                                Quantity: {item.quantity}
                            </p>

                            <div>
                                <button
                                    onClick={() =>
                                        handleQuantityChange(
                                            item.product_id,
                                            item.quantity - 1
                                        )
                                    }
                                >
                                    -
                                </button>

                                <button
                                    onClick={() =>
                                        handleQuantityChange(
                                            item.product_id,
                                            item.quantity + 1
                                        )
                                    }
                                >
                                    +
                                </button>
                            </div>

                            <button
                                onClick={() =>
                                    handleDelete(item.product_id)
                                }
                            >
                                削除
                            </button>
                        </div>
                    ))}

                    <button onClick={handleClear}>
                        カートを空にする
                    </button>

                    <button onClick={handleOrder}>
                        注文する
                    </button>
                </>
            )}
        </div>
    );
}