"""
Mortgage Refinancing Calculator
"""


def get_float_input(prompt: str, min_val: float = 0, max_val: float = None) -> float:
    """Get validated float input from user."""
    while True:
        try:
            value = float(input(prompt))
            if value < min_val:
                print(f"  ⚠ Value must be at least {min_val}")
                continue
            if max_val and value > max_val:
                print(f"  ⚠ Value must be at most {max_val}")
                continue
            return value
        except ValueError:
            print("  ⚠ Please enter a valid number")


def get_int_input(prompt: str, min_val: int = 1) -> int:
    """Get validated integer input from user."""
    while True:
        try:
            value = int(input(prompt))
            if value < min_val:
                print(f"  ⚠ Value must be at least {min_val}")
                continue
            return value
        except ValueError:
            print("  ⚠ Please enter a valid whole number")


def calculate_monthly_payment(principal: float, annual_rate: float, months: int) -> float:
    """
    Calculate monthly mortgage payment using standard amortization formula.
    
    P = L[c(1 + c)^n] / [(1 + c)^n - 1]
    Where:
        P = monthly payment
        L = loan principal
        c = monthly interest rate (annual rate / 12)
        n = number of payments (months)
    """
    if annual_rate == 0:
        return principal / months
    
    monthly_rate = annual_rate / 100 / 12
    payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / \
              ((1 + monthly_rate) ** months - 1)
    return payment


def estimate_closing_costs(loan_amount: float) -> tuple[float, float, float]:
    """
    Estimate closing costs based on typical percentages.
    Returns (low, mid, high) estimates.
    
    Typical closing costs: 2-5% of loan amount
    """
    low = loan_amount * 0.02
    mid = loan_amount * 0.03
    high = loan_amount * 0.05
    return low, mid, high


def calculate_break_even(closing_costs: float, monthly_savings: float) -> float:
    """Calculate months to break even on closing costs."""
    if monthly_savings <= 0:
        return float('inf')
    return closing_costs / monthly_savings


def print_header():
    """Print the calculator header."""
    print("\n" + "=" * 60)
    print("         🏠 MORTGAGE REFINANCING CALCULATOR 🏠")
    print("=" * 60)
    print()


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


def format_currency(amount: float) -> str:
    """Format a number as currency."""
    return f"${amount:,.2f}"


