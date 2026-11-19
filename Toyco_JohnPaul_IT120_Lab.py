from abc import ABC, abstractmethod

# PaymentProcessor Interface
class PaymentProcessor(ABC):

    @abstractmethod
    def pay(self, amount: float):
        pass


# Three Payment Processors
class GCashProcessor(PaymentProcessor):

    def pay(self, amount: float):
        print(f"Processing PHP {amount} via GCash API...")



class CreditCardProcessor(PaymentProcessor):

    def pay(self, amount: float):
        print(f"Processing PHP {amount} via Credit Card Gateway...")

class MayaProcessor(PaymentProcessor):

    def pay(self, amount: float):
        print(f"Processing PHP {amount} via Maya API...")


# PaymentFactory
class PaymentFactory:

    @staticmethod
    def create_processor(method: str) -> PaymentProcessor:

        processors = {
            "gcash": GCashProcessor,
            "creditcard": CreditCardProcessor,
            "maya": MayaProcessor
        }

        processor = processors.get(method.lower())

        if processor is None:
            raise ValueError("Invalid payment method")

        return processor()

# TransactionLogger Interface
class TransactionLogger(ABC):

    @abstractmethod
    def save(self, data: str):
        pass

# PlainTransactionLogger
class PlainTransactionLogger(TransactionLogger):

    def __init__(self):
        self.records = []

    def save(self, data: str):
        print(f"[STORAGE] Saving: {data}")
        self.records.append(data)

# EncryptionDecorator
class EncryptionDecorator(TransactionLogger):

    def __init__(self, wrapped_logger: TransactionLogger):
        self._wrapped = wrapped_logger

    def save(self, data: str):

        encrypted = f"ENC({data[::-1]})"

        print("[DECORATOR] Encrypting transaction...")

        self._wrapped.save(encrypted)

# HistoryAccess Interface
class HistoryAccess(ABC):

    @abstractmethod
    def view_history(self) -> list:
        pass

# RealHistoryAccess
class RealHistoryAccess(HistoryAccess):

    def __init__(self, logger: PlainTransactionLogger):
        self._logger = logger

    def view_history(self) -> list:
        return self._logger.records

# SecureHistoryProxy
class SecureHistoryProxy(HistoryAccess):

    def __init__(self, real_access: RealHistoryAccess, user_role: str):
        self._real_access = real_access
        self._user_role = user_role

    def view_history(self) -> list:

        if self._user_role != "admin":
            raise PermissionError(
                f"Access Denied: '{self._user_role}' cannot view transaction history."
            )

        print("[PROXY] Admin verified. Access granted.")

        return self._real_access.view_history()

# Connect Everything in the Main Program
class CheckoutSystem:

    def __init__(self, logger):
        self.logger = logger

    def process_checkout(self, method: str, amount: float, customer_ssn: str):

        processor = PaymentFactory.create_processor(method)

        processor.pay(amount)

        log_entry = (
            f"Method: {method} | Amount: {amount} | SSN: {customer_ssn}"
        )

        self.logger.save(log_entry)

# MAIN EXECUTION

raw_logger = PlainTransactionLogger()

secure_logger = EncryptionDecorator(raw_logger)

checkout = CheckoutSystem(secure_logger)

# Process Maya payment
checkout.process_checkout("maya", 1500.00, "SSN-998-112")

# Create history access
real_access = RealHistoryAccess(raw_logger)

# Test cashier access
cashier_proxy = SecureHistoryProxy(real_access, "cashier")

try:
    print("\nCashier Transaction History:")
    print(cashier_proxy.view_history())

except PermissionError as e:
    print(e)

# Test admin access
admin_proxy = SecureHistoryProxy(real_access, "admin")

print("\nAdmin Transaction History:")
print(admin_proxy.view_history())