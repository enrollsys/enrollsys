def site_context(request):
    role = None
    if request.user.is_authenticated:
        # Superusers are always treated as admin
        if request.user.is_superuser:
            role = "admin"
        elif hasattr(request.user, "profile"):
            role = request.user.profile.role
    return {
        "current_role": role,
        "site_name": "Управление организацией приема",
    }
