def site_context(request):
    role = None
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        role = request.user.profile.role
    return {
        'current_role': role,
        'site_name': 'Приемная комиссия МУ им. С.Ю. Витте',
    }
