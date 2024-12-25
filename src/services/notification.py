import mailtrap as mt


class NotificationService:
    def __init__(self):
        pass

    def send_notification(self, message):

        mail = mt.Mail(
            sender=mt.Address(email="hello@demomailtrap.com", name="Mailtrap Test"),
            to=[mt.Address(email="ssahadev2024@gmail.com")],
            subject="Scraping Status",
            text=message,
            category="Integration Test",
        )

        client = mt.MailtrapClient(token="0d46d689dc4a56ebc80a49a19bc13fc1")
        response = client.send(mail)
