from enum import Enum


# Defines the UserRole enum to represent possible user roles in the system
class UserRole(str, Enum):
    USER = "user"  # Standard user with basic permissions
    ADMIN = "admin"  # Administrator with elevated permissions
    SUPER_ADMIN = "super_admin"  # Super administrator with full control
