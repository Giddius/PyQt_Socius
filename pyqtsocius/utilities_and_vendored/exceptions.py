

class PyQtSociusError(Exception):
    pass


class WrongInputFileTypeError(PyQtSociusError):
    __module__ = 'pyqtsocius'

    def __init__(self, input_file: str, expected_file_extension: str, extra_message: str = None):
        self.file = input_file
        self.file_ext = '.' + input_file.split('.')[-1]
        self.expected_ext = expected_file_extension
        self.message = f"File '{self.file}' with extension '{self.file_ext}', has wrong File type. expected extension --> '{self.expected_ext}'\n"
        if extra_message is not None:
            self.message += extra_message
        super().__init__(self.message)


class FeatureNotYetImplemented(PyQtSociusError):
    __module__ = 'pyqtsocius'

    def __init__(self, requested_feature):
        super().__init__(f"the feature '{requested_feature}' is currently not yet implemented")
