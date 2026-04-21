const Spinner = () => {
    return (
        <div style={{ textAlign: "center", padding: "20px" }}>
            <div
                style={{
                    width: "30px",
                    height: "30px",
                    border: "4px solid #ccc",
                    borderTop: "4px solid #2563eb",
                    borderRadius: "50%",
                    animation: "spin 1s linear infinite",
                    margin: "0 auto",
                }}
            />

            <style>
                {`
            @keyframes spin {
              0% { transform: rotate(0deg); }
              100% { transform: rotate(360deg); }
            }
          `}
            </style>
        </div>
    );
};

export default Spinner;