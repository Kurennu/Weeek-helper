def validate_title(title):
    if not title:
        return False, "Пустой заголовок"

    if len(title) < 10:
        return False, "Слишком короткий заголовок"

    verbs = [
        'создать', 'добавить', 'удалить', 'изменить',
        'обновить', 'исправить', 'настроить', 'проверить'
    ]
    
    has_verb = any(verb in title.lower() for verb in verbs)

    if not has_verb:
        return False, "Нет глагола действия"

    return True, "OK"
