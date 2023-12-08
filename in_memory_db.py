class InMemoryDB:
    def __init__(self):
        self.main_db = {}
        self.transaction_db = {}
        self.in_transaction = False

    def begin_transaction(self):
        if self.in_transaction:
            raise Exception("Transaction already in progress")
        self.in_transaction = True
        self.transaction_db = self.main_db.copy()

    def put(self, key, value):
        if not self.in_transaction:
            raise Exception("No transaction in progress")
        self.transaction_db[key] = value

    def get(self, key):
        # Changes are not visible until they are committed
        return self.main_db.get(key, None)

    def commit(self):
        if not self.in_transaction:
            raise Exception("No transaction to commit")
        self.main_db = self.transaction_db.copy()
        self.in_transaction = False

    def rollback(self):
        if not self.in_transaction:
            raise Exception("No transaction to rollback")
        self.transaction_db = {}
        self.in_transaction = False

# Example usage
if __name__ == "__main__":
    db = InMemoryDB()
    try:
        print(db.get("A"))  # Should return None
        db.put("A", 5)  # Should raise an error
    except Exception as e:
        print(f"Error: {e}")

    db.begin_transaction()
    db.put("A", 5)
    print(db.get("A"))  # Should return none
    db.put("A", 6)
    db.commit()
    print(db.get("A"))  # Should return 6 after commit
    try:
        db.commit()
    except Exception as e:
        print(f"Error: {e}")
    try:
        db.rollback()
    except Exception as e:
        print(f"Error: {e}")
    print(db.get("B"))  # Should return None
    db.begin_transaction()
    db.put("B", 10)
    db.rollback()
    print(db.get("B"))  # Should return None after rollback

