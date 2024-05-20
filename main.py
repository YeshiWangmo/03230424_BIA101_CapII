class TaxCalculator:
    def __init__(self):
        self.income_source = None
        self.income_amount = None
        self.employee_type = None
        self.org_type = None
        self.num_children = None
        self.insurance_premium = None

    def take_input(self):
        self.income_source = input("Enter the income source (Salary): ").strip()
        self.income_amount = float(input("Enter the income amount: "))
        self.employee_type = input("Enter the employee type (Regular or Contract): ").strip().lower()
        self.org_type = input("Enter the organization type (Government, Private, or Corporate): ").strip().lower()
        self.num_children = int(input("Enter the number of children: "))
        self.insurance_premium = float(input("Enter the insurance premium: "))

    def calculate_tax(self):
        # Apply general deductions
        taxable_income = self.income_amount
        education_allowance = min(350000 * self.num_children, taxable_income)
        taxable_income -= education_allowance
        taxable_income -= self.insurance_premium

        # Apply specific deductions based on income source
        if self.income_source == "Salary":
            if self.employee_type == "regular":
                if self.org_type == "government":
                    pf_deduction = 0.11 * taxable_income  # Assuming 11% PF contribution for government employees
                else:
                    pf_deduction = 0.05 * taxable_income  # Assuming 5% PF contribution for non-government employees
                taxable_income -= pf_deduction

                gis_deduction = 0.01 * taxable_income  # Assuming 1% GIS contribution
                taxable_income -= gis_deduction

        # Calculate tax based on income slabs
        tax_amount = 0
        if taxable_income > 1500000:
            tax_amount += 0.3 * (taxable_income - 1500000)
            taxable_income = 1500000
        if taxable_income > 1000000:
            tax_amount += 0.25 * (taxable_income - 1000000)
            taxable_income = 1000000
        if taxable_income > 650000:
            tax_amount += 0.2 * (taxable_income - 650000)
            taxable_income = 650000
        if taxable_income > 400000:
            tax_amount += 0.15 * (taxable_income - 400000)
            taxable_income = 400000
        if taxable_income > 300000:
            tax_amount += 0.1 * (taxable_income - 300000)

        # Apply surcharge if applicable
        if taxable_income >= 1000000:
            tax_amount += 0.1 * tax_amount

        return tax_amount

# Main program
tax_calculator = TaxCalculator()
tax_calculator.take_input()
tax_payable = tax_calculator.calculate_tax()
print(f"Total tax payable: Nu. {tax_payable:.2f}")