import uuid


def generate_session_id() -> str:
    """Create a simple session identifier for stateless frontends that still need correlation."""
    return str(uuid.uuid4())
