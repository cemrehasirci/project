import tkinter as tk
from datetime import date, timedelta
from tkinter import Canvas, messagebox, ttk, Frame

class Appointment:
    def __init__(self, policlinic, doctor, date, time):
        self.policlinic = policlinic
        self.doctor = doctor
        self.date = date
        self.time = time
        self.next = None

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.appointments = None  # Initially empty linked list

# User information
user_information = {
    '1' : User('Ayşe', '1'),
    '12345678901': User('Ahmet', 'ahmet123'),
    # Add other users here
}

# Polyclinic and Doctor information
policlinics = {
    'Cardiology': ['Dr. Ahmet', 'Dr. Mehmet', 'Dr. Ayşe', 'Dr. Fatma'],
    'Dermatology': ['Dr. Ali', 'Dr. Hasan', 'Dr. Hüseyin', 'Dr. Can'],
    'Neurology': ['Dr. İsmail', 'Dr. Deniz', 'Dr. Mehmet', 'Dr. Bilge'],
    'Orthopedics': ['Dr. Sezer', 'Dr. Hasan', 'Dr. Göksel', 'Dr. Can'],
    'Eye Diseases': ['Dr. İsmail', 'Dr. Rüzgar', 'Dr. Mehmet', 'Dr. Ayşe'],
    'Ear Nose Throat': ['Dr. Kayra', 'Dr. Hasan', 'Dr. Burcu', 'Dr. Can'],
    'Internal Medicine': ['Dr. İsmail', 'Dr. Ahmet', 'Dr. Koray', 'Dr. Ayşe'],
    'Child Health and Diseases': ['Dr. Yiğit', 'Dr. Kemal', 'Dr. Duru', 'Dr. Fatma'],
    'Gynecology and Obstetrics': ['Dr. İsmail', 'Dr. Mustafa', 'Dr. Mehmet', 'Dr. Ayşe'],
    'Psychiatry': ['Dr. Ali', 'Dr. Hasan', 'Dr. Hüseyin', 'Dr. Pelin']
}

def log_in():
    global user
    id = id_entry.get()
    password = password_entry.get()
    if id in user_information and user_information[id].password == password:
        user = user_information[id]  
        log_in_screen.pack_forget()
        welcome_label.config(text=f"Welcome {user.name}")
        main_screen.pack()
    else:
        messagebox.showerror("Login Failed", "ID Number or Password is incorrect")

def sign_up():
    sign_up_screen = tk.Toplevel(root)
    sign_up_screen.geometry("300x300")
    sign_up_screen.title("Sign up")
    sign_up_screen.geometry("+{}+{}".format(650,250))

    tk.Label(sign_up_screen, text="ID No:").pack(pady=10)
    new_id_entry = tk.Entry(sign_up_screen)
    new_id_entry.pack(pady=10)

    tk.Label(sign_up_screen, text="Password:").pack(pady=10)
    new_password_entry = tk.Entry(sign_up_screen, show="*")
    new_password_entry.pack(pady=10)

    tk.Label(sign_up_screen, text="Name:").pack(pady=10)
    new_name_entry = tk.Entry(sign_up_screen)
    new_name_entry.pack(pady=10)

    tk.Button(sign_up_screen, text="Sign Up", command=lambda: registration_confirm(new_id_entry.get(), new_password_entry.get(), new_name_entry.get(), sign_up_screen)).pack(pady=10)

def registration_confirm(id, password, name, sign_up_screen):
    if id not in user_information:
        user_information[id] = User(name, password)
        messagebox.showinfo("Registration Successful", "Registration completed successfully.")
        sign_up_screen.destroy()
    else:
        messagebox.showerror("Error", "This ID Number is already registered.")

def make_an_appointment():
    main_screen.pack_forget()
    policlinic_choose_screen.pack()
    policlinic_choose.set(' ')       # Reset outpatient clinic selection
    doctor_choose.set('Doctor:')     # Reset outpatient doctor selection

def choose_policlinic():
    choosen_policlinic = policlinic_choose.get()
    if choosen_policlinic != ' ':    # Make sure the user makes a selection
        policlinic_choose_screen.pack_forget()
        doctor_choose['values'] = sorted(policlinics[choosen_policlinic])    # Show doctors
        doctor_choose_screen.pack()
    else:
        messagebox.showerror("Error", "Please select an outpatient clinic")

def choose_doctor():
    choosen_doctor = doctor_choose.get()
    if choosen_doctor != 'Doctor:':      # Make sure the user makes a selection
        doctor_choose_screen.pack_forget()
        date_choose.set('Date:')         # reset date selection
        time_choose.set('Time:')         # reset time selection
        minute_choose.set('Minute:')     # reset min selection
        date_choose_screen.pack()
    else:
        messagebox.showerror("Error", "Please select a doctor")

def confirm_appointment():

    choosen_date = date_choose.get()
    choosen_time = time_choose.get()
    choosen_minute = minute_choose.get()

    if choosen_date != 'Date:' and choosen_time != 'Time:' and choosen_minute != 'Minute:':
        policlinic = policlinic_choose.get()
        doctor = doctor_choose.get()
        if is_appointment_available(policlinic, doctor, choosen_date, choosen_minute) == 1:
            messagebox.showerror("Error", "The same appointment was made before. Please make a new appointment.")
        elif is_appointment_available(policlinic, doctor, choosen_date, choosen_minute) == 0:
            messagebox.showerror("Error", "An appointment cannot be made at the selected time. Please select another time.")
        else:
            date_choose_screen.pack_forget()
            added_appointment(policlinic, doctor, choosen_date, choosen_minute)
            messagebox.showinfo("Appointment confirmed", f"Appointment confirmed!\nPoliclinic: {policlinic}\nDoctor: {doctor}\nDate: {choosen_date}\nTime: {choosen_minute}")
            main_screen.pack()
    else:
        messagebox.showerror("Error", "Please select a date, time or minute")

