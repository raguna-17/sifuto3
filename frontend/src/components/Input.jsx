const Input = ({ value, onChange, placeholder, type = "text" }) => {
    return (
        <input
            type={type}
            value={value}
            placeholder={placeholder}
            onChange={onChange}
            style={{
                width: "80%",
                padding: "10px",
                marginBottom: "10px",
                borderRadius: "6px",
                border: "1px solid #ccc",
                outline: "none",
            }}
        />
    );
};

export default Input;