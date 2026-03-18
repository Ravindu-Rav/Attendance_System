from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QProgressBar,
    QDateEdit,
    QMessageBox,
    QSizePolicy,
    QStackedWidget,
    QFileDialog,
)
from PySide6.QtGui import QColor, QCursor
from PySide6.QtCore import Qt
import sys
import os
from datetime import datetime, timedelta
import csv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.services.dashboard_service import (
    get_dashboard_stats,
    get_trend_counts,
    get_departments_overview,
    get_admins,
    get_early_leave_requests,
    approve_early_leave,
    get_attendance_records,
)
from app.services.attendance_logic_service import (
    calculate_worked_hours,
    calculate_extra_hours,
    calculate_late_hours,
)


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance System - Dashboard")
        self.setMinimumSize(900, 600)
        self.resize(1100, 700)
        self.setWindowState(Qt.WindowMaximized)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self._build_ui()
        self._apply_styles()
        self._load_statistics()
        self._set_active_nav(self.nav_overview, 0)

    def _build_ui(self):
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 26, 20, 26)
        sidebar_layout.setSpacing(14)

        brand = QLabel("Attendance System")
        brand.setObjectName("brandTitle")
        sidebar_layout.addWidget(brand)

        self.date_label = QLabel(datetime.now().strftime("%A, %B %d, %Y"))
        self.date_label.setObjectName("dateLabel")
        sidebar_layout.addWidget(self.date_label)

        self.nav_overview = QPushButton("Overview")
        self.nav_overview.setObjectName("navButton")
        self.nav_overview.setCursor(QCursor(Qt.PointingHandCursor))
        self.nav_overview.clicked.connect(lambda: self._set_active_nav(self.nav_overview, 0))

        self.nav_attendance = QPushButton("Attendance")
        self.nav_attendance.setObjectName("navButton")
        self.nav_attendance.setCursor(QCursor(Qt.PointingHandCursor))
        self.nav_attendance.clicked.connect(lambda: self._set_active_nav(self.nav_attendance, 1))

        self.nav_trends = QPushButton("Trends")
        self.nav_trends.setObjectName("navButton")
        self.nav_trends.setCursor(QCursor(Qt.PointingHandCursor))
        self.nav_trends.clicked.connect(lambda: self._set_active_nav(self.nav_trends, 2))

        self.nav_admin = QPushButton("Admin")
        self.nav_admin.setObjectName("navButton")
        self.nav_admin.setCursor(QCursor(Qt.PointingHandCursor))
        self.nav_admin.clicked.connect(lambda: self._set_active_nav(self.nav_admin, 3))

        sidebar_layout.addWidget(self.nav_overview)
        sidebar_layout.addWidget(self.nav_attendance)
        sidebar_layout.addWidget(self.nav_trends)
        sidebar_layout.addWidget(self.nav_admin)
        sidebar_layout.addStretch()

        self.main_menu_button = QPushButton("Main Menu")
        self.main_menu_button.setObjectName("secondaryButton")
        self.main_menu_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.main_menu_button.clicked.connect(self._back_to_main)
        sidebar_layout.addWidget(self.main_menu_button)

        main_layout.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack, 1)

        self._build_overview_page()
        self._build_attendance_page()
        self._build_trends_page()
        self._build_admin_page()

        self.stack.addWidget(self.overview_page)
        self.stack.addWidget(self.attendance_page)
        self.stack.addWidget(self.trends_page)
        self.stack.addWidget(self.admin_page)

    def _build_overview_page(self):
        self.overview_page = QWidget()
        layout = QVBoxLayout(self.overview_page)
        layout.setContentsMargins(26, 24, 26, 24)
        layout.setSpacing(18)

        header = QVBoxLayout()
        title = QLabel("Dashboard Overview")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Today: present, absent, and system basics")
        subtitle.setObjectName("pageSubtitle")
        header.addWidget(title)
        header.addWidget(subtitle)
        layout.addLayout(header)

        stats_grid = QGridLayout()
        stats_grid.setHorizontalSpacing(16)
        stats_grid.setVerticalSpacing(16)

        self.total_employees_value = QLabel("0")
        stats_grid.addWidget(self._stat_card("Total Employees", self.total_employees_value, "Active in system"), 0, 0)

        self.present_today_value = QLabel("0")
        stats_grid.addWidget(self._stat_card("Present Today", self.present_today_value, "Checked in"), 0, 1)

        self.absent_today_value = QLabel("0")
        stats_grid.addWidget(self._stat_card("Absent Today", self.absent_today_value, "Not checked in"), 0, 2)

        self.attendance_rate_value = QLabel("0%")
        stats_grid.addWidget(self._stat_card("Attendance Rate", self.attendance_rate_value, "Today"), 0, 3)

        self.avg_duration_value = QLabel("0h")
        stats_grid.addWidget(self._stat_card("Avg Duration", self.avg_duration_value, "Today"), 1, 0)

        self.departments_value = QLabel("0")
        stats_grid.addWidget(self._stat_card("Departments", self.departments_value, "Active units"), 1, 1)

        self.job_titles_value = QLabel("0")
        stats_grid.addWidget(self._stat_card("Job Titles", self.job_titles_value, "Defined roles"), 1, 2)

        self.admins_value = QLabel("0")
        stats_grid.addWidget(self._stat_card("Admins", self.admins_value, "System users"), 1, 3)

        self.extra_hours_value = QLabel("0.0h")
        stats_grid.addWidget(self._stat_card("Extra Hours", self.extra_hours_value, "Today"), 2, 0)

        self.late_hours_value = QLabel("0.0h")
        stats_grid.addWidget(self._stat_card("Late Hours", self.late_hours_value, "Today"), 2, 1)

        layout.addLayout(stats_grid)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(18)

        self.department_frame = QFrame()
        self.department_frame.setObjectName("sectionCard")
        dept_layout = QVBoxLayout(self.department_frame)
        dept_layout.setContentsMargins(20, 18, 20, 18)
        dept_layout.setSpacing(10)
        dept_title = QLabel("Departments Overview")
        dept_title.setObjectName("sectionTitle")
        dept_layout.addWidget(dept_title)

        self.dept_list_container = QVBoxLayout()
        self.dept_list_container.setSpacing(6)
        dept_layout.addLayout(self.dept_list_container)

        content_layout.addWidget(self.department_frame, 2)

        self.quick_frame = QFrame()
        self.quick_frame.setObjectName("sectionCard")
        quick_layout = QVBoxLayout(self.quick_frame)
        quick_layout.setContentsMargins(20, 18, 20, 18)
        quick_layout.setSpacing(10)
        quick_title = QLabel("Quick Actions")
        quick_title.setObjectName("sectionTitle")
        quick_layout.addWidget(quick_title)

        quick_buttons = QHBoxLayout()
        self.open_attendance_button = QPushButton("Mark Attendance")
        self.open_attendance_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.open_attendance_button.setObjectName("actionButton")
        self.open_attendance_button.clicked.connect(self._open_attendance)

        self.open_employee_button = QPushButton("Manage Employees")
        self.open_employee_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.open_employee_button.setObjectName("actionButton")
        self.open_employee_button.clicked.connect(self._open_employee_management)

        quick_buttons.addWidget(self.open_attendance_button)
        quick_buttons.addWidget(self.open_employee_button)
        quick_layout.addLayout(quick_buttons)

        content_layout.addWidget(self.quick_frame, 2)

        layout.addLayout(content_layout)
        layout.addStretch()

    def _build_attendance_page(self):
        self.attendance_page = QWidget()
        layout = QVBoxLayout(self.attendance_page)
        layout.setContentsMargins(26, 24, 26, 24)
        layout.setSpacing(18)

        title = QLabel("Attendance Records")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Find by date, view all, and download reports")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        filter_frame = QFrame()
        filter_frame.setObjectName("sectionCard")
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(16, 12, 16, 12)
        filter_layout.setSpacing(10)

        self.attendance_filter_date = None
        self.filter_date_input = QDateEdit()
        self.filter_date_input.setCalendarPopup(True)
        self.filter_date_input.setObjectName("dateInput")
        self.filter_date_input.setDate(datetime.now().date())

        self.filter_by_date_button = QPushButton("Load Date")
        self.filter_by_date_button.setObjectName("secondaryButton")
        self.filter_by_date_button.clicked.connect(self._load_attendance_by_date)

        self.filter_all_button = QPushButton("Load All")
        self.filter_all_button.setObjectName("secondaryButton")
        self.filter_all_button.clicked.connect(self._load_all_attendance)

        self.export_button = QPushButton("Download Report")
        self.export_button.setObjectName("actionButton")
        self.export_button.clicked.connect(self._export_attendance_report)

        self.filter_status = QLabel("Showing: Today")
        self.filter_status.setObjectName("rowLabel")

        filter_layout.addWidget(QLabel("Date"))
        filter_layout.addWidget(self.filter_date_input)
        filter_layout.addWidget(self.filter_by_date_button)
        filter_layout.addWidget(self.filter_all_button)
        filter_layout.addStretch()
        filter_layout.addWidget(self.filter_status)
        filter_layout.addWidget(self.export_button)

        layout.addWidget(filter_frame)

        self.attendance_table = QTableWidget(0, 9)
        self.attendance_table.setHorizontalHeaderLabels([
            "Employee", "Job Title", "Date", "In Time", "Out Time", "Worked", "Late", "Extra", "Status"
        ])
        self.attendance_table.setObjectName("dataTable")
        self.attendance_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.attendance_table.horizontalHeader().setStretchLastSection(True)
        self.attendance_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.attendance_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.attendance_table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.attendance_table)

    def _build_trends_page(self):
        self.trends_page = QWidget()
        layout = QVBoxLayout(self.trends_page)
        layout.setContentsMargins(26, 24, 26, 24)
        layout.setSpacing(18)

        title = QLabel("Attendance Trends")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Last 7 days performance overview")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.trend_frame = QFrame()
        self.trend_frame.setObjectName("sectionCard")
        trend_layout = QVBoxLayout(self.trend_frame)
        trend_layout.setContentsMargins(20, 18, 20, 18)
        trend_layout.setSpacing(10)
        trend_title = QLabel("Attendance Trend (Last 7 Days)")
        trend_title.setObjectName("sectionTitle")
        trend_layout.addWidget(trend_title)

        self.trend_rows_container = QVBoxLayout()
        self.trend_rows_container.setSpacing(8)
        trend_layout.addLayout(self.trend_rows_container)
        layout.addWidget(self.trend_frame)
        layout.addStretch()

    def _build_admin_page(self):
        self.admin_page = QWidget()
        layout = QVBoxLayout(self.admin_page)
        layout.setContentsMargins(26, 24, 26, 24)
        layout.setSpacing(18)

        title = QLabel("Admin Panel")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Admin details and logout")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        admin_card = QFrame()
        admin_card.setObjectName("sectionCard")
        admin_layout = QVBoxLayout(admin_card)
        admin_layout.setContentsMargins(20, 18, 20, 18)
        admin_layout.setSpacing(10)

        self.admin_count_label = QLabel("Admins: 0")
        self.admin_count_label.setObjectName("sectionTitle")
        admin_layout.addWidget(self.admin_count_label)

        self.admin_table = QTableWidget(0, 3)
        self.admin_table.setHorizontalHeaderLabels(["Admin ID", "Username", "Created At"])
        self.admin_table.setObjectName("dataTable")
        self.admin_table.horizontalHeader().setStretchLastSection(True)
        self.admin_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.admin_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.admin_table.setSelectionMode(QTableWidget.SingleSelection)
        admin_layout.addWidget(self.admin_table)

        self.approval_frame = QFrame()
        self.approval_frame.setObjectName("sectionCard")
        approval_layout = QVBoxLayout(self.approval_frame)
        approval_layout.setContentsMargins(20, 18, 20, 18)
        approval_layout.setSpacing(10)

        approval_title = QLabel("Early Leave Approvals (Today)")
        approval_title.setObjectName("sectionTitle")
        approval_layout.addWidget(approval_title)

        self.approval_table = QTableWidget(0, 4)
        self.approval_table.setHorizontalHeaderLabels(["Employee", "In Time", "Worked", "Approved"])
        self.approval_table.setObjectName("dataTable")
        self.approval_table.horizontalHeader().setStretchLastSection(True)
        self.approval_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.approval_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.approval_table.setSelectionMode(QTableWidget.SingleSelection)
        approval_layout.addWidget(self.approval_table)

        self.approve_button = QPushButton("Approve Early Leave")
        self.approve_button.setObjectName("actionButton")
        self.approve_button.clicked.connect(self._approve_early_leave)
        approval_layout.addWidget(self.approve_button, alignment=Qt.AlignRight)

        layout.addWidget(self.approval_frame)

        self.logout_button = QPushButton("Logout")
        self.logout_button.setObjectName("logoutButton")
        self.logout_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.logout_button.clicked.connect(self._logout)
        admin_layout.addWidget(self.logout_button, alignment=Qt.AlignRight)

        layout.addWidget(admin_card)
        layout.addStretch()

    def _stat_card(self, title, value_label, subtitle):
        card = QFrame()
        card.setObjectName("statCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 16, 18, 16)
        card_layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setObjectName("statTitle")
        value_label.setObjectName("statValue")
        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("statSubtitle")

        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        card_layout.addWidget(subtitle_label)
        return card

    def _apply_styles(self):
        self.setStyleSheet("""
        QMainWindow {
            background: qlineargradient(
                spread:pad,
                x1:0, y1:0,
                x2:1, y2:1,
                stop:0 #0f2027,
                stop:1 #203a43
            );
        }

        QFrame#sidebar {
            background-color: rgba(14, 18, 22, 0.95);
            border-right: 1px solid rgba(255, 255, 255, 0.06);
            min-width: 220px;
            max-width: 240px;
        }

        QLabel#brandTitle {
            font-size: 16px;
            font-weight: 700;
            color: #f2f5f8;
        }

        QLabel#pageTitle {
            font-size: 30px;
            font-weight: 700;
            color: #f5f7fa;
        }

        QLabel#pageSubtitle {
            font-size: 13px;
            color: #aeb7bd;
        }

        QLabel#dateLabel {
            font-size: 12px;
            color: #9aa6ac;
        }

        QFrame#statCard {
            background-color: rgba(20, 24, 28, 0.9);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        QLabel#statTitle {
            font-size: 12px;
            color: #9aa6ac;
        }

        QLabel#statValue {
            font-size: 26px;
            font-weight: 700;
            color: #f4f7f9;
        }

        QLabel#statSubtitle {
            font-size: 11px;
            color: #7f8a91;
        }

        QFrame#sectionCard {
            background-color: rgba(20, 24, 28, 0.92);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        QLabel#sectionTitle {
            font-size: 14px;
            font-weight: 600;
            color: #f0f4f7;
        }

        QLabel#rowLabel {
            font-size: 12px;
            color: #c2c9ce;
        }

        QProgressBar#trendBar {
            background-color: rgba(255, 255, 255, 0.08);
            border-radius: 6px;
            height: 10px;
            text-align: center;
        }

        QProgressBar#trendBar::chunk {
            background-color: #16c2ff;
            border-radius: 6px;
        }

        QPushButton#navButton {
            background-color: transparent;
            color: #c9d1d6;
            padding: 10px 12px;
            border-radius: 10px;
            text-align: left;
            font-weight: 600;
        }

        QPushButton#navButton:hover {
            background-color: rgba(255, 255, 255, 0.08);
        }

        QPushButton#navButton[active="true"] {
            background-color: #16c2ff;
            color: #0b1216;
        }

        QTableWidget#dataTable {
            background-color: rgba(16, 20, 24, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.06);
            gridline-color: rgba(255, 255, 255, 0.06);
            color: #e8edf1;
        }

        QHeaderView::section {
            background-color: rgba(30, 34, 38, 0.9);
            color: #c9d1d6;
            padding: 6px;
            border: none;
        }

        QLineEdit#textInput, QComboBox#comboInput, QDateEdit#dateInput {
            background-color: rgba(16, 20, 24, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            color: #e8edf1;
            padding: 6px 8px;
        }

        QPushButton#actionButton {
            background-color: #16c2ff;
            color: #0b1216;
            padding: 10px 16px;
            border-radius: 10px;
            font-weight: 600;
        }

        QPushButton#actionButton:hover {
            background-color: #0fb4e6;
        }

        QPushButton#secondaryButton {
            background-color: rgba(255, 255, 255, 0.08);
            color: #e8edf1;
            padding: 10px 16px;
            border-radius: 10px;
            font-weight: 600;
        }

        QPushButton#secondaryButton:hover {
            background-color: rgba(255, 255, 255, 0.14);
        }

        QPushButton#logoutButton {
            background-color: #ff4b55;
            color: white;
            padding: 10px 16px;
            border-radius: 10px;
            font-weight: 700;
        }

        QPushButton#logoutButton:hover {
            background-color: #e13e47;
        }
        """)

    def _load_statistics(self):
        try:
            stats = get_dashboard_stats()

            self.total_employees_value.setText(str(stats["total_employees"]))
            self.present_today_value.setText(str(stats["today_attendance"]))
            self.absent_today_value.setText(str(stats["absent"]))
            self.avg_duration_value.setText(f"{stats['avg_duration']:.1f}h")
            self.departments_value.setText(str(stats["total_departments"]))
            self.job_titles_value.setText(str(stats["total_job_titles"]))
            self.admins_value.setText(str(stats["total_admins"]))
            self.attendance_rate_value.setText(f"{stats['rate']}%")
            self.extra_hours_value.setText(f"{stats['extra_hours_total']:.1f}h")
            self.late_hours_value.setText(f"{stats['late_hours_total']:.1f}h")

            self._load_trend(stats["total_employees"])
            self._load_departments()
            self._load_admins()
            self._load_early_leave_requests()
            self._load_attendance_by_date(initial=True)

        except Exception as e:
            print(f"Error loading dashboard: {e}")

    def _load_trend(self, total_employees):
        for i in reversed(range(self.trend_rows_container.count())):
            item = self.trend_rows_container.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        dates, counts = get_trend_counts()

        max_value = max(counts.values()) if counts else 0
        max_value = max(max_value, total_employees)

        for d in dates:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(10)

            label = QLabel(datetime.strptime(d, "%Y-%m-%d").strftime("%a"))
            label.setObjectName("rowLabel")
            label.setFixedWidth(30)

            bar = QProgressBar()
            bar.setObjectName("trendBar")
            bar.setMaximum(max_value if max_value else 1)
            bar.setValue(counts[d])
            bar.setFormat(f"{counts[d]} / {max_value}")

            row_layout.addWidget(label)
            row_layout.addWidget(bar)
            self.trend_rows_container.addWidget(row)

    def _load_departments(self):
        for i in reversed(range(self.dept_list_container.count())):
            item = self.dept_list_container.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        rows = get_departments_overview()
        if not rows:
            empty = QLabel("No department data available")
            empty.setObjectName("rowLabel")
            self.dept_list_container.addWidget(empty)
            return

        for name, count in rows:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(10)

            label = QLabel(name)
            label.setObjectName("rowLabel")
            count_label = QLabel(str(count))
            count_label.setObjectName("rowLabel")
            count_label.setAlignment(Qt.AlignRight)

            row_layout.addWidget(label)
            row_layout.addStretch()
            row_layout.addWidget(count_label)
            self.dept_list_container.addWidget(row)

    def _load_admins(self):
        rows = get_admins()
        self.admin_table.setRowCount(0)
        for row_index, (admin_id, username, created_at) in enumerate(rows):
            self.admin_table.insertRow(row_index)
            self.admin_table.setItem(row_index, 0, QTableWidgetItem(str(admin_id)))
            self.admin_table.setItem(row_index, 1, QTableWidgetItem(username))
            self.admin_table.setItem(row_index, 2, QTableWidgetItem(created_at))
        self.admin_count_label.setText(f"Admins: {len(rows)}")

    def _load_early_leave_requests(self):
        rows = get_early_leave_requests()
        self.approval_table.setRowCount(0)
        for row_index, (duty_id, full_name, in_time, approved) in enumerate(rows):
            worked_hours = self._format_hours(calculate_worked_hours(in_time, datetime.now().strftime("%H:%M:%S")))
            approved_text = "Yes" if approved else "No"
            self.approval_table.insertRow(row_index)
            self.approval_table.setItem(row_index, 0, QTableWidgetItem(full_name))
            self.approval_table.setItem(row_index, 1, QTableWidgetItem(in_time or "-"))
            self.approval_table.setItem(row_index, 2, QTableWidgetItem(worked_hours))
            self.approval_table.setItem(row_index, 3, QTableWidgetItem(approved_text))
            self.approval_table.setVerticalHeaderItem(row_index, QTableWidgetItem(str(duty_id)))

    def _load_attendance_by_date(self, initial=False):
        date_str = self.filter_date_input.date().toString("yyyy-MM-dd")
        self.attendance_filter_date = date_str
        self._load_attendance_rows(date_str)
        if initial:
            self.filter_status.setText("Showing: Today")
        else:
            self.filter_status.setText(f"Showing: {date_str}")

    def _load_all_attendance(self):
        self.attendance_filter_date = None
        self._load_attendance_rows(None)
        self.filter_status.setText("Showing: All")

    def _load_attendance_rows(self, date_str):
        try:
            rows = get_attendance_records(date_str)
            self.attendance_table.setRowCount(0)
            for row_index, (full_name, job_title, date_value, in_time, out_time, duration, status) in enumerate(rows):
                worked_hours = self._calc_duration_hours(duration, in_time, out_time)
                worked_text = self._format_hours(worked_hours)
                late_text = self._format_hours(calculate_late_hours(in_time))
                extra_text = self._format_hours(calculate_extra_hours(out_time))
                status_text = status or ("OUT" if out_time else "IN")
                self.attendance_table.insertRow(row_index)
                self.attendance_table.setItem(row_index, 0, QTableWidgetItem(full_name))
                self.attendance_table.setItem(row_index, 1, QTableWidgetItem(job_title))
                self.attendance_table.setItem(row_index, 2, QTableWidgetItem(date_value))
                self.attendance_table.setItem(row_index, 3, QTableWidgetItem(in_time or "-"))
                self.attendance_table.setItem(row_index, 4, QTableWidgetItem(out_time or "-"))
                self.attendance_table.setItem(row_index, 5, QTableWidgetItem(worked_text))
                self.attendance_table.setItem(row_index, 6, QTableWidgetItem(late_text))
                self.attendance_table.setItem(row_index, 7, QTableWidgetItem(extra_text))
                self.attendance_table.setItem(row_index, 8, QTableWidgetItem(status_text))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load attendance: {str(e)}")

    def _export_attendance_report(self):
        date_label = self.attendance_filter_date or "all"
        filename = f"attendance_{date_label}.csv"
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Attendance Report",
            filename,
            "CSV Files (*.csv)"
        )
        if not path:
            return

        try:
            rows = get_attendance_records(self.attendance_filter_date)
            with open(path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Employee", "Job Title", "Date", "In Time", "Out Time", "Worked", "Late", "Extra", "Status"])
                for full_name, job_title, date_value, in_time, out_time, duration, status in rows:
                    worked_hours = self._calc_duration_hours(duration, in_time, out_time)
                    worked_text = self._format_hours(worked_hours)
                    late_text = self._format_hours(calculate_late_hours(in_time))
                    extra_text = self._format_hours(calculate_extra_hours(out_time))
                    status_text = status or ("OUT" if out_time else "IN")
                    writer.writerow([full_name, job_title, date_value, in_time or "", out_time or "", worked_text, late_text, extra_text, status_text])

            QMessageBox.information(self, "Report Saved", f"Report saved to {path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export report: {str(e)}")

    def _set_active_nav(self, button, index):
        for nav_button in (self.nav_overview, self.nav_attendance, self.nav_trends, self.nav_admin):
            nav_button.setProperty("active", nav_button is button)
            nav_button.style().unpolish(nav_button)
            nav_button.style().polish(nav_button)
        self.stack.setCurrentIndex(index)

    def _approve_early_leave(self):
        current_row = self.approval_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Select Employee", "Please select a row to approve.")
            return

        duty_id_item = self.approval_table.verticalHeaderItem(current_row)
        if not duty_id_item:
            QMessageBox.warning(self, "Error", "Could not determine attendance record.")
            return

        duty_id = duty_id_item.text()
        try:
            approve_early_leave(duty_id)
            self._load_statistics()
            QMessageBox.information(self, "Approved", "Early leave approved.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to approve: {str(e)}")

    def _calc_duration_hours(self, duration, in_time, out_time):
        if duration:
            try:
                return float(duration)
            except Exception:
                return 0.0
        return calculate_worked_hours(in_time, out_time)

    def _format_hours(self, hours):
        try:
            return f"{float(hours):.1f}h"
        except Exception:
            return "0.0h"

    def _open_attendance(self):
        from .attendance_window import AttendanceWindow
        self.attendance_window = AttendanceWindow()
        self.attendance_window.showMaximized()
        self.close()

    def _open_employee_management(self):
        from .employee_window import EmployeeWindow
        self.employee_window = EmployeeWindow()
        self.employee_window.showMaximized()
        self.close()

    def _back_to_main(self):
        from .main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.showMaximized()
        self.close()

    def _logout(self):
        from .login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.showMaximized()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())
