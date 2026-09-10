import streamlit as st

import cartin_bank_auth
import cartin_bank_storage
import cartin_bank_transactions
import cartin_bank_analysis
import cartin_bank_utils


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Cartin Bank",
    page_icon="🏦",
    layout="wide"
)


# ==========================================
# CUSTOM STYLING
# ==========================================

st.markdown("""
<style>
    /* Overall banking color palette */
    :root {
        --bank-navy: #0B2545;
        --bank-blue: #13315C;
        --bank-gold: #C9A227;
        --bank-green: #1B7A3D;
        --bank-red: #B3261E;
    }

    /* Main title styling */
    h1 {
        color: #0B2545;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #0B2545;
    }
    section[data-testid="stSidebar"] * {
        color: #F5F5F5 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15);
    }

    /* Buttons */
    div.stButton > button {
        background-color: #0B2545;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6em 1.2em;
        font-weight: 600;
        transition: background-color 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #C9A227;
        color: #0B2545;
    }

    /* Metric cards */
div[data-testid="stMetric"] {
    background-color: #F4F6F9;
    border: 1px solid #DDE3EC;
    border-radius: 10px;
    padding: 14px 16px;
}

div[data-testid="stMetric"] label,
div[data-testid="stMetricLabel"] {
    color: #0B2545 !important;
}

div[data-testid="stMetricValue"] {
    color: #0B2545 !important;
}

    /* Section dividers */
    hr {
        margin: 1.2em 0;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account" not in st.session_state:
    st.session_state.account = None


# ==========================================
# BANK HEADER / BRANDING
# ==========================================

header_col1, header_col2 = st.columns([1, 6])

with header_col1:
    st.markdown("<div style='font-size: 52px; text-align:center;'>🏦</div>", unsafe_allow_html=True)

with header_col2:
    st.title("Cartin Bank")
    st.caption("Secure Digital Banking System  •  Member FDIC-style protection  •  Est. 2026")

st.divider()


# ==========================================
# LOGIN / REGISTRATION
# ==========================================

if not st.session_state.logged_in:

    # Center the auth card in the page
    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown("### 👋 Welcome to Cartin Bank")
        st.caption("Log in to manage your account, or register to get started.")

        login_tab, register_tab = st.tabs(["🔑 Login", "📝 Register"])

        # ======================================
        # LOGIN
        # ======================================

        with login_tab:

            st.subheader("Welcome Back")

            account_number = st.text_input(
                "Account Number",
                key="login_account",
                placeholder="e.g. 100234"
            )

            pin = st.text_input(
                "PIN",
                type="password",
                key="login_pin",
                placeholder="4-digit PIN"
            )

            if st.button("Login", use_container_width=True):

                account, message = cartin_bank_auth.login_account(
                    account_number, pin
                )

                if account is not None:
                    st.session_state.logged_in = True
                    st.session_state.account = account
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

        # ======================================
        # REGISTRATION
        # ======================================

        with register_tab:

            st.subheader("Create Your Cartin Bank Account")

            name = st.text_input("Full Name", key="register_name", placeholder="Juan Dela Cruz")
            account_number = st.text_input("Account Number", key="register_account", placeholder="Choose a unique number")

            pin_col, confirm_col = st.columns(2)
            with pin_col:
                pin = st.text_input("Create 4-Digit PIN", type="password", key="register_pin")
            with confirm_col:
                confirm_pin = st.text_input("Confirm PIN", type="password", key="register_confirm_pin")

            account_type = st.selectbox(
                "Account Type",
                ["Savings Account", "Student Account", "Business Account"]
            )

            starting_balance = st.number_input(
                "Starting Balance", min_value=0.0, step=100.0, format="%.2f"
            )

            if st.button("Create Account", use_container_width=True):

                account, message = cartin_bank_auth.register_account(
                    name, account_number, pin, confirm_pin,
                    account_type, starting_balance
                )

                if account is not None:
                    st.success(message)
                    st.info("Your account has been created. Please use the Login tab.")
                else:
                    st.error(message)


# ==========================================
# LOGGED-IN BANKING APPLICATION
# ==========================================

else:

    account = st.session_state.account

    # ======================================
    # SIDEBAR
    # ======================================

    st.sidebar.markdown("## 🏦 Cartin Bank")
    st.sidebar.markdown(f"### {account.account_name}")
    st.sidebar.caption(f"🪪 {account.get_account_type()}")
    st.sidebar.caption(f"# {account.account_number}")

    st.sidebar.divider()

    menu = st.sidebar.radio(
        "BANKING MENU",
        [
            "🏠 Dashboard",
            "💵 Deposit",
            "💸 Withdraw",
            "🔄 Transfer Money",
            "🔒 Change PIN",
            "🎯 Savings Goal",
            "📜 Transaction History",
            "📊 Transaction Analysis"
        ]
    )

    st.sidebar.divider()

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.account = None
        st.rerun()


    # ======================================
    # DASHBOARD
    # ======================================

    if menu == "🏠 Dashboard":

        st.header(f"Welcome back, {account.account_name} 👋")
        st.caption("Here's a snapshot of your account.")

        col1, col2, col3 = st.columns(3)

        col1.metric("💰 Current Balance", cartin_bank_utils.format_currency(account.check_balance()))
        col2.metric("🪪 Account Type", account.get_account_type())
        col3.metric("# Account Number", account.account_number)

        st.divider()
        st.info("Select a banking service from the menu on the left to get started.")


    # ======================================
    # DEPOSIT
    # ======================================

    elif menu == "💵 Deposit":

        st.header("💵 Deposit Money")
        st.write(f"Current Balance: **{cartin_bank_utils.format_currency(account.check_balance())}**")
        st.divider()

        amount = st.number_input("Deposit Amount", min_value=0.0, step=100.0, format="%.2f")

        if st.button("Confirm Deposit", use_container_width=True):

            if not cartin_bank_utils.is_valid_amount(amount):
                st.error("Invalid deposit amount.")
            else:
                success = account.deposit(amount)

                if success:
                    cartin_bank_storage.update_account(account)
                    cartin_bank_transactions.record_transaction(account, "Deposit", amount)
                    st.success("Deposit successful. ✅")
                    st.metric("New Balance", cartin_bank_utils.format_currency(account.check_balance()))


    # ======================================
    # WITHDRAW
    # ======================================

    elif menu == "💸 Withdraw":

        st.header("💸 Withdraw Money")
        st.write(f"Available Balance: **{cartin_bank_utils.format_currency(account.check_balance())}**")
        st.divider()

        amount = st.number_input("Withdrawal Amount", min_value=0.0, step=100.0, format="%.2f")

        if st.button("Confirm Withdrawal", use_container_width=True):

            if not cartin_bank_utils.is_valid_amount(amount):
                st.error("Invalid withdrawal amount.")
            elif amount > account.check_balance():
                st.error("Insufficient balance.")

            else:
                today_total = cartin_bank_transactions.get_today_withdrawal_total(account.account_number)

                if (today_total + amount) > cartin_bank_utils.DAILY_WITHDRAWAL_LIMIT:
                    remaining = cartin_bank_utils.DAILY_WITHDRAWAL_LIMIT - today_total
                    st.error(f"Daily withdrawal limit exceeded. You can withdraw up to {cartin_bank_utils.format_currency(remaining)} more today.")
                else:
                    success = account.withdraw(amount)

                    if success:
                        cartin_bank_storage.update_account(account)
                        cartin_bank_transactions.record_transaction(account, "Withdraw", amount)
                        st.success("Withdrawal successful. ✅")
                        st.metric("New Balance", cartin_bank_utils.format_currency(account.check_balance()))

    # ======================================
    # TRANSFER MONEY
    # ======================================

    elif menu == "🔄 Transfer Money":

        st.header("🔄 Transfer Money")
        st.write(f"Available Balance: **{cartin_bank_utils.format_currency(account.check_balance())}**")
        st.divider()

        recipient_number = st.text_input("Recipient Account Number")
        amount = st.number_input("Transfer Amount", min_value=0.0, step=100.0, format="%.2f")

        if st.button("Confirm Transfer", use_container_width=True):

            recipient_number = recipient_number.strip()

            if recipient_number == "":
                st.error("Please enter a recipient account number.")

            elif recipient_number == account.account_number:
                st.error("You cannot transfer money to your own account.")

            elif not cartin_bank_utils.is_valid_amount(amount):
                st.error("Invalid transfer amount.")

            elif amount > account.check_balance():
                st.error("Insufficient balance.")

            else:
                recipient = cartin_bank_storage.find_account(recipient_number)

                if recipient is None:
                    st.error("Recipient account not found.")

                else:
                    if account.withdraw(amount):

                        recipient.deposit(amount)

                        cartin_bank_storage.update_account(account)
                        cartin_bank_storage.update_account(recipient)

                        cartin_bank_transactions.record_transaction(account, "Transfer Out", amount)
                        cartin_bank_transactions.record_transaction(recipient, "Transfer In", amount)

                        st.success(f"₱{amount:,.2f} sent to {recipient.account_name} successfully. ✅")
                        st.metric("New Balance", cartin_bank_utils.format_currency(account.check_balance()))

                        receipt = cartin_bank_utils.generate_receipt(account, "Transfer Out", amount, account.check_balance())
                        st.download_button("📄 Download E-Receipt", receipt, file_name="transfer_receipt.txt")

                    else:
                        st.error("Transfer failed.")

    # ======================================
    # CHANGE PIN
    # ======================================


    elif menu == "🔒 Change PIN":

        st.header("🔒 Change PIN")
        st.caption("Update your 4-digit PIN for account security.")
        st.divider()

        current_pin = st.text_input("Current PIN", type="password", key="change_current_pin")
        new_pin = st.text_input("New PIN", type="password", key="change_new_pin")
        confirm_new_pin = st.text_input("Confirm New PIN", type="password", key="change_confirm_pin")

        if st.button("Update PIN", use_container_width=True):

            if not account.verify_pin(current_pin):
                st.error("Current PIN is incorrect.")

            elif not cartin_bank_auth.validate_pin(new_pin):
                st.error("New PIN must contain exactly 4 digits.")

            elif new_pin != confirm_new_pin:
                st.error("PIN confirmation does not match.")

            else:
                account.set_pin(new_pin)
                cartin_bank_storage.update_account(account)
                st.success("PIN updated successfully. ✅")

    # ======================================
    # SAVINGS GOAL
    # ======================================


    elif menu == "🎯 Savings Goal":

        st.header("🎯 Savings Goal")
        st.caption("Set a target and track your progress toward it.")
        st.divider()

        current_goal = account.get_savings_goal()

        if current_goal > 0:
            progress = min(account.check_balance() / current_goal, 1.0)
            st.write(f"Goal: **{cartin_bank_utils.format_currency(current_goal)}**")
            st.progress(progress)
            st.caption(f"{progress * 100:.1f}% reached — {cartin_bank_utils.format_currency(account.check_balance())} of {cartin_bank_utils.format_currency(current_goal)}")
        else:
            st.info("You haven't set a savings goal yet.")

        st.divider()

        new_goal = st.number_input("Set New Savings Goal", min_value=0.0, step=500.0, format="%.2f")

        if st.button("Save Goal", use_container_width=True):

            if account.set_savings_goal(new_goal):
                cartin_bank_storage.update_account(account)
                st.success("Savings goal updated. ✅")
                st.rerun()
            else:
                st.error("Savings goal must be greater than zero.")


    # ======================================
    # TRANSACTION HISTORY
    # ======================================

    elif menu == "📜 Transaction History":

        st.header("📜 Transaction History")

        transactions = cartin_bank_transactions.get_transactions()
        transactions = [t for t in transactions if t.get("account_number") == account.account_number]

        if transactions:
            display_data = []
            for t in transactions:
                display_data.append({
                    "Timestamp": t.get("timestamp", "N/A"),
                    "Transaction": t.get("transaction", "N/A"),
                    "Amount": cartin_bank_utils.format_currency(t.get("amount", 0)),
                    "Balance After": cartin_bank_utils.format_currency(t.get("balance_after", 0))
                })

            st.dataframe(display_data, use_container_width=True, hide_index=True)
        else:
            st.info("No transaction history available.")


    # ======================================
    # TRANSACTION ANALYSIS
    # ======================================

    elif menu == "📊 Transaction Analysis":

        st.header("📊 Transaction Analysis")

        result = cartin_bank_analysis.analyze_transactions(account.account_number)

        st.subheader("1. Transaction Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Transactions", result["total_transactions"])
        col2.metric("Deposits", result["deposits"])
        col3.metric("Withdrawals", result["withdrawals"])

        st.divider()

        st.subheader("2. Money Flow Analysis")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Deposited", cartin_bank_utils.format_currency(result["total_deposited"]))
        col2.metric("Total Withdrawn", cartin_bank_utils.format_currency(result["total_withdrawn"]))
        col3.metric("Net Cash Flow", cartin_bank_utils.format_currency(result["net_cash_flow"]))

        st.divider()

        st.subheader("3. Account Activity Analysis")
        col1, col2, col3 = st.columns(3)
        col1.metric("Largest Transaction", cartin_bank_utils.format_currency(result["largest_transaction"]))
        col2.metric("Average Transaction", cartin_bank_utils.format_currency(result["average_transaction"]))
        col3.metric("Latest Transaction", result["latest_transaction"])

        st.caption(f"Latest Activity: {result['latest_timestamp']}")


"""
######### Learning Signature #########
Programmed by: Art Rian F. Cartin
Date Submitted: September 10, 2026

Program Description: This program displays the account information.
Reflection: I learned how to use variables, f-strings, comparison operators, and if/else.

AI Usage
[ ] No AI Assistance – Completed independently without AI.
[Y] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[Y] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""