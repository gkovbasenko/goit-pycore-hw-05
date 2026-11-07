from hw05.chatbot.decorators import input_error


@input_error
def add_contact(args, contacts):
    name, phone = args
    if name in contacts:
        return "Contact already exists."
    contacts[name] = phone
    return "Contact added."
