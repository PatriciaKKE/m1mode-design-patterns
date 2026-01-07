class NotificationConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.email_host = "smtp.techflow.com"
        self.email_port = 587
        self.sms_api_key = "sk_live_xxxxx"
        self.push_api_key = "pk_xxxxx"
        self.slack_webhook = "https://hooks.slack.com/..."
    
    def get_email_config(self):
        return {"host": self.email_host, "port": self.email_port}
    
    def get_sms_config(self):
        return {"api_key": self.sms_api_key}

# Test
if __name__ == "__main__":
    config1 = NotificationConfig()
    config2 = NotificationConfig()
    print(f"Même instance ? {config1 is config2}")