from concurrent.futures import ProcessPoolExecutor

# Exactly as shown in the example structure
def compute_total_deduction(employee):
    name, salary = employee
    total = salary * (0.045 + 0.025 + 0.02 + 0.10)
    return name, total

# Employees data
employees = [
    ("Alice", 25000),
    ("Bob", 32000),
    ("Charlie", 28000),
    ("Diana", 40000),
    ("Edward", 35000)
]

print("Data Parallelism - Total Deductions Only")
print("=" * 50)

if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = executor.map(compute_total_deduction, employees)
        
        for name, total in results:
            net = 0  # Net not calculated in this version
            print(f"{name}: Total Deduction = ₱{total:,.2f}")