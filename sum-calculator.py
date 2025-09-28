import tkinter as tk
from tkinter import messagebox, filedialog
from openpyxl import Workbook

class GPAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("محاسبه معدل دانشگاه")

        self.courses = []  
        self.edit_index = None  

        # ورودی‌ها
        tk.Label(root, text="نام درس:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = tk.Entry(root)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="نمره:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_grade = tk.Entry(root)
        self.entry_grade.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="تعداد واحد:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_credit = tk.Entry(root)
        self.entry_credit.grid(row=2, column=1, padx=5, pady=5)

        # دکمه‌ها
        tk.Button(root, text="➕ اضافه کردن درس", command=self.add_course).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(root, text="🗑️ حذف درس انتخاب‌شده", command=self.delete_course).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(root, text="✏️ ویرایش درس انتخاب‌شده", command=self.edit_course).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(root, text="📊 محاسبه معدل", command=self.calculate_gpa).grid(row=6, column=0, columnspan=2, pady=5)
        tk.Button(root, text="💾 ذخیره در فایل متنی", command=self.save_to_txt).grid(row=7, column=0, columnspan=2, pady=5)
        tk.Button(root, text="📑 ذخیره در اکسل", command=self.save_to_excel).grid(row=8, column=0, columnspan=2, pady=10)

        # لیست دروس
        self.course_list = tk.Listbox(root, width=50, height=10)
        self.course_list.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    def add_course(self):
        try:
            name = self.entry_name.get()
            grade = float(self.entry_grade.get())
            credit = int(self.entry_credit.get())

            if not name.strip():
                messagebox.showwarning("خطا", "نام درس را وارد کنید")
                return

            if self.edit_index is not None:
                self.courses[self.edit_index] = (name, grade, credit)
                self.course_list.delete(self.edit_index)
                self.course_list.insert(self.edit_index, f"{name} - نمره: {grade} - واحد: {credit}")
                self.edit_index = None
            else:
                self.courses.append((name, grade, credit))
                self.course_list.insert(tk.END, f"{name} - نمره: {grade} - واحد: {credit}")

            self.entry_name.delete(0, tk.END)
            self.entry_grade.delete(0, tk.END)
            self.entry_credit.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("خطا", "لطفاً نمره و تعداد واحد را به‌صورت عددی وارد کنید")

    def delete_course(self):
        try:
            selected_index = self.course_list.curselection()[0]
            self.course_list.delete(selected_index)
            del self.courses[selected_index]
        except IndexError:
            messagebox.showwarning("هشدار", "هیچ درسی برای حذف انتخاب نشده است")

    def edit_course(self):
        try:
            selected_index = self.course_list.curselection()[0]
            self.edit_index = selected_index
            name, grade, credit = self.courses[selected_index]

            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, name)

            self.entry_grade.delete(0, tk.END)
            self.entry_grade.insert(0, grade)

            self.entry_credit.delete(0, tk.END)
            self.entry_credit.insert(0, credit)

        except IndexError:
            messagebox.showwarning("هشدار", "هیچ درسی برای ویرایش انتخاب نشده است")

    def calculate_gpa(self):
        if not self.courses:
            messagebox.showwarning("هشدار", "هیچ درسی اضافه نشده است")
            return None

        total_points = sum(grade * credit for _, grade, credit in self.courses)
        total_credits = sum(credit for _, _, credit in self.courses)
        gpa = total_points / total_credits
        messagebox.showinfo("معدل", f"معدل شما: {gpa:.2f}")
        return gpa

    def save_to_txt(self):
        if not self.courses:
            messagebox.showwarning("هشدار", "هیچ درسی برای ذخیره وجود ندارد")
            return

        gpa = self.calculate_gpa()
        if gpa is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("لیست دروس:\n")
                for name, grade, credit in self.courses:
                    f.write(f"{name} - نمره: {grade} - واحد: {credit}\n")
                f.write(f"\nمعدل کل: {gpa:.2f}\n")

            messagebox.showinfo("ذخیره", f"فایل متنی با موفقیت ذخیره شد:\n{file_path}")

    def save_to_excel(self):
        if not self.courses:
            messagebox.showwarning("هشدار", "هیچ درسی برای ذخیره وجود ندارد")
            return

        gpa = self.calculate_gpa()
        if gpa is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", 
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if file_path:
            wb = Workbook()
            ws = wb.active
            ws.title = "Courses"

            # هدرها
            ws.append(["نام درس", "نمره", "تعداد واحد"])

            # داده‌ها
            for name, grade, credit in self.courses:
                ws.append([name, grade, credit])

            # معدل در آخر
            ws.append([])
            ws.append(["", "معدل کل", gpa])

            wb.save(file_path)
            messagebox.showinfo("ذخیره", f"فایل اکسل با موفقیت ذخیره شد:\n{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GPAApp(root)
    root.mainloop()
