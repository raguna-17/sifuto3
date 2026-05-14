import { Link } from "react-router-dom";

import Button from "../components/Button";
import Spinner from "../components/Spinner";


const cardStyle = {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    padding: "20px",
    width: "220px",
    border: "1px solid #ddd",
    borderRadius: "10px",
    backgroundColor: "#fff",
    boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
};


const Home = () => {

    const loading = false;

    if (loading) {
        return <Spinner />;
    }

    return (
        <div
            style={{
                padding: "20px",
                textAlign: "center",
            }}
        >
            <h1>ECサイト ダッシュボード</h1>

            <p>
                商品・カート・注文を管理できます。
            </p>

            <div
                style={{
                    display: "flex",
                    gap: "20px",
                    justifyContent: "center",
                    flexWrap: "wrap",
                    marginTop: "30px",
                }}
            >

                {/* 商品一覧 */}
                <div style={cardStyle}>
                    <h2>商品一覧</h2>

                    <p>
                        商品の閲覧・追加・編集
                    </p>

                    <Link to="/products">
                        <Button>
                            商品を見る
                        </Button>
                    </Link>
                </div>


                {/* カート */}
                <div style={cardStyle}>
                    <h2>カート</h2>

                    <p>
                        カート内の商品確認
                    </p>

                    <Link to="/cart">
                        <Button>
                            カートへ
                        </Button>
                    </Link>
                </div>


                {/* 注文履歴 */}
                <div style={cardStyle}>
                    <h2>注文履歴</h2>

                    <p>
                        注文一覧・購入履歴確認
                    </p>

                    <Link to="/orders">
                        <Button>
                            注文履歴を見る
                        </Button>
                    </Link>
                </div>

            </div>
        </div>
    );
};

export default Home;