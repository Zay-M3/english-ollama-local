

export function Button({
    label,
    onClick,
    className = "",
    disabled = false,
}: {
    label: string;
    onClick: () => void;
    className?: string;
    disabled?: boolean;
}) {
    return (
    <button
        className={`bg-blue-500 text-white px-4 py-2 rounded-full hover:bg-blue-600 transition ${className}`}
        onClick={onClick}
        disabled={disabled}
      >
        {label}
      </button>
    );
}