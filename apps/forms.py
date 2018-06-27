from wtforms import Form


class BaseForm(Form):
    def get_error(self):
        try:
            message = self.errors.popitem()[1][0]
        except Exception as e:
            message = self.errors
        return message

    def validate(self):
        # return super(BaseForm, self).validate()
        return super().validate()
