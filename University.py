import sqlite3


class University:

    def __init__(self, name, country):
        self.name = name.strip()
        self.country = country
        self.status = True
        self.connectdatabase()

    def run(self):
        self.menu()
        choice = self.choice(5)
        if choice == 1:
            self.addStudent()
        elif choice == 2:
            self.deleteStudent()
        elif choice == 3:
            self.updateStudent()
        elif choice == 4:
            print("1-)All Students\n2-)Department\n3-)Faculty\n4-)Type\n5-)Status\n")
            choice = self.choice(5)
            self.showAllStudents(choice)
        else:
            self.connect.close()
            self.status = False

    def connectdatabase(self):
        self.connect = sqlite3.connect(f"{self.name}.db")
        self.cursor = self.connect.cursor()

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS students"
            "(name TEXT, surname TEXT, department TEXT, faculty TEXT, typ TEXT, stid TEXT, status TEXT)")
        self.connect.commit()

    def menu(self):
        print(
            f"\n***** {self.name} Administration System ({self.country}) *****\n"
            f"\n1-)Add Student\n2-)Delete Student\n3-)Update Student\n4-)Show All Students\n5-)Exit\n")

    def choice(self, to):
        while True:
            try:
                choice = int(input("Select: "))
                print("")
                if (to + 1) > choice > 0:
                    return choice
                else:
                    print(f"Value must be between 1-{to} !")
            except ValueError:
                print("Value must be integer!")

    def addStudent(self):
        name = input("Student's name: ").strip().lower().capitalize()
        surname = input("Student's surname: ").upper()
        department = input("Student's department: ").strip()
        faculty = input("Student's faculty: ").strip()
        typ = input("Student's type(1/2): ")
        stid = input("Student's ID: ")
        status = input("Student's status(Active/Passive/Graduated): ").strip().lower().capitalize()
        self.cursor.execute(
            "INSERT INTO students VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(name, surname, department,
                                                                                           faculty, typ, stid, status))
        self.connect.commit()
        print("Registration Successful")

    def deleteStudent(self):
        all = self.showAllStudents(1)  # Bütün öğrencileri çektik
        choice = self.choice(len(all))
        stid = all[choice - 1][5]
        self.cursor.execute(f"DELETE FROM students WHERE stid = '{stid}'")
        self.connect.commit()
        print(f"Student succesfully removed: {stid}")

    def updateStudent(self):
        value = ["name", "surname", "department", "faculty", "typ", "stid", "status"]
        all = self.showAllStudents(1)  # Bütün öğrencileri çektik
        choiceStd = self.choice(len(all))
        stid = all[choiceStd - 1][5]  # Seçilen öğrencinin ID no aldık.

        print("1-)Name\n2-)Surname\n3-)Department\n4-)Faculty\n5-Type\n6-)ID\n7-)Status\n")
        choice = self.choice(7)  # 1'den 7'ye kadar seçim yaptırdık
        new = input("New Value: ")  # Yeni değeri istedik
        self.cursor.execute(f"UPDATE students SET '{value[choice - 1]}' = '{new}' WHERE stid = '{stid}'")
        self.connect.commit()  # Yeni değer veritabanına kaydedildi
        print(f"Student succesfully updated: {stid}")

    def showAllStudents(self, by):
        global i
        value = ["*", "department", "faculty", "typ", "status"]
        if by == 1:  # Bütün öğrencileri listeler
            allStd = list(self.cursor.execute(f"SELECT * FROM students"))
            for i, value in enumerate(allStd, 1):
                print(str(i) + ")", " - ".join(value))
        else:  # Gelen isteğe göre değeri listeler
            allStd = list(self.cursor.execute(f"SELECT {value[by - 1]} FROM students"))
            num = {}
            for i in allStd:
                if i not in num.keys():
                    num[i] = 1
                else:
                    num[i] += 1
            for i, value in enumerate(num.keys(), 1):
                print(str(i) + ")", " - ".join(value), str(num[value]) + " Student")
            choice = self.choice(i)
            sortBy = list(num.keys())[choice - 1][0]
            all1 = list(self.cursor.execute(f"SELECT * FROM students"))
            allStd = []
            for i in all1:
                for j in i:
                    if sortBy == j:
                        allStd.append(i)
            for i, value in enumerate(allStd, 1):
                print(str(i) + ")", " - ".join(value))
        return allStd


beykent = University("Beykent University", "Turkey")

while beykent.status:
    try:
        beykent.run()
    except:
        continue
