class BaseSMSBackend:

    def send(self, message, recipient):
        raise NotImplementedError(
            'subclasses of BaseEmailBackend must override send_messages() method')