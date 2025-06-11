from PySide6.QtWidgets import QDateEdit
from PySide6.QtCore import QDate

from ..config.constants import ASSET_MAP

from .styled_widget import StyledWidget
from .validation_mixin import ValidationMixin


class DatePicker(QDateEdit, StyledWidget, ValidationMixin):
    def __init__(
        self,
        label: str = "",
        name: str | None = None,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.name = name

        self.setDisplayFormat("dd - MM - yyyy")
        self.setCalendarPopup(True)

        self.set_validation_trigger(self.dateChanged)
        self.setup_label(label)
        self.apply_styling(stylesheet=f"""
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: none;
            }}

            QDateEdit::down-arrow {{
                image: url({ASSET_MAP['calendar']});
                width: 16px;
                height: 16px;
            }}
        """)

    def serialize(self) -> QDate:
        return self.date()