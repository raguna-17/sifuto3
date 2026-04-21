import { Link } from "react-router-dom";

const Home = () => {
    return (
        <div>
            <h1>ホーム</h1>

            <ul>
                <li>
                    <Link to="/job-applications">応募履歴</Link>
                </li>
                <li>
                    <Link to="/organizations">求人応募</Link>
                </li>
            </ul>
        </div>
    );
};

export default Home;