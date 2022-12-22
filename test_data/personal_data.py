from mimesis import Person

generator = Person()


def create_person(
        firstname=None,
        lastname=None,
        email=None,
        telephone=None,
        password=None,
        password_confirm=None
):
    password = password if password is not None else generator.password()
    return {
        "firstname": firstname if firstname is not None else generator.first_name(),
        "lastname": lastname if lastname is not None else generator.last_name(),
        "email": email if email is not None else generator.email(),
        "telephone": telephone if telephone is not None else generator.telephone(),
        "password": password if password is not None else password,
        "password_confirm": password_confirm if password_confirm is not None else password
    }


def correct_random_person():
    return create_person()


def person_with_empty_firstname():
    return create_person(firstname="")


def person_with_empty_lastname():
    return create_person(lastname="")


def person_with_empty_email():
    return create_person(email="")


def person_with_empty_telephone():
    return create_person(telephone="")


def person_with_empty_password():
    return create_person(password="", password_confirm="password2")


def person_with_empty_password_confirm():
    return create_person(password_confirm="")


def person_with_different_passwords():
    return create_person(password="password1", password_confirm="password2")