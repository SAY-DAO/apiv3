from .base import BaseSMSBackend


class ConsoleSMSBackend(BaseSMSBackend):

    def send(self, message, recipient):
        print(
            f'\033[92mSMS sent to {recipient}: {message}'
        )
