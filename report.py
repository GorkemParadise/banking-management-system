import random
import re

class Report:
    def __init__(self):
        self.conversation_history = []
        self.knowledge_base = {
            'account': {
                'keywords': ['account', 'open', 'create', 'new', 'make'],
                'responses': [
                    "To open an account, select '(1) Open Account' from the main menu. We have 3 account types: Daily Usage (with 10,000 TL welcome bonus!), Foreign Currency, and Virtual Account.",
                    "When opening a new account, you'll need: last 4 digits of Turkish ID, name, surname, birth date, and a security keyword. This information is important for your security.",
                    "When you open a daily usage account, you get a 10,000 TL welcome bonus! Other account types don't have this bonus."
                ]
            },
            'send money': {
                'keywords': ['send', 'transfer', 'money', 'payment', 'wire'],
                'responses': [
                    "To send money, use '(2) Send Money' option. You'll need the recipient's 10-digit account number and name.",
                    "When sending money, first select your account number, then enter recipient's account number and amount. You'll need to confirm the transaction.",
                    "Money transfer can only be done in TRY. For foreign currency transfer, you need to convert it to TRY first."
                ]
            },
            'payment': {
                'keywords': ['payment', 'bill', 'pay', 'electricity', 'water', 'gas'],
                'responses': [
                    "You can make bill payments from '(3) Payments' menu. Water, electricity, gas, phone and many more payment options available.",
                    "IMPORTANT: Bill payments can ONLY be made from virtual account! You cannot pay bills from daily usage account.",
                    "To make payments, you must first open a virtual account, then transfer money from your daily account to virtual account."
                ]
            },
            'currency': {
                'keywords': ['currency', 'exchange', 'dollar', 'euro', 'gold', 'usd', 'eur', 'forex'],
                'responses': [
                    "For currency exchange, use '(4) Foreign Exchange' menu. You can buy and sell USD, EUR, and gold at current rates.",
                    "To buy currency, you need sufficient TRY balance. When you sell currency, the amount is deposited to your account in TRY.",
                    "Current rates are fetched from real-time API. Gold price is calculated per gram."
                ]
            },
            'password': {
                'keywords': ['password', 'forgot', 'reset', 'change', 'recover'],
                'responses': [
                    "If you forgot your password, use '(4) Forgot Password' option. You'll need your email, user ID, and age for verification.",
                    "To create a strong password, you can use our '(3) Produce Password' feature. It generates secure passwords of any length you want.",
                    "In password reset process, you need to verify your user ID (verification code) first, then your age."
                ]
            },
            'balance': {
                'keywords': ['balance', 'money', 'how much', 'check', 'amount'],
                'responses': [
                    "To view your balance, after logging in, your accounts and balances will be shown in any transaction menu.",
                    "Each of your accounts keeps TRY, USD, EUR, and gold (gram) balances separately.",
                    "To see your total portfolio value, all your currencies are converted to TRY equivalent."
                ]
            },
            'account type': {
                'keywords': ['account type', 'types', 'daily', 'virtual', 'foreign'],
                'responses': [
                    "We have 3 account types: 1) Daily Usage (10,000 TL bonus, for general transactions), 2) Foreign Currency (for forex), 3) Virtual Account (for bill payments - REQUIRED)",
                    "You cannot pay bills from daily usage account! You must open a virtual account for bill payments.",
                    "You can open multiple accounts of each type. Each account has a unique 10-digit number."
                ]
            },
            'security': {
                'keywords': ['security', 'safe', 'secure', 'protection'],
                'responses': [
                    "The security keyword you set when opening account is used for important transactions. Don't share it with anyone!",
                    "Last 4 digits of your Turkish ID are used for account verification.",
                    "Every transaction requires 'yes/no' confirmation. Check the details before confirming."
                ]
            },
            'register': {
                'keywords': ['register', 'signup', 'sign up', 'join', 'create account'],
                'responses': [
                    "To register, use '(2) Register' option. Just enter your email, password, and age.",
                    "When registering, you'll get a unique user ID (e.g., A1234). Save this ID in a safe place!",
                    "After registration, you can open accounts and perform banking operations."
                ]
            },
            'savings': {
                'keywords': ['savings', 'save', 'investment', 'invest', 'tips'],
                'responses': [
                    "For savings tips, use '(5) Savings Tips' menu. You'll find suggestions about gold investment, 50/30/20 rule, and more.",
                    "Experts recommend saving at least 22% of your salary. Creating an emergency fund should be a priority.",
                    "Diversify your portfolio: A distribution like 30% TRY, 30% USD, 40% EUR reduces risk."
                ]
            },
            'problem': {
                'keywords': ['problem', 'error', 'issue', 'not working', 'help', 'trouble'],
                'responses': [
                    "Which operation are you having trouble with? Please explain in detail: opening account, sending money, payment, or currency exchange?",
                    "Common errors: 1) Trying to pay bills without virtual account, 2) Insufficient balance, 3) Wrong account number. Which one applies to you?",
                    "Can you show me the error message? Messages starting with '⚠️' provide important clues."
                ]
            },
            'hello': {
                'keywords': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good day'],
                'responses': [
                    "Hello! Welcome to Paradise Bank AI Assistant. How can I help you? 🏦",
                    "Hello! I'm here to answer your questions about banking operations. What would you like to know?",
                    "Hi! You can ask me anything about Paradise Bank. I'm happy to help! 😊"
                ]
            },
            'thanks': {
                'keywords': ['thanks', 'thank you', 'appreciate', 'helpful'],
                'responses': [
                    "You're welcome! Feel free to ask if you have more questions. 😊",
                    "Not a problem! Glad I could help. Need anything else?",
                    "Anytime! Have a great day. 🌟"
                ]
            },
            'turkce': {
                'keywords': ['sa', 'merhaba', 'naber', 'yardım', 'nasılsın', 'teşekkürler', 'hesap açma', 'para gönderme', 'ödeme', 'döviz', 'şifre', 'problem', 'teşekkür ederim', 'iyi günler', 'iyi akşamlar', 'iyi sabahlar', 'alo', 'para yatırma', 'para çekme'],
                'responses': [
                    " I'm sorry, we do not have Turkish support in our bank. I can assist you in English.",
                    " I apologize, but our services are only available in English at the moment.",
                    " Unfortunately, I can only provide assistance in English. How can I help you today?"
                ]
            }
        }
        
        self.default_responses = [
            "I'd like to help you with this, but I didn't quite understand. Could you provide more details?",
            "Interesting question! Which of these would you like information about: opening account, sending money, payments, currency exchange, or password issues?",
            "To help you better, could you be more specific? For example: 'how to open account?', 'how to send money?'",
            "At Paradise Bank, you can: Open accounts, transfer money, pay bills, exchange currency. Which one would you like to know about?"
        ]
        
        self.faq = {
            'do i need virtual account for bill payment': "Yes! Bill payments can ONLY be made from virtual account. You cannot pay bills from daily usage account. You must open a virtual account first.",
            'is there welcome bonus': "Yes! When you open a daily usage account, you get 10,000 TL welcome bonus. This bonus is automatically credited to your account.",
            'how to buy currency': "To buy currency, log in, select '(4) Foreign Exchange', choose your account, and select the currency type you want to buy. The amount will be deducted from your TRY balance.",
            'i forgot my password what to do': "Use '(4) Forgot Password' option. Enter your email, user ID (verification code), and age to reset your password.",
            'how many account types': "There are 3 account types: Daily Usage (general transactions + 10K bonus), Foreign Currency (forex), Virtual Account (bill payments - required).",
            'how to send money': "Log in, select '(2) Send Money', choose your account, enter recipient's 10-digit account number, enter amount, and confirm.",
            'how many digits account number': "All account numbers are 10 digits and unique. They are automatically generated by the system.",
            'can i open multiple accounts': "Yes! You can open as many accounts as you want from each account type. Each account has separate number and balance."
        }
    
    def normalize_text(self, text):
        text = text.lower()
        # Remove Turkish characters for better matching
        replacements = {
            'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    def find_best_match(self, user_input):
        user_input_normalized = self.normalize_text(user_input)
        
        best_match = None
        max_score = 0
        
        for category, data in self.knowledge_base.items():
            score = 0
            for keyword in data['keywords']:
                keyword_normalized = self.normalize_text(keyword)
                if keyword_normalized in user_input_normalized:
                    score += len(keyword_normalized)  
            
            if score > max_score:
                max_score = score
                best_match = category
        
        return best_match if max_score > 0 else None
    
    def check_faq(self, user_input):
        user_input_normalized = self.normalize_text(user_input)
        
        for question, answer in self.faq.items():
            question_normalized = self.normalize_text(question)
            if question_normalized in user_input_normalized or user_input_normalized in question_normalized:
                return answer
        return None
    
    def generate_response(self, user_input):
        faq_answer = self.check_faq(user_input)
        if faq_answer:
            return faq_answer
        category = self.find_best_match(user_input) 
        if category:
            responses = self.knowledge_base[category]['responses']
            return random.choice(responses)
        else:
            return random.choice(self.default_responses)
    
    def chat(self):
        print("\n" + "="*60)
        print("🤖 PARADISE BANK AI ASSISTANT")
        print("="*60)
        print("Hello! I'm your Paradise Bank AI assistant. How can I help you?")
        print("I can answer questions about banking operations, opening accounts,")
        print("money transfers, and payments. Type 'exit' or 'quit' to leave.")
        print("="*60)
        
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            if self.normalize_text(user_input) in ['exit', 'quit', 'bye', 'goodbye']:
                print("\n🤖 AI: Thank you for choosing Paradise Bank! Have a great day! 👋")
                break
            
            self.conversation_history.append({'user': user_input})
            
            response = self.generate_response(user_input)
            self.conversation_history.append({'bot': response})
            
            print(f"\n🤖 AI: {response}")
            
            if 'problem' in self.normalize_text(user_input) or 'error' in self.normalize_text(user_input):
                print("\n💡 Tip: If the problem continues, please share this information:")
                print("   - Which menu option did you use?")
                print("   - What exactly were you trying to do?")
                print("   - What was the error message you saw?")
    
    def quick_help(self):
        """Quick help menu"""
        print("\n" + "="*60)
        print("📚 PARADISE BANK - QUICK HELP GUIDE")
        print("="*60)
        
        topics = {
            '1': ('Opening Account', [
                "• Select (1) Open Account from main menu",
                "• 3 account types: Daily (10K bonus!), Foreign, Virtual",
                "• Need: last 4 digits of ID, name, surname, birth date",
                "• You can open multiple accounts of each type"
            ]),
            '2': ('Sending Money', [
                "• Select (2) Send Money",
                "• Choose your account number",
                "• Enter recipient's 10-digit account number",
                "• Enter amount and confirm transaction"
            ]),
            '3': ('Bill Payment', [
                "• IMPORTANT: Payments can ONLY be made from virtual account!",
                "• Select (3) Payments menu",
                "• Choose payment type (water, electricity, etc.)",
                "• Enter your virtual account number"
            ]),
            '4': ('Currency Exchange', [
                "• Select (4) Foreign Exchange",
                "• You can buy/sell USD, EUR, or Gold",
                "• Current rates fetched from API",
                "• Need TRY balance to buy currency"
            ]),
            '5': ('Password Operations', [
                "• Forgot password: (4) Forgot Password",
                "• Need email, user ID, and age verification",
                "• Generate strong password: (3) Produce Password",
                "• Creates password of any length you want"
            ])
        }
        
        while True:
            print("\n" + "-"*60)
            print("What topic do you need help with?")
            print("-"*60)
            for key, (title, _) in topics.items():
                print(f"{key}) {title}")
            print("6) Chat with AI Assistant (Advanced Help)")
            print("7) Exit")
            print("-"*60)
            
            choice = input("Your choice: ").strip()
            
            if choice in topics:
                title, content = topics[choice]
                print(f"\n{'='*60}")
                print(f"📖 {title.upper()}")
                print('='*60)
                for line in content:
                    print(line)
                print('='*60)
                
            elif choice == '6':
                self.chat()
                
            elif choice == '7':
                print("\nHave a great day! 👋")
                break
                
            else:
                print("\n⚠️ Invalid choice!")


if __name__ == "__main__":
    ai = Report()
    ai.quick_help()