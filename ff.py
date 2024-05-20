class Person:
    def __init__(self, name, age, marital_status, org_type=None, emp_type=None, salary=None, has_children=False, children_in_school=False, num_children_in_school=0, rental_income=None, rental_expenses=None, dividend_income=None, other_income=None):
        self.name = name
        self.age = age
        self.marital_status = marital_status
        self.org_type = org_type
        self.emp_type = emp_type
        self.salary = salary
        self.has_children = has_children
        self.children_in_school = children_in_school
        self.num_children_in_school = num_children_in_school
        self.rental_income = rental_income
        self.rental_expenses = rental_expenses
        self.dividend_income = dividend_income
        self.other_income = other_income

class Employee(Person):
    def __init__(self, name, age, marital_status, org_type, emp_type, salary, has_children, children_in_school, num_children_in_school, rental_income=None, rental_expenses=None, dividend_income=None, other_income=None):
        super().__init__(name, age, marital_status, org_type, emp_type, salary, has_children, children_in_school, num_children_in_school, rental_income, rental_expenses, dividend_income, other_income)

class TaxCalculator:
    def __init__(self, employee):
        self.employee = employee
        self.pit = self.calculate_pit()
        self.surcharge = self.calculate_surcharge()
        self.total_tax = self.pit + self.surcharge
        self.bonus = self.calculate_bonus()
        self.provident_fund = self.calculate_provident_fund()
        self.rental_tax = self.calculate_rental_tax()
        self.dividend_tax = self.calculate_dividend_tax()
        self.other_income_tax = self.calculate_other_income_tax()
        self.total_tax += self.rental_tax + self.dividend_tax + self.other_income_tax

    def calculate_rental_tax(self):
        if self.employee.rental_income is None or self.employee.rental_expenses is None:
            return 0

        taxable_rental_income = max(0, self.employee.rental_income - self.employee.rental_expenses)
        rental_tax_rate = 0.1  # Assuming a flat rate of 10% for simplicity

        return taxable_rental_income * rental_tax_rate

    def calculate_dividend_tax(self):
        if self.employee.dividend_income is None:
            return 0

        taxable_dividend_income = max(0, self.employee.dividend_income - 30000)  # Subtracting specific exemption
        dividend_tax_rate = 0.1  # TDS @ 10%

        return taxable_dividend_income * dividend_tax_rate

    def calculate_other_income_tax(self):
        if self.employee.other_income is None:
            return 0

        taxable_other_income = max(0, self.employee.other_income - (self.employee.other_income * 0.3))  # Subtracting 30% on Gross Other Income
        other_income_tax_rate = 0.1  # Assuming a flat rate of 10% for simplicity

        return taxable_other_income * other_income_tax_rate

    # Existing methods (calculate_pit, calculate_surcharge, calculate_bonus, calculate_provident_fund) remain unchanged...

class Deductions:
    def __init__(self, employee):
        self.employee = employee
        self.deductions = self.calculate_deductions()

    def calculate_deductions(self):         
        deductions = 0
        if self.employee.emp_type == 'Regular':
            if self.employee.org_type == 'Government':
                deductions += min(self.employee.salary * 0.1, 350000)  # NPPF
            else:
                deductions += min(self.employee.salary * 0.1, 350000)  # NPPF
            deductions += 200 * 12  # GIS (200 per month)

        if self.employee.marital_status and self.employee.has_children:
            if self.employee.children_in_school:
                deductions += min(350000 * self.employee.num_children_in_school, 350000 * 5)  # Education allowance
            else:
                deductions += 350000  # Education allowance for a child

        deductions += min(350000, self.employee.salary * 0.05)  # Donations
        deductions += min(350000, self.employee.salary * 0.1)  # Life insurance premium
        deductions += min(350000, self.employee.salary * 0.05)  # Self-education allowance

        return deductions

def calculate_tax():
    name = input("Enter your name: ")
    try:
        age = int(input("Enter your age: "))
    except ValueError:
        print('Please enter a number')
        exit()

    if age < 18:
        print("You are below 18 years of age, so you don't need to pay any tax.")
    else:
        marital_status = input("Are you married? (Yes/No): ").lower() == 'yes'
        org_type = input("Enter your organization type (Government/Private/Corporate): ").lower()
        emp_type = input("Enter your employee type (Regular/Contract): ").lower()
        salary = int(input("Enter your salary: "))
        has_children = False
        children_in_school = False
        num_children_in_school = 0
        
        # Only ask about children if the user is married
        if marital_status:
            has_children = input("Do you have children? (Yes/No): ").lower() == 'yes'
            if has_children:
                children_in_school = input("Are your children going to school? (Yes/No): ").lower() == 'yes'
                num_children_in_school = int(input("Enter the number of children going to school: ")) if children_in_school else 0
                
        rental_income = int(input("Enter your rental income: ")) if input("Do you have rental income? (Yes/No): ").lower() == 'yes' else None
        rental_expenses = int(input("Enter your rental expenses: ")) if input("Do you have rental expenses? (Yes/No): ").lower() == 'yes' else None
        dividend_income = int(input("Enter your dividend income: ")) if input("Do you have dividend income? (Yes/No): ").lower() == 'yes' else None
        other_income = int(input("Enter your other income: ")) if input("Do you have other income? (Yes/No): ").lower() == 'yes' else None

        person = Person(name, age, marital_status, org_type, emp_type, salary, has_children, children_in_school, num_children_in_school, rental_income, rental_expenses, dividend_income, other_income)
        deductions = Deductions(person)
        tax_calculator = TaxCalculator(person)

        print(f"Name: {person.name}")
        print(f"Organization Type: {person.org_type}")
        print(f"Employee Type: {person.emp_type}")
        print(f"Age: {person.age}")
        print(f"Marital Status: {'Married' if person.marital_status else 'Single'}")
        print(f"Has Children: {'Yes' if person.has_children else 'No'}")

        if person.has_children:
            print(f"Children in School: {'Yes' if person.children_in_school else 'No'}")
            if person.children_in_school:
                print(f"Number of Children in School: {person.num_children_in_school}")

        print(f"Salary: {person.salary}")
        print(f"Deductions: {deductions.deductions}")
        print(f"Rental Tax: {tax_calculator.rental_tax}")
        print(f"Dividend Tax: {tax_calculator.dividend_tax}")
        print(f"Other Income Tax: {tax_calculator.other_income_tax}")
        print(f"Personal Income Tax (PIT): {tax_calculator.pit}")
        print(f"Surcharge: {tax_calculator.surcharge}")
        print(f"Total Tax Payable: {tax_calculator.total_tax}")
        print(f"Bonus: {tax_calculator.bonus}")
        print(f"Provident Fund: {tax_calculator.provident_fund}")

if __name__ == "__main__":
    calculate_tax()