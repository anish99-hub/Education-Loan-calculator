import pandas as pd
import numpy_financial as npf

# Get loan amount from user
while True:  # Loop until a valid loan amount is entered
    Loan_Amount = int(input("Please enter your loan amount: "))
    if Loan_Amount > 0:
        break
    else:
        print("Invalid loan amount. The loan amount must be a positive value.")
        print("Please enter a valid loan amount.")

# Get rate of interest from user
while True:  # Loop until a valid rate of interest is entered
    Rate_of_Interest = float(input("Please enter your rate of interest (in percentage): "))
    if Rate_of_Interest > 0 and Rate_of_Interest <= 100:
        break
    else:
        print("Invalid rate of interest. The rate must be between 0 and 100%.")
        print("Please enter a valid rate of interest.")

# Get loan tenure from user
while True:  # Loop until a valid loan tenure is entered
    Loan_tenure = int(input("Please enter your loan tenure (in Years): "))
    if Loan_tenure > 0:  # Check if loan tenure is positive
        while True:  # Get course duration
            Course_Duration = int(input("Please enter your course duration (in Years): "))
            if Course_Duration > 0:
                break
            else:
                print("Course duration must be a positive value.")
                print("Please enter a valid course duration.")
        
        while True:  # Get moratorium period
            Moratorium_Period = int(input("Please enter your moratorium period (in Years): "))
            if Moratorium_Period > 0:
                break
            else:
                print("Moratorium period must be a positive value.")
                print("Please enter a valid moratorium period.")
        
        if Loan_tenure > (Moratorium_Period + Course_Duration):
            break
        else:
            print("Loan tenure must be greater than the sum of Moratorium Period and Course Duration.")
            print("Please enter valid values.")
    else:
        print("Loan tenure must be a positive value.")
        print("Please enter a valid loan tenure.")

# Get monthly payment amount from user
while True:  # Loop until a valid monthly payment is entered
    monthly_payment = float(input("Please enter your monthly payment during the course period: "))
    if monthly_payment > 0:
        break
    else:
        print("Invalid monthly payment. The payment must be a positive value.")
        print("Please enter a valid monthly payment.")

# Convert annual interest rate to a decimal
Rate_of_Interest = Rate_of_Interest / 100

# Initialize variables for loan calculations
remaining_principal_course_period = Loan_Amount
simple_interest_course_period = 0

course_period_data = []
# Calculate payments during the course period
for month in range(1, Course_Duration * 12 + 1):
    monthly_interest = remaining_principal_course_period * (Rate_of_Interest / 12)
    simple_interest_course_period += monthly_interest
    
    principal_payment = max(0, monthly_payment - monthly_interest)
    remaining_principal_course_period -= principal_payment
  
    # Store data for each month during the course period
    course_period_data.append({
        'Month': month,
        'Monthly Payment During Course Period': monthly_payment,
        'Interest Payment During Course Period': monthly_interest,
        'Principal Payment During Course Period': principal_payment,
        'Remaining Principal During Course Period': remaining_principal_course_period
    })
    
    if remaining_principal_course_period <= 0:
        break

# Calculate total amount paid during the course period
total_amount_paid_course_period = monthly_payment * len(course_period_data)
print(f"\nTotal Amount Paid During Course Period: {total_amount_paid_course_period:.2f}")

# Calculate new loan amount after course period
new_loan_amount = remaining_principal_course_period + simple_interest_course_period

# Calculate remaining loan tenure and EMI
remaining_loan_tenure = Loan_tenure - Course_Duration - Moratorium_Period
monthly_interest_rate = Rate_of_Interest / 12

# Calculate EMI using numpy_financial
emi = -npf.pmt(monthly_interest_rate, remaining_loan_tenure * 12, new_loan_amount)

loan_data = []
principal_remaining = new_loan_amount

# Calculate payments after the course period
for month in range(1, remaining_loan_tenure * 12 + 1):
    interest_payment = principal_remaining * monthly_interest_rate
    principal_payment = emi - interest_payment
    principal_remaining -= principal_payment

    # Store data for each month after the course period
    loan_data.append({
        'Month': month,
        'EMI After Course Period': emi,
        'Interest Payment After Course Period': interest_payment,
        'Principal Payment After Course Period': principal_payment,
        'Remaining Principal After Course Period': principal_remaining
    })

# Convert the lists to DataFrames for better visualization
df_course = pd.DataFrame(course_period_data)
df_remaining = pd.DataFrame(loan_data)

# Apply rounding for the final display
df_course = df_course.round(2)
df_remaining = df_remaining.round(2)

# Display the loan amortization schedule during the course period
print("\nLoan Amortization Schedule During Course Period:")
print(df_course)

# Display the loan amortization schedule after the course period
print("\nLoan Amortization Schedule After Course Period:")
print(df_remaining)

# Calculate total interest paid
total_interest_paid = df_remaining['Interest Payment After Course Period'].sum()
total_interest_paid += simple_interest_course_period
print(f"\nTotal Interest Paid (including course period) over {Loan_tenure} Years: {total_interest_paid:.2f}")

# Calculate total outstanding payment
total_principal_after_course_period = df_remaining['Principal Payment After Course Period'].sum()
total_interest_after_course_period = df_remaining['Interest Payment After Course Period'].sum()
total_outstanding_pay = total_principal_after_course_period + total_interest_after_course_period + simple_interest_course_period

print(f"\nTotal Outstanding Payment: {total_outstanding_pay:.2f}")

# Display last EMI amount after the course period
if len(df_remaining) > 0:
    last_emi = df_remaining['EMI After Course Period'].iloc[-1]
    print(f"\nLast EMI After Course Period: {last_emi:.2f}")

# Function to calculate fee
def calculate_fee(Loan_Amount):
    return Loan_Amount * 0.01 * 1.18  # Example fee calculation

Fee_paid = Loan_Amount
result_fee = calculate_fee(Loan_Amount)
print(f"Fee Paid: {result_fee:.2f}")

# Function to calculate insurance
def calculate_insurance(Loan_Amount):
    return Loan_Amount * 0.01  # Example insurance calculation

Insurance = Loan_Amount
result_insu = calculate_insurance(Loan_Amount)
print(f"Insurance: {result_insu:.2f}")

# Calculate and display total payment including insurance and fees
total_payment_with_insurance_fees = result_insu + result_fee + total_outstanding_pay
print(f"\nTotal Payment (including insurance and fees): {total_payment_with_insurance_fees:.2f}")


# Calculate the final effective interest rate
total_principal_paid = Loan_Amount  # Since the principal paid is the loan amount
final_effective_interest_rate = (total_interest_paid / Loan_Amount) * 100

print(f"\nFinal Effective Interest Rate Paid by Student: {final_effective_interest_rate:.2f}%")