def format_months(months: float) -> str:
    """Format months as years and months."""
    if months == float('inf'):
        return "Never (no savings)"
    
    years = int(months // 12)
    remaining_months = int(months % 12)
    
    if years == 0:
        return f"{remaining_months} months"
    elif remaining_months == 0:
        return f"{years} years"
    else:
        return f"{years} years, {remaining_months} months"


def main():
    print_header()
    
    print_section("CURRENT MORTGAGE DETAILS")
    
    current_balance = get_float_input(
        "  Remaining loan balance: $", min_val=1000
    )
    
    current_rate = get_float_input(
        "  Current interest rate (%): ", min_val=0.1, max_val=30
    )
    
    remaining_years = get_int_input(
        "  Years remaining on loan: ", min_val=1
    )
    remaining_months = remaining_years * 12
    
    current_payment = get_float_input(
        "  Current monthly payment (principal + interest): $", min_val=100
    )
    
    print_section("NEW LOAN DETAILS")
    
    new_rate = get_float_input(
        "  New interest rate (%): ", min_val=0.1, max_val=30
    )
    
    print("\n  New loan term options:")
    print("    1. Keep same remaining term ({} years)".format(remaining_years))
    print("    2. Start fresh with new term")
    
    term_choice = input("  Choose (1 or 2): ").strip()
    
    if term_choice == "2":
        new_term_years = get_int_input("  New loan term (years): ", min_val=1)
        new_term_months = new_term_years * 12
    else:
        new_term_years = remaining_years
        new_term_months = remaining_months
    
    print_section("CLOSING COSTS")
    
    low_est, mid_est, high_est = estimate_closing_costs(current_balance)
    
    print(f"  Typical closing costs range: {format_currency(low_est)} - {format_currency(high_est)}")
    print(f"  (Usually 2-5% of loan amount)")
    print()
    
    use_estimate = input("  Do you have actual closing cost quote? (y/n): ").strip().lower()
    
    if use_estimate == 'y':
        closing_costs = get_float_input("  Enter closing costs: $", min_val=0)
    else:
        print(f"  Using mid-range estimate: {format_currency(mid_est)}")
        closing_costs = mid_est
    
    new_payment = calculate_monthly_payment(current_balance, new_rate, new_term_months)
    monthly_savings = current_payment - new_payment
    annual_savings = monthly_savings * 12
    break_even_months = calculate_break_even(closing_costs, monthly_savings)
    
    total_current_interest = (current_payment * remaining_months) - current_balance
    total_new_interest = (new_payment * new_term_months) - current_balance
    interest_savings = total_current_interest - total_new_interest
    
    total_payment_savings = monthly_savings * remaining_months
    net_savings = total_payment_savings - closing_costs
    
    print_section("REFINANCING ANALYSIS")
    
    print(f"""
  CURRENT LOAN
  ├─ Balance:           {format_currency(current_balance)}
  ├─ Interest Rate:     {current_rate}%
  ├─ Monthly Payment:   {format_currency(current_payment)}
  └─ Time Remaining:    {remaining_years} years

  NEW LOAN
  ├─ Loan Amount:       {format_currency(current_balance)}
  ├─ Interest Rate:     {new_rate}%
  ├─ Monthly Payment:   {format_currency(new_payment)}
  └─ Loan Term:         {new_term_years} years
""")
    
    print_section("SAVINGS BREAKDOWN")
    
    if monthly_savings > 0:
        print(f"""
  Monthly Savings:      {format_currency(monthly_savings)}
  Annual Savings:       {format_currency(annual_savings)}
  
  Closing Costs:        {format_currency(closing_costs)}
  Break-Even Point:     {format_months(break_even_months)}
  
  Total Interest Saved: {format_currency(interest_savings)}
  Net Savings (after closing costs over {remaining_years}yr):
                        {format_currency(net_savings)}
""")
    else:
        print(f"""
  ⚠️  Monthly payment would INCREASE by {format_currency(abs(monthly_savings))}
  
  This refinance does NOT save money on monthly payments.
  
  However, if you're shortening the term, you may still save on total interest:
  Total Interest Difference: {format_currency(interest_savings)}
""")
    
    print_section("📋 RECOMMENDATION")
    
    if monthly_savings <= 0:
        print("""
  ❌ NOT RECOMMENDED based on monthly savings.
  
  Unless you specifically want to shorten your loan term or have
  other strategic reasons, this refinance may not make sense.
""")
    elif break_even_months <= 24:
        print(f"""
  ✅ STRONGLY RECOMMENDED
  
  You'll break even in just {format_months(break_even_months)}!
  After that, you're saving {format_currency(monthly_savings)}/month.
  
  If you plan to stay in the home more than 2 years, this is a great deal.
""")
    elif break_even_months <= 48:
        print(f"""
  ✅ RECOMMENDED (if staying 4+ years)
  
  Break-even period: {format_months(break_even_months)}
  
  This makes sense if you plan to stay in the home at least 4 years.
  The longer you stay, the more you save.
""")
    elif break_even_months <= 84:
        print(f"""
  ⚠️  CONSIDER CAREFULLY
  
  Break-even period: {format_months(break_even_months)}
  
  This only makes sense if you're confident you'll stay in the home
  for at least {int(break_even_months // 12) + 1} years.
""")
    else:
        print(f"""
  ❌ PROBABLY NOT WORTH IT
  
  Break-even period: {format_months(break_even_months)}
  
  The savings are too small relative to closing costs.
  Consider negotiating lower closing costs or waiting for a better rate.
""")
    
    print("=" * 60)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Cancelled. Goodbye! 👋\n")

