function StatusToasts({ toasts, onDismiss }) {
  if (!toasts.length) {
    return null;
  }

  return (
    <div className="toast-stack" role="status" aria-live="polite">
      {toasts.map((toast) => (
        <div key={toast.id} className={`toast ${toast.type}`}>
          <p>{toast.message}</p>
          <button type="button" onClick={() => onDismiss(toast.id)} aria-label="Dismiss notification">
            x
          </button>
        </div>
      ))}
    </div>
  );
}

export default StatusToasts;
