# peer_to_peer_lending.py

from datetime import datetime, timedelta
import uuid

# Simulate in-memory databases
borrowers = {}
investors = {}
loan_listings = {}
portfolios = {}
repayments = []

# --- Helper Functions ---
def generate_id():
    return str(uuid.uuid4())

# --- Borrower Verification ---
def verify_borrower(name, credit_score):
    if credit_score >= 600:
        borrower_id = generate_id()
        borrowers[borrower_id] = {
            'name': name,
            'credit_score': credit_score,
            'verified': True
        }
        print(f"Borrower {name} verified. ID: {borrower_id}")
        return borrower_id
    else:
        print(f"Borrower {name} not verified (credit score too low).")
        return None

# --- Loan Listing ---
def list_loan(borrower_id, amount, interest_rate, duration_months):
    if borrower_id in borrowers and borrowers[borrower_id]['verified']:
        loan_id = generate_id()
        loan_listings[loan_id] = {
            'borrower_id': borrower_id,
            'amount': amount,
            'interest_rate': interest_rate,
            'duration': duration_months,
            'funded': False,
            'funded_by': None
        }
        print(f"Loan listed: {loan_id} for amount ${amount}")
        return loan_id
    else:
        print("Borrower not verified or does not exist.")
        return None

# --- Investor Portfolio Management ---
def add_investor(name, capital):
    investor_id = generate_id()
    investors[investor_id] = {
        'name': name,
        'capital': capital
    }
    portfolios[investor_id] = []
    print(f"Investor {name} added. ID: {investor_id}")
    return investor_id

def invest(investor_id, loan_id):
    if investor_id in investors and loan_id in loan_listings:
        loan = loan_listings[loan_id]
        investor = investors[investor_id]
        if not loan['funded'] and investor['capital'] >= loan['amount']:
            investor['capital'] -= loan['amount']
            loan['funded'] = True
            loan['funded_by'] = investor_id
            portfolios[investor_id].append(loan_id)
            print(f"Investor {investor['name']} funded loan {loan_id}")
            return True
        else:
            print("Loan already funded or investor lacks capital.")
            return False
    else:
        print("Invalid investor or loan ID.")
        return False

# --- Automated Repayment Processing ---
def process_repayments():
    print("Processing repayments...")
    for loan_id, loan in loan_listings.items():
        if loan['funded']:
            installment = (loan['amount'] * (1 + loan['interest_rate']/100)) / loan['duration']
            repayments.append({
                'loan_id': loan_id,
                'amount': round(installment, 2),
                'date': datetime.now().strftime('%Y-%m-%d')
            })
            print(f"Processed repayment of ${round(installment, 2)} for loan {loan_id}")

# --- Demonstration ---
if __name__ == "__main__":
    # Create and verify a borrower
    borrower_id = verify_borrower("Alice", 700)

    # List a loan
    if borrower_id:
        loan_id = list_loan(borrower_id, 1000, 10, 12)

        # Add investor and fund the loan
        investor_id = add_investor("Bob", 5000)
        if loan_id:
            invest(investor_id, loan_id)

        # Process repayments
        process_repayments()

        # View all repayments
        print("\nRepayment History:")
        for r in repayments:
            print(r)
