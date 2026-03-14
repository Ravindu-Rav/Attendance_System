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
    QGraphicsDropShadowEffect,
    QTableWidget,
    QTableWidgetItem,
    QProgressBar,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QFormLayout,
    QMessageBox,
    QSizePolicy,
)
from PySide6.QtGui import QColor, QCursor
from PySide6.QtCore import Qt
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.database.db import get_connection


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

    def _build_ui(self):
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(18)

        header_layout = QHBoxLayout()
        title_layout = QVBoxLayout()

        self.title = QLabel("Dashboard")
        self.title.setObjectName("pageTitle")
        self.subtitle = QLabel("Attendance overview and operational insights")
        self.subtitle.setObjectName("pageSubtitle")

        title_layout.addWidget(self.title)
        title_layout.addWidget(self.subtitle)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        right_header = QVBoxLayout()
        self.date_label = QLabel(datetime.now().strftime("%A, %B %d, %Y"))
        self.date_label.setObjectName("dateLabel")
        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setObjectName("backButton")
        self.back_button.clicked.connect(self._back_to_main)
        right_header.addWidget(self.date_label, alignment=Qt.AlignRight)
        right_header.addWidget(self.back_button, alignment=Qt.AlignRight)
        header_layout.addLayout(right_header)

        main_layout.addLayout(header_layout)

        stats_grid = QGridLayout()
        stats_grid.setHorizontalSpacing(16)
        stats_grid.setVerticalSpacing(16)

        self.total_employees_value = QLabel("0")
        stats_grid.addWidget(self._stat_card("Total Employees", self.total_employees_value, "Active in system"), 0, 0)

        self.present_today_value = QLabel("0")
        stats_grid.addWidget(self._stat_card("Present Today", self.present_today_value, "Checked in"), 0, 1)

        self.absent_today_value = QLabel("0")
        stats_grid.addWidget(self._stat_card("Absent Today", self.absent_today_value, "Not checked in"), 0, 2)

        self.avg_duration_value = QLabel("0h")
        stats_grid.addWidget(self._stat_card("Avg Duration", self.avg_duration_value, "Today"), 0, 3)

        self.departments_value = QLabel("0")
        stats_grid.addWidget(self._stat_card("Departments", self.departments_value, "Active units"), 1, 0)

        self.job_titles_value = QLabel("0")
        stats_grid.addWidget(self._stat_card("Job Titles", self.job_titles_value, "Defined roles"), 1, 1)

        self.admins_value = QLabel("0")
        stats_grid.addWidget(self._stat_card("Admins", self.admins_value, "System users"), 1, 2)

        self.attendance_rate_value = QLabel("0%")
        stats_grid.addWidget(self._stat_card("Attendance Rate", self.attendance_rate_value, "Today"), 1, 3)

        main_layout.addLayout(stats_grid)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(18)

        left_col = QVBoxLayout()
        left_col.setSpacing(18)

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

        left_col.addWidget(self.trend_frame)

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

        left_col.addWidget(self.department_frame)
        left_col.addStretch()

        right_col = QVBoxLayout()
        right_col.setSpacing(18)

        self.data_entry_frame = QFrame()
        self.data_entry_frame.setObjectName("sectionCard")
        entry_layout = QVBoxLayout(self.data_entry_frame)
        entry_layout.setContentsMargins(20, 18, 20, 18)
        entry_layout.setSpacing(12)
        entry_title = QLabel("Data Entry")
        entry_title.setObjectName("sectionTitle")
        entry_layout.addWidget(entry_title)

        entry_form = QFormLayout()
        entry_form.setLabelAlignment(Qt.AlignLeft)
        entry_form.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        entry_form.setHorizontalSpacing(12)
        entry_form.setVerticalSpacing(8)

        self.department_input = QLineEdit()
        self.department_input.setObjectName("textInput")
        self.department_input.setPlaceholderText("e.g., Operations")

        self.department_add_button = QPushButton("Add Department")
        self.department_add_button.setObjectName("secondaryButton")
        self.department_add_button.clicked.connect(self._handle_add_department)

        dept_row = QHBoxLayout()
        dept_row.addWidget(self.department_input)
        dept_row.addWidget(self.department_add_button)
        entry_form.addRow(QLabel("Department"), dept_row)

        self.job_title_input = QLineEdit()
        self.job_title_input.setObjectName("textInput")
        self.job_title_input.setPlaceholderText("e.g., Site Supervisor")

        self.job_department_combo = QComboBox()
        self.job_department_combo.setObjectName("comboInput")

        self.job_employee_combo = QComboBox()
        self.job_employee_combo.setObjectName("comboInput")

        self.job_add_button = QPushButton("Add Job Title")
        self.job_add_button.setObjectName("secondaryButton")
        self.job_add_button.clicked.connect(self._handle_add_job_title)

        job_row = QHBoxLayout()
        job_row.addWidget(self.job_title_input)
        job_row.addWidget(self.job_add_button)

        entry_form.addRow(QLabel("Job Title"), job_row)
        entry_form.addRow(QLabel("Department"), self.job_department_combo)
        entry_form.addRow(QLabel("Assign To"), self.job_employee_combo)

        self.att_employee_combo = QComboBox()
        self.att_employee_combo.setObjectName("comboInput")

        self.att_job_combo = QComboBox()
        self.att_job_combo.setObjectName("comboInput")

        self.att_duration_input = QLineEdit()
        self.att_duration_input.setObjectName("textInput")
        self.att_duration_input.setPlaceholderText("Hours (e.g., 8)")

        self.att_date_input = QDateEdit()
        self.att_date_input.setCalendarPopup(True)
        self.att_date_input.setObjectName("dateInput")
        self.att_date_input.setDate(datetime.now().date())

        self.att_add_button = QPushButton("Add Attendance")
        self.att_add_button.setObjectName("actionButton")
        self.att_add_button.clicked.connect(self._handle_add_attendance)

        att_row = QHBoxLayout()
        att_row.addWidget(self.att_duration_input)
        att_row.addWidget(self.att_add_button)

        entry_form.addRow(QLabel("Employee"), self.att_employee_combo)
        entry_form.addRow(QLabel("Job Title"), self.att_job_combo)
        entry_form.addRow(QLabel("Date"), self.att_date_input)
        entry_form.addRow(QLabel("Duration"), att_row)

        entry_layout.addLayout(entry_form)
        right_col.addWidget(self.data_entry_frame)

        self.recent_frame = QFrame()
        self.recent_frame.setObjectName("sectionCard")
        recent_layout = QVBoxLayout(self.recent_frame)
        recent_layout.setContentsMargins(20, 18, 20, 18)
        recent_layout.setSpacing(10)
        recent_title = QLabel("Recent Attendance")
        recent_title.setObjectName("sectionTitle")
        recent_layout.addWidget(recent_title)

        self.recent_table = QTableWidget(0, 4)
        self.recent_table.setHorizontalHeaderLabels(["Employee", "Job Title", "Date", "Duration"])
        self.recent_table.setObjectName("dataTable")
        self.recent_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.recent_table.horizontalHeader().setStretchLastSection(True)
        self.recent_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.recent_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.recent_table.setSelectionMode(QTableWidget.SingleSelection)
        recent_layout.addWidget(self.recent_table)

        right_col.addWidget(self.recent_frame)

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

        self.back_main_button = QPushButton("Main Menu")
        self.back_main_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_main_button.setObjectName("secondaryButton")
        self.back_main_button.clicked.connect(self._back_to_main)

        quick_buttons.addWidget(self.open_attendance_button)
        quick_buttons.addWidget(self.open_employee_button)
        quick_buttons.addWidget(self.back_main_button)
        quick_layout.addLayout(quick_buttons)

        right_col.addWidget(self.quick_frame)

        content_layout.addLayout(left_col, 2)
        content_layout.addLayout(right_col, 3)

        main_layout.addLayout(content_layout)

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

        QPushButton#backButton {
            background-color: rgba(255, 255, 255, 0.08);
            color: #e8edf1;
            padding: 8px 14px;
            border-radius: 10px;
            font-weight: 600;
        }

        QPushButton#backButton:hover {
            background-color: rgba(255, 255, 255, 0.14);
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
        """)

    def _load_statistics(self):
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("SELECT COUNT(*) FROM Employee")
            total_employees = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM Department")
            total_departments = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM Job_Title")
            total_job_titles = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM Admin")
            total_admins = cur.fetchone()[0]

            today = datetime.now().strftime("%Y-%m-%d")
            cur.execute("SELECT COUNT(*), COALESCE(AVG(duration), 0) FROM On_Duty WHERE date = ?", (today,))
            row = cur.fetchone()
            today_attendance = row[0]
            avg_duration = row[1] or 0

            absent = max(total_employees - today_attendance, 0)
            rate = 0
            if total_employees:
                rate = int((today_attendance / total_employees) * 100)

            self.total_employees_value.setText(str(total_employees))
            self.present_today_value.setText(str(today_attendance))
            self.absent_today_value.setText(str(absent))
            self.avg_duration_value.setText(f"{avg_duration:.1f}h")
            self.departments_value.setText(str(total_departments))
            self.job_titles_value.setText(str(total_job_titles))
            self.admins_value.setText(str(total_admins))
            self.attendance_rate_value.setText(f"{rate}%")

            self._load_trend(cur, total_employees)
            self._load_departments(cur)
            self._load_recent_activity(cur)
            self._refresh_picklists(cur)

            conn.close()

        except Exception as e:
            print(f"Error loading dashboard: {e}")

    def _load_trend(self, cur, total_employees):
        for i in reversed(range(self.trend_rows_container.count())):
            item = self.trend_rows_container.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        start_date = datetime.now().date() - timedelta(days=6)
        dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
        counts = {d: 0 for d in dates}

        cur.execute(
            "SELECT date, COUNT(*) FROM On_Duty WHERE date BETWEEN ? AND ? GROUP BY date",
            (dates[0], dates[-1])
        )
        for date_str, count in cur.fetchall():
            if date_str in counts:
                counts[date_str] = count

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

    def _load_departments(self, cur):
        for i in reversed(range(self.dept_list_container.count())):
            item = self.dept_list_container.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        cur.execute(
            """
            SELECT d.department_name, COUNT(j.employee_ID) AS emp_count
            FROM Department d
            LEFT JOIN Job_Title j ON j.dept_ID = d.dept_ID
            GROUP BY d.dept_ID
            ORDER BY emp_count DESC, d.department_name ASC
            LIMIT 6
            """
        )
        rows = cur.fetchall()
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

    def _load_recent_activity(self, cur):
        cur.execute(
            """
            SELECT e.fname || ' ' || e.lname AS full_name,
                   COALESCE(j.job_title, 'N/A') AS job_title,
                   o.date,
                   COALESCE(o.duration, 0)
            FROM On_Duty o
            LEFT JOIN Employee e ON o.employee_ID = e.employee_ID
            LEFT JOIN Job_Title j ON o.job_ID = j.job_ID
            ORDER BY o.date DESC, o.duty_ID DESC
            LIMIT 12
            """
        )
        rows = cur.fetchall()
        self.recent_table.setRowCount(0)
        for row_index, (full_name, job_title, date_str, duration) in enumerate(rows):
            self.recent_table.insertRow(row_index)
            self.recent_table.setItem(row_index, 0, QTableWidgetItem(full_name))
            self.recent_table.setItem(row_index, 1, QTableWidgetItem(job_title))
            self.recent_table.setItem(row_index, 2, QTableWidgetItem(date_str))
            self.recent_table.setItem(row_index, 3, QTableWidgetItem(f"{duration}h"))

    def _refresh_picklists(self, cur):
        self.job_department_combo.clear()
        self.job_department_combo.addItem("Select department", None)
        cur.execute("SELECT dept_ID, department_name FROM Department ORDER BY department_name")
        for dept_id, name in cur.fetchall():
            self.job_department_combo.addItem(name, dept_id)

        self.job_employee_combo.clear()
        self.job_employee_combo.addItem("Optional", None)
        cur.execute("SELECT employee_ID, fname, lname FROM Employee ORDER BY fname, lname")
        for emp_id, fname, lname in cur.fetchall():
            self.job_employee_combo.addItem(f"{fname} {lname}", emp_id)

        self.att_employee_combo.clear()
        self.att_employee_combo.addItem("Select employee", None)
        cur.execute("SELECT employee_ID, fname, lname FROM Employee ORDER BY fname, lname")
        for emp_id, fname, lname in cur.fetchall():
            self.att_employee_combo.addItem(f"{fname} {lname}", emp_id)

        self.att_job_combo.clear()
        self.att_job_combo.addItem("Select job title", None)
        cur.execute("SELECT job_ID, job_title FROM Job_Title ORDER BY job_title")
        for job_id, title in cur.fetchall():
            self.att_job_combo.addItem(title, job_id)

    def _handle_add_department(self):
        name = self.department_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation", "Department name is required.")
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO Department (department_name) VALUES (?)", (name,))
            conn.commit()
            self.department_input.clear()
            self._load_statistics()
            QMessageBox.information(self, "Success", "Department added.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def _handle_add_job_title(self):
        title = self.job_title_input.text().strip()
        dept_id = self.job_department_combo.currentData()
        emp_id = self.job_employee_combo.currentData()
        if not title:
            QMessageBox.warning(self, "Validation", "Job title is required.")
            return
        if dept_id is None:
            QMessageBox.warning(self, "Validation", "Please select a department.")
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Job_Title (job_title, dept_ID, employee_ID) VALUES (?, ?, ?)",
                (title, dept_id, emp_id),
            )
            conn.commit()
            self.job_title_input.clear()
            self._load_statistics()
            QMessageBox.information(self, "Success", "Job title added.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def _handle_add_attendance(self):
        emp_id = self.att_employee_combo.currentData()
        job_id = self.att_job_combo.currentData()
        duration_text = self.att_duration_input.text().strip()
        date_str = self.att_date_input.date().toString("yyyy-MM-dd")

        if emp_id is None or job_id is None:
            QMessageBox.warning(self, "Validation", "Select an employee and job title.")
            return
        try:
            duration = int(duration_text)
            if duration < 0:
                raise ValueError
        except Exception:
            QMessageBox.warning(self, "Validation", "Duration must be a positive number.")
            return

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO On_Duty (employee_ID, job_ID, duration, date) VALUES (?, ?, ?, ?)",
                (emp_id, job_id, duration, date_str),
            )
            conn.commit()
            self.att_duration_input.clear()
            self._load_statistics()
            QMessageBox.information(self, "Success", "Attendance record added.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            try:
                conn.close()
            except Exception:
                pass

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())
