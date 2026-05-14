import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Layout from "./layouts/Layout";

import LoginPage from "./features/auth/LoginPage";
import RegisterPage from "./features/auth/RegisterPage";

import Home from "./pages/Home";

// products
import ProductListPage from "./features/products/pages/ProductListPage";
import ProductDetailPage from "./features/products/pages/ProductDetailPage";
import ProductCreatePage from "./features/products/pages/ProductCreatePage";

// cart
import CartPage from "./features/cart/CartPage";

// orders
import OrderPage from "./features/orders/OrderPage";


// -------------------------
// auth check
// -------------------------

const isAuthenticated = () => {
  return !!localStorage.getItem(
    "token"
  );
};


// -------------------------
// private route
// -------------------------

const PrivateRoute = ({
  children,
}) => {
  return isAuthenticated()
    ? children
    : (
      <Navigate
        to="/login"
        replace
      />
    );
};


function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* -------------------------
            public
        ------------------------- */}

        <Route
          path="/login"
          element={<LoginPage />}
        />

        <Route
          path="/register"
          element={<RegisterPage />}
        />


        {/* -------------------------
            private
        ------------------------- */}

        <Route
          path="/"
          element={
            <PrivateRoute>
              <Layout />
            </PrivateRoute>
          }
        >

          {/* home */}
          <Route
            index
            element={<Home />}
          />


          {/* -------------------------
              products
          ------------------------- */}

          <Route
            path="products"
            element={<ProductListPage />}
          />

          <Route
            path="products/create"
            element={<ProductCreatePage />}
          />

          <Route
            path="products/:id"
            element={<ProductDetailPage />}
          />


          {/* -------------------------
              cart
          ------------------------- */}

          <Route
            path="cart"
            element={<CartPage />}
          />


          {/* -------------------------
              orders
          ------------------------- */}

          <Route
            path="orders"
            element={<OrderPage />}
          />

        </Route>


        {/* -------------------------
            not found
        ------------------------- */}

        <Route
          path="*"
          element={
            <Navigate
              to="/"
              replace
            />
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;