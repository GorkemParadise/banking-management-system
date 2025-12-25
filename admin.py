import json
import os
from datetime import datetime

class Admin:
    def __init__(self, data_file='data.json', history_file='history.json', user_file='user_data.json'):
        self.data_file = data_file
        self.history_file = history_file
        self.user_file = user_file
        self.admin_password = "admin123"  
    
    def load_accounts(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def load_users(self):
        if os.path.exists(self.user_file):
            with open(self.user_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        return {}
    
    def authenticate(self):
        """Admin girişi"""
        print("\n" + "="*50)
        print("🔐 ADMIN AUTHENTICATION")
        print("="*50)
        password = input("Enter admin password: ").strip()
        
        if password == self.admin_password:
            print("✅ Authentication successful!")
            return True
        else:
            print("⚠️ Invalid password!")
            return False
    
    def admin_panel(self):
        """Ana admin paneli"""
        if not self.authenticate():
            return
        
        while True:
            print("\n" + "="*50)
            print("👑 ADMIN PANEL - Paradise Bank")
            print("="*50)
            print("1) View User Account Info")
            print("2) View Transaction History")
            print("3) View All Users")
            print("4) Search User by Email")
            print("5) System Statistics")
            print("6) Exit Admin Panel")
            print("="*50)
            
            choice = input("Select option: ").strip()
            
            if choice == "1":
                self.view_account_info()
            elif choice == "2":
                self.view_transaction_history()
            elif choice == "3":
                self.view_all_users()
            elif choice == "4":
                self.search_user()
            elif choice == "5":
                self.system_statistics()
            elif choice == "6":
                print("👋 Exiting admin panel...")
                break
            else:
                print("⚠️ Invalid option!")
    
    def view_account_info(self):
        print("\n" + "="*50)
        print("📊 VIEW ACCOUNT INFORMATION")
        print("="*50)
        
        account_number = input("Enter account number (10 digits): ").strip()
        
        accounts = self.load_accounts()
        users = self.load_users()
        
        found = False
        for email, data in accounts.items():
            if account_number in data.get('accounts', {}):
                found = True
                account_data = data['accounts'][account_number]
                personal_info = data.get('personal_info', {})
                
                # Kullanıcı temel bilgileri
                user_basic = users.get(email, {})
                
                print("\n" + "-"*50)
                print("👤 USER INFORMATION")
                print("-"*50)
                print(f"Email: {email}")
                print(f"User ID: {user_basic.get('id', 'N/A')}")
                print(f"Age: {user_basic.get('age', 'N/A')}")
                
                print("\n" + "-"*50)
                print("🏦 PERSONAL BANKING INFO")
                print("-"*50)
                print(f"Name: {personal_info.get('name', 'N/A')} {personal_info.get('surname', 'N/A')}")
                print(f"Birth Date: {personal_info.get('birth_date', 'N/A')}")
                print(f"TC Last 4 Digits: {personal_info.get('tc_last_four', 'N/A')}")
                print(f"Security Keyword: {personal_info.get('keyword', 'N/A')}")
                
                print("\n" + "-"*50)
                print("💰 ACCOUNT DETAILS")
                print("-"*50)
                print(f"Account Number: {account_number}")
                print(f"Account Type: {account_data.get('type', 'N/A')}")
                print(f"Created At: {account_data.get('created_at', 'N/A')}")
                
                print("\n" + "-"*50)
                print("💵 BALANCE INFORMATION")
                print("-"*50)
                print(f"TRY Balance: {account_data.get('balance_try', 0):.2f} TL")
                print(f"USD Balance: {account_data.get('balance_usd', 0):.4f} USD")
                print(f"EUR Balance: {account_data.get('balance_eur', 0):.4f} EUR")
                print(f"Gold Balance: {account_data.get('balance_gold', 0):.4f} grams")
                
                total_try = (
                    account_data.get('balance_try', 0) +
                    account_data.get('balance_usd', 0) * 34.50 +
                    account_data.get('balance_eur', 0) * 37.20 +
                    account_data.get('balance_gold', 0) * 2850
                )
                print(f"\n💎 Total Portfolio Value: ~{total_try:.2f} TL")
                print("-"*50)
                
                break
        
        if not found:
            print("⚠️ Account number not found!")
    
    def view_transaction_history(self):
        print("\n" + "="*50)
        print("📜 VIEW TRANSACTION HISTORY")
        print("="*50)
        
        account_number = input("Enter account number (10 digits): ").strip()
        
        accounts = self.load_accounts()
        history = self.load_history()

        account_email = None
        for email, data in accounts.items():
            if account_number in data.get('accounts', {}):
                account_email = email
                break
        
        if not account_email:
            print("⚠️ Account number not found!")
            return
        
        relevant_transactions = []
        for transaction in history:
            if transaction.get('user') == account_email:
                details = transaction.get('details', {})
                if (details.get('account_number') == account_number or
                    details.get('account') == account_number or
                    details.get('from_account') == account_number or
                    details.get('to_account') == account_number):
                    relevant_transactions.append(transaction)
        
        if not relevant_transactions:
            print(f"\n⚠️ No transactions found for account {account_number}")
            return
        
        print(f"\n📊 Transactions for Account: {account_number}")
        print(f"Account Owner: {account_email}")
        print("-"*50)
        
        for i, trans in enumerate(relevant_transactions, 1):
            print(f"\n[{i}] Transaction Type: {trans.get('type', 'N/A')}")
            print(f"    Timestamp: {trans.get('timestamp', 'N/A')}")
            print(f"    Details:")
            
            details = trans.get('details', {})
            for key, value in details.items():
                print(f"      • {key}: {value}")
            print("-"*50)
        
        print(f"\nTotal Transactions: {len(relevant_transactions)}")
    
    def view_all_users(self):
        """Tüm kullanıcıları listele"""
        print("\n" + "="*50)
        print("👥 ALL REGISTERED USERS")
        print("="*50)
        
        users = self.load_users()
        accounts = self.load_accounts()
        
        if not users:
            print("⚠️ No users registered yet!")
            return
        
        print(f"\nTotal Users: {len(users)}\n")
        
        for i, (email, user_data) in enumerate(users.items(), 1):
            print(f"[{i}] {email}")
            print(f"    ID: {user_data.get('id', 'N/A')}")
            print(f"    Age: {user_data.get('age', 'N/A')}")
            
            user_accounts = accounts.get(email, {}).get('accounts', {})
            print(f"    Accounts: {len(user_accounts)}")
            
            if user_accounts:
                print(f"    Account Numbers:")
                for acc_num, acc_data in user_accounts.items():
                    print(f"      • {acc_num} ({acc_data.get('type', 'N/A')})")
            
            print("-"*50)
    
    def search_user(self):
        """Email'e göre kullanıcı ara"""
        print("\n" + "="*50)
        print("🔍 SEARCH USER BY EMAIL")
        print("="*50)
        
        email = input("Enter user email: ").strip()
        
        users = self.load_users()
        accounts = self.load_accounts()
        
        if email not in users:
            print("⚠️ User not found!")
            return
        
        user_data = users[email]
        account_data = accounts.get(email, {})
        
        print("\n" + "-"*50)
        print("👤 USER INFORMATION")
        print("-"*50)
        print(f"Email: {email}")
        print(f"User ID: {user_data.get('id', 'N/A')}")
        print(f"Age: {user_data.get('age', 'N/A')}")
        
        user_accounts = account_data.get('accounts', {})
        
        if user_accounts:
            print("\n" + "-"*50)
            print("🏦 USER ACCOUNTS")
            print("-"*50)
            
            for acc_num, acc_info in user_accounts.items():
                print(f"\nAccount: {acc_num}")
                print(f"  Type: {acc_info.get('type', 'N/A')}")
                print(f"  TRY: {acc_info.get('balance_try', 0):.2f} TL")
                print(f"  USD: {acc_info.get('balance_usd', 0):.4f}")
                print(f"  EUR: {acc_info.get('balance_eur', 0):.4f}")
                print(f"  Gold: {acc_info.get('balance_gold', 0):.4f} grams")
                print(f"  Created: {acc_info.get('created_at', 'N/A')}")
        else:
            print("\n⚠️ User has no bank accounts yet.")
        
        print("-"*50)
    
    def system_statistics(self):
        """Sistem istatistikleri"""
        print("\n" + "="*50)
        print("📈 SYSTEM STATISTICS")
        print("="*50)
        
        users = self.load_users()
        accounts = self.load_accounts()
        history = self.load_history()
        
        total_users = len(users)
        total_accounts = sum(len(data.get('accounts', {})) for data in accounts.values())
        total_transactions = len(history)
        
        account_types = {'daily_usage': 0, 'foreign_currency': 0, 'virtual': 0}
        total_balance_try = 0
        
        for data in accounts.values():
            for acc_data in data.get('accounts', {}).values():
                acc_type = acc_data.get('type', '')
                if acc_type in account_types:
                    account_types[acc_type] += 1
                total_balance_try += acc_data.get('balance_try', 0)
        
        print(f"\n👥 Total Users: {total_users}")
        print(f"🏦 Total Accounts: {total_accounts}")
        print(f"📊 Total Transactions: {total_transactions}")
        
        print("\n" + "-"*50)
        print("ACCOUNT TYPES")
        print("-"*50)
        print(f"Daily Usage Accounts: {account_types['daily_usage']}")
        print(f"Foreign Currency Accounts: {account_types['foreign_currency']}")
        print(f"Virtual Accounts: {account_types['virtual']}")
        
        print("\n" + "-"*50)
        print("FINANCIAL OVERVIEW")
        print("-"*50)
        print(f"Total TRY in System: {total_balance_try:.2f} TL")
        
        if total_accounts > 0:
            avg_balance = total_balance_try / total_accounts
            print(f"Average Account Balance: {avg_balance:.2f} TL")
        
        print("="*50)