class StateManager:
    _instance = None

    def __init__(self):
        if StateManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            StateManager._instance = self
            self.is_forwarding = False
            self.is_adding_content = False
            self.is_adding_content_to_button_name = ""

    @staticmethod
    def get_instance():
        if StateManager._instance is None:
            StateManager()
        return StateManager._instance
