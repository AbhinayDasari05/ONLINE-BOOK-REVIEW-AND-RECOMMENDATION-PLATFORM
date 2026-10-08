import logging
from flask import request
from flask_login import current_user
from app.extensions import db
from app.models.audit_log import AuditLog

logger = logging.getLogger("security.audit")

FORBIDDEN_KEYS = {'password', 'password_hash', 'token', 'secret', 'secret_key', 'csrf_token'}

def sanitize_audit_details(details: dict or str) -> str:
    """Scrub sensitive secrets from audit data before persistence (CTRL-08, RULE H)."""
    if isinstance(details, dict):
        sanitized = {}
        for k, v in details.items():
            if any(forbidden in k.lower() for forbidden in FORBIDDEN_KEYS):
                sanitized[k] = "[REDACTED]"
            else:
                sanitized[k] = str(v)[:200]
        return str(sanitized)
    elif isinstance(details, str):
        # Enforce max length on details string
        return details[:1000]
    return ""

def log_audit_event(action: str, resource_type: str, resource_id=None, status: str = "SUCCESS", details=None, user=None):
    """
    Persist structured security audit trail (COMP-08, CTRL-08).
    Captures: timestamp, actor, action, resource, client IP, outcome.
    """
    try:
        actor_id = None
        actor_name = "anonymous"

        if user and hasattr(user, 'id'):
            actor_id = user.id
            actor_name = getattr(user, 'username', 'unknown')
        elif current_user and current_user.is_authenticated:
            actor_id = current_user.id
            actor_name = current_user.username

        client_ip = request.remote_addr if request else "127.0.0.1"
        sanitized_details = sanitize_audit_details(details) if details else None

        log_entry = AuditLog(
            user_id=actor_id,
            username=actor_name,
            action=action[:80],
            resource_type=resource_type[:50],
            resource_id=str(resource_id)[:50] if resource_id is not None else None,
            ip_address=client_ip,
            status=status[:20],
            details=sanitized_details
        )
        db.session.add(log_entry)
        db.session.commit()

        logger.info(f"AUDIT: [{status}] {actor_name} performed {action} on {resource_type}:{resource_id} from {client_ip}")
    except Exception as e:
        logger.error(f"Failed to record audit event: {e}")
        db.session.rollback()
