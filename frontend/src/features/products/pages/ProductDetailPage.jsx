import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getProductById } from "../api";
import { addToCart } from "../../cart/api";

const ProductDetailPage = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [adding, setAdding] = useState(false);

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const data = await getProductById(id);
                setProduct(data);
            } catch (err) {
                setError("商品取得失敗");
            } finally {
                setLoading(false);
            }
        };

        fetchProduct();
    }, [id]);

    const handleAddToCart = async () => {
        try {
            setAdding(true);

            await addToCart(product.id, 1);

            // カートへ遷移（少し待つと安定）
            setTimeout(() => {
                navigate("/cart");
            }, 100);

        } catch (err) {
            console.error(err);
            alert("カート追加に失敗しました");
        } finally {
            setAdding(false);
        }
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;
    if (!product) return <p>商品が見つかりません</p>;

    return (
        <div>
            <h1>{product.name}</h1>

            <p>{product.description}</p>

            <p>価格: ¥{product.price}</p>

            <p>在庫: {product.stock}</p>

            {product.image_url && (
                <img
                    src={product.image_url}
                    alt={product.name}
                    width="300"
                />
            )}

            <button
                onClick={handleAddToCart}
                disabled={adding}
                style={{
                    marginTop: "16px",
                    padding: "10px 16px",
                }}
            >
                {adding ? "追加中..." : "カートに追加"}
            </button>
        </div>
    );
};

export default ProductDetailPage;