#Vérifier si un utilisateur peut mettre à jour un autre utilisateur
def can_update_client(current_user, target_user):
    return current_user.id == target_user.id or current_user.role_id == 1

#Valider un email avant création
def is_valid_email(email):
    return "@" in email and "." in email

#Vérifier qu’un username est unique dans une liste d’utilisateurs
def is_unique_username(username, users):
    return all(u["username"] != username for u in users)
