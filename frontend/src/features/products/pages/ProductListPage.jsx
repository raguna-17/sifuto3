import {
    useEffect,
    useState,
} from "react";

import { Link } from "react-router-dom";

import {
    getProducts,
} from "../api";

const ProductListPage = () => {
    const [products, setProducts] =
        useState([]);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState("");

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const data =
                    await getProducts();

                setProducts(data);

            } catch (err) {
                setError(
                    "商品取得失敗"
                );

            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, []);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <div>
            <h1>商品一覧</h1>

            {products.length === 0 ? (
                <p>
                    商品がありません
                </p>

            ) : (
                products.map((product) => (
                    <div
                        key={product.id}
                        style={{
                            border:
                                "1px solid #ccc",
                            padding: "12px",
                            marginBottom: "12px",
                        }}
                    >
                        <h2>
                            {product.name}
                        </h2>

                        <p>
                            ¥{product.price}
                        </p>

                        <p>
                            在庫:
                            {" "}
                            {product.stock}
                        </p>

                        <Link
                            to={`/products/${product.id}`}
                        >
                            詳細を見る
                        </Link>
                    </div>
                ))
            )}
        </div>
    );
};

export default ProductListPage;