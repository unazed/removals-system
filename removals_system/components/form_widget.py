from PySide6.QtWidgets import QWidget

from .forms.form import Form

from typing import final


@final
class FormWidget(QWidget, Form):
    pass