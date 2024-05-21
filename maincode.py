class Person:
    def __init__(self, name, age, marital_status, organization_type, employee_type):
        self.name = name
        self.age = age
        self.marital_status = marital_status
        self.organization_type = organization_type
        self.employee_type = employee_type

class Employee(Person):
    def __init__(self, name, age, marital_status, organization_type, employee_type, income, gis_contributions, pension_contributions, life_insurance_premium, self_education_allowance, donations, bonus_amount, rental_income=0, dividend_income=0, other_income=0):
        super().__init__(name, age, marital_status, organization_type, employee_type)
        self.income = income
        self.gis_contributions = gis_contributions
        self.pension_contributions = pension_contributions
        self.life_insurance_premium = life_insurance_premium
        self.self_education_allowance = self_education_allowance
        self.donations = donations
        self.bonus_amount = bonus_amount
        self.rental_income = rental_income
        self.dividend_income = dividend_income
        self.other_income = other_income
        self.num_children = 0
        self.child_edu_allowances = []
        self.sponsored_edu_expenses = []

    #for checking if the user have children or not to calculate education allowance
        if marital_status.lower() == "married":
            self.num_children = self.get_num_children() 
            if self.num_children > 0:
                self.child_edu_allowances = self.get_child_education_allowances()   
                self.sponsored_edu_expenses = self.get_sponsored_education_expenses()

    def get_num_children(self):
        while True:
            try:# for calculating education alllowance for children
                num_children_input = input("Do you have children? (yes/no): ")
                if num_children_input.lower() == "yes":
                    return int(input("Enter the number of your children: "))
                elif num_children_input.lower() == "no":
                    return 0
                else:
                    print("Please enter yes or no.")
            except ValueError:
                print(" Please enter a valid number of children.")

    def get_child_education_allowances(self):
        allowances = []
        for child in range(self.num_children):
            while True:
                try: #Education allowance up to a max of Nu. 350,000 per child.
                    allowance = float(input(f"Enter education allowance for child {child + 1} (max Nu. 350,000): "))
                    allowances.append(min(allowance, 350000))
                    break
                except ValueError:
                    print("Please enter a valid number.")
        return allowances

    def get_sponsored_education_expenses(self):
        expenses = []
        for child in range(self.num_children):
            while True:
                goes_to_school = input(f"Does your child {child + 1} go to school? (y/n): ").lower()  # calaculating education allowance f0r each children
                if goes_to_school in ['y', 'n']:
                    break
                print("There is no such option,  check the spelling and retype it again.")

            if goes_to_school == "y":
                while True:
                    try:
                        expense = float(input(f"Enter your sponsored education expense for your child {child + 1} (max Nu. 350,000): "))
                        expenses.append(min(expense, 350000)) #Sponsored children education expense up to max of Nu. 350,000 per child.
                        break
                    except ValueError:
                        print(" Please enter a valid number.")
            else:
                expenses.append(0)
        return expenses

class TaxCalculator:
    def __init__(self, employee):
        self.employee = employee

    def calculate_tax(self):
        total_income = self.employee.income
    #Deduction
        total_income -= self.employee.gis_contributions
        total_income -= self.employee.pension_contributions

        rental_income = self.employee.rental_income * 0.8  # 20% deduction on repairs and maintenance.
        total_income += rental_income

        # 10 %  of TDS
        if self.employee.dividend_income > 30000:
            dividend_income = (self.employee.dividend_income - 30000) * 0.9  
        else:
            dividend_income = self.employee.dividend_income
        total_income += dividend_income
        
        #30% deduction on other income
        other_income = self.employee.other_income * 0.7 
        total_income += other_income

        total_income -= sum(self.employee.child_edu_allowances)
        total_income -= self.employee.life_insurance_premium
        total_income -= min(self.employee.self_education_allowance, 350000)

        #checking whether donation exceed 5% of the incomr
        max_donation = 0.05 * total_income
        if self.employee.donations > max_donation:
            print(f"Note: Donations are limited to {max_donation}. Excess amount will not be considered for deduction.")
            donations = max_donation
        else:
            donations = self.employee.donations

        total_income -= donations
        total_income -= sum(self.employee.sponsored_edu_expenses)
        total_income -= self.employee.bonus_amount  
        return self.apply_tax_slabs(total_income)

    def apply_tax_slabs(self, total_income):
        tax_amount = 0
        if total_income <= 300000:
            tax_amount = 0
        elif total_income <= 400000:
            tax_amount = (total_income - 300000) * 0.1
        elif total_income <= 650000:
            tax_amount = (total_income - 400000) * 0.15 + 10000
        elif total_income <= 1000000:
            tax_amount = (total_income - 650000) * 0.2 + 45500
        elif total_income <= 1500000:
            tax_amount = (total_income - 1000000) * 0.25 + 130500
        else:
            tax_amount = (total_income - 1500000) * 0.3 + 280500

        if total_income >= 1000000:
            tax_amount += tax_amount * 0.1

        return tax_amount

def main():
    while True:
        print("Personal Income Tax (PIT) Calculator")
        name = input("Enter your name: ")

        while True:
            try:
                age = int(input("Enter your age: "))
                if age > 100:
                    print("Enter your age correctly.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        if age < 18:
            print("Since you are below 18 years old. You are not required to pay taxes.")
            continue

        while True:
            marital_status = input("Enter your marital status (Married/Single): ").lower()
            if marital_status in ["married", "single"]:
                break
            else:
                print("There is no such option, check the spelling and retype it again.")

        while True:
            organization_type = input("Enter the organization type (Government/Private/Corporate): ").lower()
            if organization_type in ["government", "private", "corporate"]:
                break
            else:
                print("There is no such option, make sure you check the spelling and retype it again.")

        while True:
            employee_type = input("Enter the employee type (Regular/Contract): ").lower()
            if employee_type in ["regular", "contract"]:
                break
            else:
                print("There is no such option, make sure you check the spelling and retype it again.")

        while True:
            try:
                income = float(input("Enter your annual gross salary: "))
                gis_contributions = float(input("Enter your GIS contributions: "))
                pension_contributions = float(input("Enter your pension contributions (NPPF/PF): ")) if organization_type!= "government" and employee_type == "contract" else 0
                life_insurance_premium = float(input("Enter your life insurance premium: "))
                self_education_allowance = float(input("Enter your self-education allowance, if any: ") or 0)
                donations = float(input("Enter your donations (if any): ") or 0)
                bonus_amount = float(input("Enter your bonus amount: ") or 0)
                rental_income = float(input("Enter your annual rental income (if any): ") or 0)
                dividend_income = float(input("Enter your annual dividend income (if any): ") or 0)
                other_income = float(input("Enter your annual income from other sources (if any): ") or 0)
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        employee = Employee(name, age, marital_status, organization_type, employee_type, income, gis_contributions, pension_contributions, life_insurance_premium, self_education_allowance, donations, bonus_amount, rental_income, dividend_income, other_income)
        calculator = TaxCalculator(employee)
        tax_amount = calculator.calculate_tax()
        print(f"{employee.name}'s tax amount is: {tax_amount}")
        
        #making the code again if the user wants if not exit
        run_again = input("Would you like to calculate tax again? (yes/no): ").lower()
        if run_again!= "yes":
            break

if __name__ == "__main__":
    main()
