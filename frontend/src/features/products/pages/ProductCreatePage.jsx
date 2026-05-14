import {
    useState,
} from "react";

import {
    useNavigate,
} from "react-router-dom";

import {
    createProduct,
} from "../api";

const ProductCreatePage = () => {
    const navigate = useNavigate();

    const [name, setName] =
        useState("");

    const [description,
        setDescription] =
        useState("");

    const [price, setPrice] =
        useState("");

    const [stock, setStock] =
        useState("");

    const [imageUrl,
        setImageUrl] =
        useState("");

    const [error, setError] =
        useState("");

    const [loading, setLoading] =
        useState(false);

    const handleSubmit = async (
        e
    ) => {
        e.preventDefault();

        setError("");

        try {
            setLoading(true);

            await createProduct({
                name,
                description,
                price: Number(price),
                stock: Number(stock),
                image_url: imageUrl,
            });

            navigate("/products");

        } catch (err) {
            setError(
                err.response?.data?.detail ||
                err.message ||
                "商品作成失敗"
            );

        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>商品作成</h1>

            {error && (
                <p>{error}</p>
            )}

            <form onSubmit={handleSubmit}>
                <div>
                    <input
                        type="text"
                        placeholder="商品名"
                        value={name}
                        onChange={(e) =>
                            setName(
                                e.target.value
                            )
                        }
                    />
                </div>

                <div>
                    <textarea
                        placeholder="商品説明"
                        value={description}
                        onChange={(e) =>
                            setDescription(
                                e.target.value
                            )
                        }
                    />
                </div>

                <div>
                    <input
                        type="number"
                        placeholder="価格"
                        value={price}
                        onChange={(e) =>
                            setPrice(
                                e.target.value
                            )
                        }
                    />
                </div>

                <div>
                    <input
                        type="number"
                        placeholder="在庫"
                        value={stock}
                        onChange={(e) =>
                            setStock(
                                e.target.value
                            )
                        }
                    />
                </div>

                <div>
                    <input
                        type="text"
                        placeholder="画像URL"
                        value={imageUrl}
                        onChange={(e) =>
                            setImageUrl(
                                e.target.value
                            )
                        }
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                >
                    {loading
                        ? "作成中..."
                        : "商品作成"}
                </button>
            </form>
        </div>
    );
};

export default ProductCreatePage;