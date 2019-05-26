"Application Style Sheet"
STYLESHEETTEMPLATE = """
QComboBox {
    background-color: @main2;
    color: @text;
    border-style: outset;
    border-width: 1px;
    border-color: @main2;
    font: bold 14px;
    min-width: 10em;
    padding: 6px;
}
QComboBox::drop-down{
    border-style: none;
    border-width: 0px;
    border-color: @main2;
    color: @main2;
    padding: 0px;
}
QComboBox::item{
    background-color: @main2;
    color: @text;
}
QComboBox::item::selected{
    background-color: @main2;
}
QComboBox > QMenu {
    background-color: @main2;
}


QDialog {
    background-color: @main1;
    padding : 0px;
    margin : 0px;
}


QFileDialog {
    background-color: @main2;
    padding : 0px;
    margin : 0px;
}


QLineEdit {
    background-color: @main1;
    border-style: none;
    border-width: 1px;
    border-color: @main1;
    color: @text;
}


QMenuBar {
    background-color: @menu_bar;
    color: @text;
}
QMenuBar::item:selected {
    background: @title_bar;
}

QLabel{
    color: @text;
}

QRadioButton {
    color: @text;
}
QRadioButton::indicator {
    color: black;
}


QMenu {
    background: @menu_bar;
    color: @text;
}
QMenu::item:selected {
    background: @title_bar;
}

QStatusBar {
    background-color: @progress_bar;
    color: @text;
}


QMainWindow {
    background-color: @main1;
}

QProgressBar {
    background-color: @progress_bar;
}
QProgressBar::chunk {
    background-color: @title_bar;
    width: 10px;
}


QTabWidget::pane {
    background-color: @main1;
    border-style: none;
    border-width: 1px;
    border-color: @main1;
    color: @text;
}


QTabBar::tab {
    background: @main1;
    border-color: @main1;
    color: @text;
    border-style: none;
    border-width: 1px;
    min-width: 8ex;
    padding: 5px;
}
QTabBar::close-button {
    image: none
}
QTabBar::close-button:hover {
    image: url(@close_icon)
}
QTabBar::tab:hover {
    border-color: @main2;
    background: @main2;
}
QTabBar::tab:selected {
    border-color: @main2;
    background: @main2;
}


QPlainTextEdit {
    background-color: @main1;
    border-style: none;
    color: @text;
}
QPlainTextEdit#brd {
    background-color: @main1;
    border-style: solid;
    border-width: 2px;
    border-color: @main1;
    border-right-color: @main2;
    color: @text;
}
QPlainTextEdit#dmi_edit {
    background-color: @main2;
    border-style: outset;
    border-width: 1px;
    border-color: @main2;
    color: @text;
}


QScrollBar:vertical {
    width: 13px;
    background: @main1;
}
QScrollBar::handle:vertical {
    min-height: 5px;
}
QScrollBar::add-line:vertical {
    background: none;
    height: 45px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
} 
QScrollBar::up-arrow:vertical { 
    height: 3px; 
    width: 3px 
}
QScrollBar::down-arrow:vertical {
    height: 3px; 
    width: 3px 
}

QScrollBar:horizontal {
    height: 13px;
    background: @main1;
}
QScrollBar::handle:horizontal {
    min-width: 5px;
}
QScrollBar::add-line:horizontal {
    background: none;
    width: 45px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
} 
QScrollBar::right-arrow:horizontal { 
    height: 3px; 
    width: 3px 
}
QScrollBar::left-arrow:horizontal {
    height: 3px; 
    width: 3px 
}


QPushButton {
    background-color: @main1;
    color: @text;
    border-style: none;
    border-width: 1px;
    border-color: @main1;
    font: bold 14px;
    padding: 6px;
}
QPushButton:pressed {
    background-color: @main1;
    border-style: inset;
}


QToolButton#title_button {
    background-color: @title_bar;
    border-width: 0px;
}
QToolButton#exit {
    background-color: @title_bar;
    border-width: 0px;
}
QToolButton#logo {
    background-color: @title_bar;
    border-width: 0px;
}
QToolButton#tab_button {
    background-color: @main2;
    color: @text;
    border-style: none;
    border-width: 1px;
    border-color: @main1;
    font: bold 14px;
    padding: 6px;
}
QToolButton#tab_button:pressed {
    background-color: @main2;
    border-style: inset;
}
QToolButton#exit:hover  {
    background-color: red;
    border: 0px;
}
QToolButton {
    border-width: 0px;
    background-color: @main2;
}

QToolBar#tool_bar {
    border-width: 0px;
    background-color: @main2;
}
QToolBar#title_bar {
    background-color: @title_bar;
    color: @text;
    border-style: none;
    border-radius: 0px;
    border: 0px;
}


QTextEdit {
    background-color: @main1;
    border-style: none;
    border-width: 1px;
    border-color: @main1;
    color: @text;
}


QTreeWidget {
    background-color: @main1;
    border-style: none;
    border-width: 1px;
    border-color: @main1;
    color: @text;
    selection-background-color: @highlight;
}


QHeaderView::section {
    background-color: @main1;
    color: @text;
    padding-left: 4px;
    border: none;
}
"""