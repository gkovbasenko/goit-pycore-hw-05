from hw05.chatbot.decorators import input_error


@input_error
def change_contact(args, contacts):
    name, phone = args
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."
