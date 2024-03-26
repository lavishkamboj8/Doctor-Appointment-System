from PyQt6.QtWidgets import *
from PyQt6.uic import loadUiType
import sys
import sqlite3
from datetime import date


ui, _ = loadUiType('appointment.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)

        try:
            con = sqlite3.connect("appointment-booking.db")
            con.execute(
                "CREATE TABLE IF NOT EXISTS appointments(appointmentid INTEGER, patientname TEXT, city TEXT, phone TEXT, appointmenttime TEXT, status TEXT, appointmentdate TEXT)")
            con.commit()
            print("Table creaed")
        except:
            print(con.Error)

        self.create_appointmentid()
        self.fill_appointmentid()
        self.dateEdit.setDate(date.today())

        self.LOGINBUTTON.clicked.connect(self.login)

        self.BookAppointmentIcon1.clicked.connect(self.show_book_appointment)
        self.BookAppointmentIcon2.clicked.connect(self.show_book_appointment)
        self.BookAppointmentIcon3.clicked.connect(self.show_book_appointment)

        self.ConsultDoctorIcon1.clicked.connect(self.show_consult_doctor)
        self.ConsultDoctorIcon2.clicked.connect(self.show_consult_doctor)
        self.ConsultDoctorIcon3.clicked.connect(self.show_consult_doctor)

        self.ReportsIcon1.clicked.connect(self.show_reports_form)
        self.ReportsIcon2.clicked.connect(self.show_reports_form)
        self.ReportsIcon3.clicked.connect(self.show_reports_form)

        self.LogoutIcon1.clicked.connect(self.logout)
        self.LogoutIcon2.clicked.connect(self.logout)
        self.LogoutIcon3.clicked.connect(self.logout)

        self.BOOKAPPOINTMENT.clicked.connect(self.book_appointment)
        self.SelectAppointmentId.currentIndexChanged.connect(self.fill_details_appointment_id_selected)
        self.EditAppointment.clicked.connect(self.edit_appointment)
        self.DeleteAppointment.clicked.connect(self.delete_appointment)

        self.dateEdit.dateChanged.connect(self.show_date_wise_reports)

        print("GOOD")

        self.tabWidget.setStyleSheet("QTabWidget::pane { border: 0; }")

    #### ADMIN LOGIN CODE ####

    def login(self):
        pw = self.PASSWORD.text()
        if (pw == "admin"):
            self.PASSWORD.setText("")
            self.LOGININFO.setText("")
            self.tabWidget.setCurrentIndex(1)
        else:
            self.LOGININFO.setText("Invalid login details")

    #### LOG OUT CODE ####

    def logout(self):
        self.tabWidget.setCurrentIndex(0)

        ### SHOW BOOK APPOINTMENT FORM ####

    def show_book_appointment(self):
        self.tabWidget.setCurrentIndex(1)

    ### SHOW CONSULT DOCTOR FORM ####

    def show_consult_doctor(self):
        self.fill_appointmentid()
        self.tabWidget.setCurrentIndex(2)

    ### SHOW REPORTS FORM ####

    def show_reports_form(self):
        self.tabWidget.setCurrentIndex(3)

        self.Reports.setRowCount(0)
        self.Reports.clear()

        con = sqlite3.connect("appointment-booking.db")
        cursor = con.execute("SELECT * FROM appointments")
        result = cursor.fetchall()
        r = 0
        c = 0
        for row_number, row_data in enumerate(result):
            r += 1
            c = 0
            for column_number, data in enumerate(row_data):
                c += 1
        self.Reports.setColumnCount(c)
        for row_number, row_data in enumerate(result):
            self.Reports.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Reports.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.Reports.setHorizontalHeaderLabels(['Id', 'Name', 'City', 'Phone', 'Time', 'Status', 'Date'])
        self.Reports.setColumnWidth(0, 10)
        self.Reports.setColumnWidth(1, 70)
        self.Reports.setColumnWidth(2, 70)
        self.Reports.setColumnWidth(3, 70)
        self.Reports.setColumnWidth(4, 30)
        self.Reports.setColumnWidth(5, 50)
        self.Reports.verticalHeader().setVisible(False)
        # self.Reports.horizontalHeader().setVisible(False)

    def show_date_wise_reports(self):

        self.Reports.setRowCount(0)
        self.Reports.clear()
        self.Reports.setColumnWidth(0, 10)
        self.Reports.setColumnWidth(1, 70)
        self.Reports.setColumnWidth(2, 70)
        self.Reports.setColumnWidth(3, 70)
        self.Reports.setColumnWidth(4, 30)
        self.Reports.setColumnWidth(5, 50)
        self.Reports.verticalHeader().setVisible(False)
        # self.Reports.horizontalHeader().setVisible(False)
        con = sqlite3.connect("appointment-booking.db")
        print("SELECT * FROM appointments where appointmentdate = '" + str(self.dateEdit.date()) + "'")
        cursor = con.execute(
            "SELECT * FROM appointments where appointmentdate = '" + str((self.dateEdit.date()).toPyDate()) + "'")
        result = cursor.fetchall()
        r = 0
        c = 0
        for row_number, row_data in enumerate(result):
            r += 1
            c = 0
            for column_number, data in enumerate(row_data):
                c += 1
        self.Reports.setColumnCount(c)
        for row_number, row_data in enumerate(result):
            self.Reports.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Reports.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.Reports.setHorizontalHeaderLabels(['Id', 'Name', 'City', 'Phone', 'Time', 'Status', 'Date'])

    #### CREATE APPOINTMENT ID ####

    def create_appointmentid(self):
        appointmentid = 0
        try:
            print("Starting")
            connection = sqlite3.connect("appointment-booking.db")
            cursor = connection.execute("SELECT MAX(appointmentid) FROM appointments")
            result = cursor.fetchall()
            if result:
                for maxid in result:
                    appointmentid = int(maxid[0]) + 1
        except:
            appointmentid = 1
        print(appointmentid)
        self.AppointmentIdLabel.setText(str(appointmentid))

    #### BOOK APPOINTMENT ####

    def book_appointment(self):
        self.create_appointmentid()
        try:
            con = sqlite3.connect("appointment-booking.db")
            con.execute("INSERT INTO appointments VALUES(" + str(self.AppointmentIdLabel.text()) + " ,'" + str(
                self.PatientName.text()) + "','" + str(self.PatientCity.text()) + "','" + str(
                self.PatientPhone.text()) + "','" + str(self.PatientAppointmentTime.text()) + "','Booked','" + str(
                date.today()) + "')")
            con.commit()
        except:
            print("Error in insert", con.Error)
        self.AppointmentIdLabel.setText("")
        self.PatientName.setText("")
        self.PatientCity.setText("")
        self.PatientPhone.setText("")
        self.PatientAppointmentTime.setText("")
        self.create_appointmentid()
        print("Saved successfully")
        self.BOOKINFO.setText("Appointment Booked Successfully")

        #### FILL APPOINTMENT IDS IN COMBO BOX ####

    def fill_appointmentid(self):
        con = sqlite3.connect("appointment-booking.db")
        cursor = con.execute("SELECT * FROM appointments")
        print("selecting")
        result = cursor.fetchall()
        if result:
            self.SelectAppointmentId.clear()
            print("clearing")
            for appointments in result:
                self.SelectAppointmentId.addItem(str(appointments[0]))
                print("filling" + str(appointments[0]))

    ### FILL DETAILS APPOINTMENT ID SELECTED ####

    def fill_details_appointment_id_selected(self):
        try:
            con = sqlite3.connect("appointment-booking.db")
            cursor = con.execute(
                "SELECT * FROM appointments where appointmentid = " + str(self.SelectAppointmentId.currentText()) + "")
            result = cursor.fetchall()
            if result:
                for appointments in result:
                    print(appointments)
                    self.EditPatientName.setText(str(appointments[1]))
                    self.EditPatientCity.setText(str(appointments[2]))
                    self.EditPatientPhone.setText(str(appointments[3]))
                    self.EditPatientAppointmentTime.setText(str(appointments[4]))
                    if (str(appointments[5]) == "booked"):
                        self.SelectAppointmentStatus.setCurrentIndex(3)
                    elif (str(appointments[5]) == "Cancelled"):
                        self.SelectAppointmentStatus.setCurrentIndex(1)
                    elif (str(appointments[5]) == "Completed"):
                        self.SelectAppointmentStatus.setCurrentIndex(2)
                    elif (str(appointments[5]) == "Not Attended"):
                        self.SelectAppointmentStatus.setCurrentIndex(3)
        except:
            print(con.Error)

    ### EDIT APPOINTMENT DETAILS ####


    def edit_appointment(self):
        try:
            con = sqlite3.connect("appointment-booking.db")
            con.execute(
                "UPDATE appointments set patientname = '" + str(self.EditPatientName.text()) + "', city='" + str(
                    self.EditPatientCity.text()) + "', phone='" + str(
                    self.EditPatientPhone.text()) + "',appointmenttime='" + str(
                    self.EditPatientAppointmentTime.text()) + "',status='" + str(
                    self.SelectAppointmentStatus.currentText()) + "' where appointmentid = " + str(
                    self.SelectAppointmentId.currentText()) + "")
            con.commit()
            self.EDITINFO.setText("Appointment Updated Successfully")
        except:
            print(con.Error)

    ### DELETE APPOINTMENT DETAILS ####

    def delete_appointment(self):
        try:
            con = sqlite3.connect("appointment-booking.db")
            con.execute(
                "DELETE FROM appointments where appointmentid = " + str(self.SelectAppointmentId.currentText()) + "")
            con.commit()
            self.fill_appointmentid()
            self.EDITINFO.setText("Appointment Deleted Successfully")
        except:
            print(con.Error)


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()