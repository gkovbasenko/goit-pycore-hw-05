from hw05.chatbot.decorators import input_error


@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts found."
    return "\n".join(f"{name}: {phone}" for name, phone in sorted(contacts.items()))
