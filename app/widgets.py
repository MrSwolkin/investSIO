"""
Custom Django form widgets with TailwindCSS styling.

These widgets replace Bootstrap form-control classes with Tailwind design system classes
defined in theme/static_src/src/styles.css
"""

from django import forms


class TailwindTextInput(forms.TextInput):
    """
    Text input widget with Tailwind styling.
    Uses the .input class from the design system.
    """
    def __init__(self, attrs=None):
        default_attrs = {'class': 'input'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class TailwindNumberInput(forms.NumberInput):
    """
    Number input widget with Tailwind styling.
    Uses the .input class from the design system.
    """
    def __init__(self, attrs=None):
        default_attrs = {'class': 'input'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class TailwindSelect(forms.Select):
    """
    Select dropdown widget with Tailwind styling.
    Uses the .select class from the design system with custom arrow icon.
    """
    def __init__(self, attrs=None):
        default_attrs = {'class': 'select'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class TailwindTextarea(forms.Textarea):
    """
    Textarea widget with Tailwind styling.
    Uses the .textarea class from the design system.
    Default: 3 rows, resizable vertically.
    """
    def __init__(self, attrs=None):
        default_attrs = {'class': 'textarea', 'rows': 3}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class TailwindDateInput(forms.DateInput):
    """
    Date input widget with Tailwind styling.
    Uses HTML5 date input type with .input class from the design system.
    """
    def __init__(self, attrs=None):
        default_attrs = {'class': 'input', 'type': 'date'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class TailwindCheckboxInput(forms.CheckboxInput):
    """
    Checkbox input widget with Tailwind styling.
    Uses the .checkbox class from the design system.
    """
    def __init__(self, attrs=None):
        default_attrs = {'class': 'checkbox'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
