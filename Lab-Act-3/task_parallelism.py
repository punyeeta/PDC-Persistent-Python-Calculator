from concurrent.futures import ThreadPoolExecutor
import threading

# Deduction functions (separate tasks)
def compute_sss(salary):
    print(f"SSS computed by: {threading.current_thread().name}")
    return salary * 0.045

def compute_philhealth(salary):
    print(f"PhilHealth computed by: {threading.current_thread().name}")
    return salary * 0.025

def compute_pagibig(salary):
    print(f"Pag-IBIG computed by: {threading.current_thread().name}")
    return salary * 0.02

def compute_tax(salary):
    print(f"Withholding Tax computed by: {threading.current_thread().name}")
    return salary * 0.10


def main():
    salary = 30000  # Example salary

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

    # Display results
    print("\n--- Deduction Breakdown ---")
    print(f"SSS: {sss:.2f}")
    print(f"PhilHealth: {philhealth:.2f}")
    print(f"Pag-IBIG: {pagibig:.2f}")
    print(f"Withholding Tax: {tax:.2f}")
    print(f"Total Deduction: {total_deduction:.2f}")


if __name__ == "__main__":
    main()