def is_appointment_available(policlinic, doctor, date, time):
    current = user.appointments
    while current is not None:
        if (
            current.policlinic == policlinic
            and current.doctor == doctor
            and current.date == date
            and current.time == time
        ):
            return 1    # same appointment available
        elif (
            current.date == date
            and current.time == time
        ):
            return 0    # there is another appointment at that date and time
        current = current.next
    return -1

def my_appointments():
    main_screen.pack_forget()
    appointments_screen.pack(fill='both', expand=1)
    canvas = Canvas(appointments_screen)
    canvas.pack(side='left', fill='both', expand=1)
    
    scrollbar = ttk.Scrollbar(appointments_screen, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')
    
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind(' <Configure> ', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    second_frame = Frame(canvas)
    canvas.create_window((200,0), window=second_frame)
    
    
    if user.appointments:  # If the user has appointments
        current = user.appointments
        i = 1
        while current is not None:
            tk.Label(second_frame, text=f"Appointment {i}:\nPoliclinic: {current.policlinic}\nDoctor: {current.doctor}\nDate: {current.date}\nTime: {current.time}").pack( pady=10)
            tk.Button(second_frame, text="Delete appointment", command=lambda current=current: delete_appointment(current)).pack(pady=10)
            current = current.next
            i += 1
    else:    # If the user has not appointments
        tk.Label(second_frame, text="You have not an appointment").pack(pady=10)
    tk.Button(second_frame, text="Back", command=back).pack(pady=10)
    
def added_appointment(policlinic, doctor, date, time):
    new_appointment = Appointment(policlinic, doctor, date, time)
    new_appointment.next = user.appointments
    user.appointments = new_appointment

def delete_appointment(appointment):
    current = user.appointments
    if current == appointment:
        user.appointments = current.next
    else:
        while current.next != appointment:
            current = current.next
        current.next = current.next.next
    back()   # Refresh the appointments_screen

def back():
    appointments_screen.pack_forget()
    for widget in appointments_screen.winfo_children():
        widget.destroy()     # Clear appointments screen
    main_screen.pack()
    
def update_minutes(event):
    selected_hour = str(time_choose.get())
    if selected_hour:
        hour = selected_hour.split(":")[0]
        min = [f"{hour}:{minute}" for minute in ('00', '15', '30', '45')]
        minute_choose['values'] = min
        minute_choose.set("Minute:")

def account_screen():
    main_screen.pack_forget()
    # Position of the window
    root.geometry("400x400")
    root.title("Hospital Appointment System")
    root.geometry("+{}+{}".format(600,200))
    id_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    id_entry.focus()    #move the cursor there
    log_in_screen.pack()
    
root = tk.Tk()
# Position of the window
root.geometry("400x400")
root.title("Hospital Appointment System")
root.geometry("+{}+{}".format(600,200))

log_in_screen = tk.Frame(root)
tk.Label(log_in_screen, text="ID No:").pack(pady=10)
id_entry = tk.Entry(log_in_screen)
id_entry.pack(pady=10)

tk.Label(log_in_screen, text="Password:").pack(pady=10)
password_entry = tk.Entry(log_in_screen, show="*")
password_entry.pack(pady=10)

tk.Button(log_in_screen, text="Log in", command=log_in).pack(side="left", padx=10, pady=10)
tk.Button(log_in_screen, text="Sign up", command=sign_up).pack(side="left", padx=10, pady=10)

log_in_screen.pack()

main_screen = tk.Frame(root)
welcome_label = tk.Label(main_screen)
welcome_label.pack(pady=10)
tk.Button(main_screen, text="Make an Appointment", command=make_an_appointment).pack(pady=10)
tk.Button(main_screen, text="My Appointments", command=my_appointments).pack(pady=10)
tk.Button(main_screen, text="Log Out", command=account_screen).pack(pady=10)

appointments_screen = tk.Frame(root)

policlinic_choose_screen = tk.Frame(root)
policlinic_choose = tk.StringVar(value=None)
for policlinic in policlinics.keys():
    tk.Radiobutton(policlinic_choose_screen, text=policlinic, variable=policlinic_choose, value=policlinic).pack(anchor='w')
tk.Button(policlinic_choose_screen, text="Confirm", command=choose_policlinic).pack(pady=10)

doctor_choose_screen = tk.Frame(root)
doctor_choose = ttk.Combobox(doctor_choose_screen, state="readoctornly")
doctor_choose.pack(pady=10)

tk.Button(doctor_choose_screen, text="Confirm", command=choose_doctor).pack(pady=10)

date_choose_screen = tk.Frame(root)
dates = []
current_date = date.today()
for i in range(10):
    current_date = current_date + timedelta(days=1)
    formatted_date = current_date.strftime("%d/%m/%y")
    dates.append(f"{formatted_date}")
date_choose = ttk.Combobox(date_choose_screen, values=dates, state="readoctornly")
date_choose.set("Date:")
date_choose.pack(pady=10)

hours = [f"{i}:00" for i in range(9, 17)]

time_choose = ttk.Combobox(date_choose_screen, values=hours, state="readonly")
time_choose.set("Time:")
time_choose.pack(pady=10)
time_choose.bind("<<ComboboxSelected>>", update_minutes)

minute_choose = ttk.Combobox(date_choose_screen, values=[], state="readonly")
minute_choose.set("Minute:")
minute_choose.pack(pady=10)

tk.Button(date_choose_screen, text="Make an Appointment", command=confirm_appointment).pack(pady=10)

root.mainloop()
