from datetime import datetime

from sqlalchemy.orm import Session

from app import models

DEFAULT_VM_POOL = [
    {"name": "proxy-1", "host": "127.0.0.1", "port": 1080, "protocol": "socks5"},
    {"name": "proxy-2", "host": "127.0.0.1", "port": 8080, "protocol": "http"},
    {"name": "proxy-3", "host": "127.0.0.1", "port": 3128, "protocol": "https"},
]


def seed_virtual_machines(db: Session) -> int:
    if db.query(models.VirtualMachine).count() > 0:
        return 0

    db.add_all(models.VirtualMachine(**vm_data) for vm_data in DEFAULT_VM_POOL)
    db.commit()
    return len(DEFAULT_VM_POOL)


def get_user_by_activation_key(db: Session, activation_key: str):
    return (
        db.query(models.User)
        .filter(models.User.activation_key == activation_key)
        .first()
    )


def get_assigned_vm_for_user(db: Session, user_id: int):
    return (
        db.query(models.VirtualMachine)
        .filter(models.VirtualMachine.current_user_id == user_id)
        .first()
    )


def allocate_vm_to_user(db: Session, user: models.User):
    query = (
        db.query(models.VirtualMachine)
        .filter(
            models.VirtualMachine.current_user_id.is_(None),
            models.VirtualMachine.is_active.is_(True),
        )
        .order_by(models.VirtualMachine.id.asc())
    )

    if db.bind and db.bind.dialect.name == "postgresql":
        query = query.with_for_update(skip_locked=True)

    free_vm = query.first()
    if free_vm is None:
        return None

    free_vm.current_user_id = user.id
    free_vm.last_used_at = datetime.utcnow()
    user.activation_key = None
    user.activation_key_expires = None
    db.commit()
    db.refresh(free_vm)
    db.refresh(user)
    return free_vm


def consume_activation_key(db: Session, user: models.User):
    user.activation_key = None
    user.activation_key_expires = None
    db.commit()
    db.refresh(user)
    return user


def release_vm_for_user(db: Session, user_id: int):
    assigned_vm = (
        db.query(models.VirtualMachine)
        .filter(models.VirtualMachine.current_user_id == user_id)
        .first()
    )
    if assigned_vm is None:
        return None

    assigned_vm.current_user_id = None
    assigned_vm.last_used_at = datetime.utcnow()
    db.commit()
    db.refresh(assigned_vm)
    return assigned_vm
