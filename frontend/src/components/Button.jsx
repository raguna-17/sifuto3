const Button = ({
    children,
    onClick,
    disabled,
    variant = "primary",
}) => {
    const baseStyle = {
        padding: "10px 16px",
        borderRadius: "10px",
        border: "none",
        cursor: "pointer",
        fontWeight: 600,
        fontSize: "14px",
        transition: "all 0.2s ease",
        boxShadow: "0 2px 6px rgba(0,0,0,0.08)",
        transform: "translateY(0)",
    };

    const styles = {
        primary: {
            background: "linear-gradient(135deg, #2563eb, #1d4ed8)",
            color: "white",
        },
        danger: {
            background: "linear-gradient(135deg, #ef4444, #dc2626)",
            color: "white",
        },
        secondary: {
            background: "linear-gradient(135deg, #f3f4f6, #e5e7eb)",
            color: "#111827",
        },
    };

    const hoverStyle = {
        transform: "translateY(-2px)",
        boxShadow: "0 6px 16px rgba(0,0,0,0.15)",
        filter: "brightness(1.05)",
    };

    const activeStyle = {
        transform: "translateY(0px)",
        boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
    };

    return (
        <button
            onClick={onClick}
            disabled={disabled}
            style={{
                ...baseStyle,
                ...styles[variant],
                opacity: disabled ? 0.5 : 1,
            }}
            onMouseEnter={(e) => {
                if (!disabled) {
                    Object.assign(e.currentTarget.style, hoverStyle);
                }
            }}
            onMouseLeave={(e) => {
                Object.assign(e.currentTarget.style, {
                    transform: "translateY(0)",
                    boxShadow: "0 2px 6px rgba(0,0,0,0.08)",
                    filter: "none",
                });
            }}
            onMouseDown={(e) => {
                if (!disabled) {
                    Object.assign(e.currentTarget.style, activeStyle);
                }
            }}
            onMouseUp={(e) => {
                if (!disabled) {
                    Object.assign(e.currentTarget.style, hoverStyle);
                }
            }}
        >
            {children}
        </button>
    );
};

export default Button;