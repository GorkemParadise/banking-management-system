import json
import os
import random
from datetime import datetime
import requests

class BankAccount:
    def __init__(self, data_file='data.json', history_file='history.json'):
        self.data_file = data_file
        self.history_file = history_file
    
    def load_accounts(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_accounts(self, accounts):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(accounts, indent=4, fp=f, ensure_ascii=False)
    
    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_history(self, history):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, indent=4, fp=f, ensure_ascii=False)
    
    def add_to_history(self, user_email, transaction_type, details):
        history = self.load_history()
        history.append({
            'user': user_email,
            'type': transaction_type,
            'details': details,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        self.save_history(history)
    
    def generate_account_number(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(10)])
    
    def get_exchange_rates(self):
        try:
            # Döviz için API
            response = requests.get('https://api.exchangerate-api.com/v4/latest/TRY')
            data = response.json()
            
            # TL cinsinden kurlar
            usd_to_try = 1 / data['rates']['USD']
            eur_to_try = 1 / data['rates']['EUR']
            
            gold_per_gram = 2850.0  # Sabit gram altın fiyatı
            
            return {
                'USD': round(usd_to_try, 2),
                'EUR': round(eur_to_try, 2),
                'GOLD': gold_per_gram
            }
        except:
            # Hata durumunda sabit kurlar
            return {
                'USD': 34.50,
                'EUR': 37.20,
                'GOLD': 2850.0
            }
    
    def open_account(self, user_email):
        print("\n=== OPEN ACCOUNT ===")
        print("1) Daily Account")
        print("2) Foreign Currency Account")
        print("3) Virtual Account")
        
        account_type = input("Select account type: ").strip()
        
        type_map = {
            '1': 'daily_usage',
            '2': 'foreign_currency',
            '3': 'virtual'
        }
        
        if account_type not in type_map:
            print("⚠️ Invalid account type!")
            return None
        
        # Bilgi alma
        print("\nPlease provide the following information:")
        tc_last_four = input("Last 4 number of Turkish ID: ").strip()
        name = input("Name: ").strip()
        surname = input("Surname: ").strip()
        birth_date = input("Date of birth (DD/MM/YYYY): ").strip()
        keyword = input("Security keyword: ").strip()
        
        # Hesap verilerini yükleme
        accounts = self.load_accounts()
        
        if user_email not in accounts:
            accounts[user_email] = {
                'personal_info': {
                    'tc_last_four': tc_last_four,
                    'name': name,
                    'surname': surname,
                    'birth_date': birth_date,
                    'keyword': keyword
                },
                'accounts': {}
            }
        
        # Benzersiz hesap numarası oluşturma
        account_number = self.generate_account_number()
        while any(account_number in user['accounts'] for user in accounts.values()):
            account_number = self.generate_account_number()
        
        # Hesap oluşturma
        selected_type = type_map[account_type]
        welcome_bonus = 10000.0 if selected_type == 'daily_usage' else 0.0
        
        accounts[user_email]['accounts'][account_number] = {
            'type': selected_type,
            'balance_try': welcome_bonus,
            'balance_usd': 0.0,
            'balance_eur': 0.0,
            'balance_gold': 0.0,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.save_accounts(accounts)
        
        # Geçmişe ekleme
        self.add_to_history(user_email, 'account_opened', {
            'account_number': account_number,
            'type': selected_type,
            'welcome_bonus': welcome_bonus
        })
        
        print(f"\n✅ Account opened successfully!")
        print(f"Account Number: {account_number}")
        print(f"Account Type: {selected_type}")
        if welcome_bonus > 0:
            print(f"Welcome Bonus: {welcome_bonus} TL")
        
        return account_number
    
    def send_money(self, user_email):
        """Send money to another account"""
        print("\n=== SEND MONEY ===")
        
        accounts = self.load_accounts()
        
        if user_email not in accounts or not accounts[user_email]['accounts']:
            print("⚠️ You don't have any accounts!")
            return
        
        print("\nYour accounts:")
        user_accounts = accounts[user_email]['accounts']
        for acc_num, acc_data in user_accounts.items():
            print(f"  {acc_num} - {acc_data['type']} (Balance: {acc_data['balance_try']} TL)")
        
        sender_account = input("\nSelect your account number: ").strip()
        if sender_account not in user_accounts:
            print("⚠️ Invalid account number!")
            return
        
        recipient_account = input("Enter recipient's account number (10 digits): ").strip()
        recipient_name = input("Enter recipient's name: ").strip()
        amount = input("Enter amount to send (TL): ").strip()
        
        try:
            amount = float(amount)
        except:
            print("⚠️ Invalid amount!")
            return
        
        recipient_found = False
        recipient_email = None
        for email, data in accounts.items():
            if recipient_account in data['accounts']:
                recipient_found = True
                recipient_email = email
                break
        
        if not recipient_found:
            print("⚠️ Recipient account not found!")
            return
        
        if user_accounts[sender_account]['balance_try'] < amount:
            print("⚠️ Insufficient balance!")
            return
        
        # Para transferini onaylama
        print(f"\n--- Transaction Confirmation ---")
        print(f"From: {sender_account}")
        print(f"To: {recipient_account} ({recipient_name})")
        print(f"Amount: {amount} TL")
        confirm = input("Confirm transaction? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print("Transaction cancelled.")
            return
        
        # İşlemi gerçekleştirme
        accounts[user_email]['accounts'][sender_account]['balance_try'] -= amount
        accounts[recipient_email]['accounts'][recipient_account]['balance_try'] += amount
        
        self.save_accounts(accounts)
        
        # Geçmişe ekleme
        self.add_to_history(user_email, 'money_sent', {
            'from_account': sender_account,
            'to_account': recipient_account,
            'recipient_name': recipient_name,
            'amount': amount
        })
        
        self.add_to_history(recipient_email, 'money_received', {
            'from_account': sender_account,
            'to_account': recipient_account,
            'amount': amount
        })
        
        print(f"\n✅ Transaction successful!")
        print(f"New balance: {accounts[user_email]['accounts'][sender_account]['balance_try']} TL")
    
    def payments(self, user_email):
        print("\n=== PAYMENTS ===")
        print("1) Water Bill")
        print("2) Natural Gas Bill")
        print("3) Electricity Bill")
        print("4) Phone Bill")
        print("5) Credit Card Debt")
        print("6) Tax Penalty")
        print("7) Fine")
        print("8) HGS Transactions")
        print("9) Transportation Card")
        print("10) Social Security")
        print("11) Donations")
        print("12) Rent Payment")
        
        payment_type = input("\nSelect payment type: ").strip()
        
        payment_map = {
            '1': 'Water Bill', '2': 'Natural Gas Bill', '3': 'Electricity Bill',
            '4': 'Phone Bill', '5': 'Credit Card Debt', '6': 'Tax Penalty',
            '7': 'Fine', '8': 'HGS', '9': 'Transportation Card',
            '10': 'Social Security', '11': 'Donations', '12': 'Rent'
        }
        
        if payment_type not in payment_map:
            print("⚠️ Invalid payment type!")
            return
        
        company = input(f"Enter company name for {payment_map[payment_type]}: ").strip()
        amount = input("Enter payment amount (TL): ").strip()
        
        try:
            amount = float(amount)
        except:
            print("⚠️ Invalid amount!")
            return
        
        accounts = self.load_accounts()
        
        if user_email not in accounts or not accounts[user_email]['accounts']:
            print("⚠️ You don't have any accounts!")
            return
        
        # Kullanıcının hesaplarını göster - sadece sanal hesap
        print("\nYour accounts:")
        user_accounts = accounts[user_email]['accounts']
        virtual_accounts = {k: v for k, v in user_accounts.items() if v['type'] == 'virtual'}
        
        if not virtual_accounts:
            print("⚠️ You need a virtual account for payments!")
            print("⚠️ This transaction cannot be made from daily usage account.")
            return
        
        for acc_num, acc_data in virtual_accounts.items():
            print(f"  {acc_num} - {acc_data['type']} (Balance: {acc_data['balance_try']} TL)")
        
        account_number = input("\nSelect virtual account number: ").strip()
        
        if account_number not in virtual_accounts:
            print("⚠️ Invalid account or not a virtual account!")
            return
        
        if user_accounts[account_number]['balance_try'] < amount:
            print("⚠️ Insufficient balance in virtual account!")
            return
        
        # Ödemeyi onaylama
        print(f"\n--- Payment Confirmation ---")
        print(f"Type: {payment_map[payment_type]}")
        print(f"Company: {company}")
        print(f"Amount: {amount} TL")
        confirm = input("Confirm payment? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print("Payment cancelled.")
            return
        
        # Ödemeyi gerçekleştirme
        accounts[user_email]['accounts'][account_number]['balance_try'] -= amount
        self.save_accounts(accounts)
        
        # Geçmişe ekleme
        self.add_to_history(user_email, 'payment', {
            'payment_type': payment_map[payment_type],
            'company': company,
            'account': account_number,
            'amount': amount
        })
        
        print(f"\n✅ Payment successful!")
        print(f"New balance: {accounts[user_email]['accounts'][account_number]['balance_try']} TL")
    
    def foreign_currency(self, user_email):
        print("\n=== FOREIGN CURRENCY ===")
        
        # Güncel kurları alma
        rates = self.get_exchange_rates()
        
        print("\nCurrent Exchange Rates:")
        print(f"1 USD = {rates['USD']} TL")
        print(f"1 EUR = {rates['EUR']} TL")
        print(f"1 Gram Gold = {rates['GOLD']} TL")
        
        print("\n1) Buy USD")
        print("2) Buy EUR")
        print("3) Buy Gold")
        print("4) Sell USD")
        print("5) Sell EUR")
        print("6) Sell Gold")
        
        choice = input("\nSelect option: ").strip()
        
        accounts = self.load_accounts()
        
        if user_email not in accounts or not accounts[user_email]['accounts']:
            print("⚠️ You don't have any accounts!")
            return
        
        # Kullanıcının hesaplarını göster
        print("\nYour accounts:")
        user_accounts = accounts[user_email]['accounts']
        for acc_num, acc_data in user_accounts.items():
            print(f"  {acc_num} - {acc_data['type']}")
            print(f"    TRY: {acc_data['balance_try']}")
            print(f"    USD: {acc_data['balance_usd']}")
            print(f"    EUR: {acc_data['balance_eur']}")
            print(f"    Gold: {acc_data['balance_gold']} grams")
        
        account_number = input("\nSelect account number: ").strip()
        
        if account_number not in user_accounts:
            print("⚠️ Invalid account!")
            return
        
        account = user_accounts[account_number]
        
        if choice in ['1', '2', '3']:
            currency_map = {'1': ('USD', rates['USD']), '2': ('EUR', rates['EUR']), '3': ('GOLD', rates['GOLD'])}
            currency, rate = currency_map[choice]
            
            amount_try = input(f"Enter amount in TL to spend: ").strip()
            try:
                amount_try = float(amount_try)
            except:
                print("⚠️ Invalid amount!")
                return
            
            if account['balance_try'] < amount_try:
                print("⚠️ Insufficient TRY balance!")
                return
            
            amount_currency = amount_try / rate
            
            print(f"\nYou will receive: {amount_currency:.4f} {currency}")
            confirm = input("Confirm? (yes/no): ").strip().lower()
            
            if confirm != 'yes':
                print("Transaction cancelled.")
                return
            
            accounts[user_email]['accounts'][account_number]['balance_try'] -= amount_try
            
            if currency == 'USD':
                accounts[user_email]['accounts'][account_number]['balance_usd'] += amount_currency
            elif currency == 'EUR':
                accounts[user_email]['accounts'][account_number]['balance_eur'] += amount_currency
            elif currency == 'GOLD':
                accounts[user_email]['accounts'][account_number]['balance_gold'] += amount_currency
            
            self.save_accounts(accounts)
            
            self.add_to_history(user_email, 'currency_buy', {
                'account': account_number,
                'currency': currency,
                'amount': amount_currency,
                'spent_try': amount_try,
                'rate': rate
            })
            
            print(f"✅ Purchase successful!")
        
        elif choice in ['4', '5', '6']:
            currency_map = {'4': ('USD', rates['USD'], 'balance_usd'), 
                            '5': ('EUR', rates['EUR'], 'balance_eur'), 
                            '6': ('GOLD', rates['GOLD'], 'balance_gold')}
            currency, rate, balance_key = currency_map[choice]
            
            amount_currency = input(f"Enter amount of {currency} to sell: ").strip()
            try:
                amount_currency = float(amount_currency)
            except:
                print("⚠️ Invalid amount!")
                return
            
            if account[balance_key] < amount_currency:
                print(f"⚠️ Insufficient {currency} balance!")
                return
            
            amount_try = amount_currency * rate
            
            print(f"\nYou will receive: {amount_try:.2f} TL")
            confirm = input("Confirm? (yes/no): ").strip().lower()
            
            if confirm != 'yes':
                print("Transaction cancelled.")
                return
            
            accounts[user_email]['accounts'][account_number][balance_key] -= amount_currency
            accounts[user_email]['accounts'][account_number]['balance_try'] += amount_try
            
            self.save_accounts(accounts)
            
            self.add_to_history(user_email, 'currency_sell', {
                'account': account_number,
                'currency': currency,
                'amount': amount_currency,
                'received_try': amount_try,
                'rate': rate
            })
            
            print(f"✅ Sale successful!")
        
        else:
            print("⚠️ Invalid option!")
    
    def savings_tips(self):
        tips = [
            {
                'title': 'Invest in Gold',
                'content': 'Gold has historically been a stable store of value. Consider allocating 10-15% of your portfolio to gold for long-term wealth preservation.'
            },
            {
                'title': 'The 50/30/20 Rule',
                'content': 'Allocate 50% of your income to needs, 30% to wants, and 20% to savings. This balanced approach helps build wealth while enjoying life.'
            },
            {
                'title': 'Save 22% of Monthly Salary',
                'content': 'Financial experts recommend saving at least 22% of your monthly income. This creates a solid emergency fund and investment base.'
            },
            {
                'title': 'Diversify with Foreign Currency',
                'content': 'Protect your savings from currency fluctuations by holding a portion in USD or EUR. A 30/30/40 split between TRY, USD, and EUR can reduce risk.'
            },
            {
                'title': 'Emergency Fund First',
                'content': 'Before investing, build an emergency fund covering 6 months of expenses. This financial cushion protects you from unexpected costs.'
            },
            {
                'title': 'Dollar-Cost Averaging',
                'content': 'Instead of timing the market, invest a fixed amount regularly. This strategy reduces risk and takes advantage of market fluctuations.'
            }
        ]
        
        tip = random.choice(tips)
        
        print("\n" + "="*50)
        print(f"💡 SAVINGS TIP: {tip['title']}")
        print("="*50)
        print(f"\n{tip['content']}")
        print("\n" + "="*50)