from concurrent.futures import ThreadPoolExecutor
import threading

# Deduction functions (separate tasks)
def compute_sss(salary):
    return salary * 0.045

def compute_philhealth(salary):
    return salary * 0.025

def compute_pagibig(salary):
    return salary * 0.02

def compute_tax(salary):
    return salary * 0.10
def salary_input(text):
    width = len(text) + 4
    print("+" + "-" * width + "+")
    print(f"|  {text}  |")
    print("+" + "-" * width + "+")


def main():
    salary = float(input("Enter monthly salary: "))

    print()
    salary_input(f"Salary Entered: PHP {salary:,.2f}")
    print("\nStarting parallel deduction computation...\n")

    # Create ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks (returns Future objects)
        future_sss = executor.submit(compute_sss, salary)
        future_philhealth = executor.submit(compute_philhealth, salary)
        future_pagibig = executor.submit(compute_pagibig, salary)
        future_tax = executor.submit(compute_tax, salary)

        # Retrieve results from Future objects
        sss = future_sss.result()
        philhealth = future_philhealth.result()
        pagibig = future_pagibig.result()
        tax = future_tax.result()

    total_deduction = sss + philhealth + pagibig + tax
    Net_salary = salary - total_deduction

    # Display results
    print("\n========== Deduction Breakdown ==========")
    print(f"{'SSS':15} : {sss:10.2f}")
    print(f"{'PhilHealth':15} : {philhealth:10.2f}")
    print(f"{'Pag-IBIG':15} : {pagibig:10.2f}")
    print(f"{'Withholding Tax':15} : {tax:10.2f}")
    print("----------------------------------------")
    print(f"{'Total Deduction':15} : {total_deduction:10.2f}")
    print(f"{'Net Salary':15} : {Net_salary:10.2f}")

if __name__ == "__main__":
    main()
