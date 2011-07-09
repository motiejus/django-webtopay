from django import forms

class ValueHiddenInput(forms.HiddenInput):
    """ 
    Widget that renders only if it has a value.
    Used to remove unused fields.
    Stolen from django-paypal.
    """
    def render(self, name, value, attrs=None):
        if value is None:
            return u'' 
        else:
            return super(ValueHiddenInput, self).render(name, value, attrs)
