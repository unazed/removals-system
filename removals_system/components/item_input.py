from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSpinBox, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, Signal, QSize
from functools import partial

from ..config.constants import ASSET_MAP

from .svg_pixmap import SVGPixmap
from .combo_box import ComboBox
from .primary_button import PrimaryButton
from .validation_mixin import ValidationMixin


class ItemInput(QWidget, ValidationMixin):
    state = Signal(str)

    def __init__(
        self,
        label: str,
        *,
        name: str | None = None,
        min: int = 1,
        step: int = 1
    ) -> None:
        super().__init__()
        self.name = name

        layout = QVBoxLayout(self)
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(min)
        self.spinbox.setSingleStep(step)
        self.spinbox.setFixedSize(48, 32)

        self.combo_box = ComboBox(label)
        self.add_button = PrimaryButton("+")
        self.add_button.setFixedSize(32, 32)
        self.add_button.clicked.connect(self.add_item)

        input_layout.addWidget(self.spinbox, alignment=Qt.AlignmentFlag.AlignBottom)
        input_layout.addWidget(self.combo_box)
        input_layout.addWidget(self.add_button, alignment=Qt.AlignmentFlag.AlignBottom)
        layout.addLayout(input_layout)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Qty", "Item name", ""])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        self.state.connect(self.combo_box.state.emit)

    def add_combo_items(self, *items: str) -> None:
        for item in items:
            self.combo_box.addItem(item)

    def add_item(self):
        qty = self.spinbox.value()
        item_name = self.combo_box.serialize()
        if not item_name:
            return

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(qty)))
        self.table.setItem(row, 1, QTableWidgetItem(item_name))

        container = QWidget()
        layout = QHBoxLayout(container)

        icon_pixmap = SVGPixmap(ASSET_MAP['x']).colored(QColor("#888"))
        remove_button = QPushButton()
        remove_button.setIcon(icon_pixmap)
        remove_button.setIconSize(QSize(16, 16))
        remove_button.setFixedSize(24, 24)
        remove_button.setStyleSheet("border: none; padding: 0;")
        remove_button.clicked.connect(partial(self.remove_row, row))

        layout.addWidget(remove_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table.setCellWidget(row, 2, container)

    def remove_row(self, row: int):
        self.table.removeRow(row)
        for r in range(self.table.rowCount()):
            container = self.table.cellWidget(r, 2)
            button = container.layout().itemAt(0).widget()
            button.clicked.disconnect()
            button.clicked.connect(partial(self.remove_row, r))

    def serialize(self) -> list[tuple[int, str]]:
        items = []
        for row in range(self.table.rowCount()):
            qty_item = self.table.item(row, 0)
            name_item = self.table.item(row, 1)
            if qty_item and name_item:
                qty = int(qty_item.text())
                name = name_item.text().strip()
                items.append((qty, name))
        return items
