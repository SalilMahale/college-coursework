class BloomFilter:
    def __init__(self, size, roll_no):
        self.size = size
        self.roll_no = roll_no
        self.bit_array = [0] * size

    # First hash function
    def hash1(self, x):
        return (self.roll_no * x) % self.size

    # Second hash function
    def hash2(self, x):
        return ((self.roll_no * 2 - 1) * x) % self.size

    # Generate hash details for a word
    def get_hash_details(self, word):
        # Convert each character into ASCII value
        ascii_values = [ord(ch) for ch in word]
        # Apply hash functions to ASCII values
        hash1_values = [self.hash1(x) for x in ascii_values]
        hash2_values = [self.hash2(x) for x in ascii_values]
        # Combine both hash results and remove duplicates
        indexes = sorted(set(hash1_values + hash2_values))
        return ascii_values, hash1_values, hash2_values, indexes

    # Insert a word into the Bloom Filter
    def insert(self, word):
        ascii_values, hash1_values, hash2_values, indexes = self.get_hash_details(word)
        # Set corresponding bits to 1
        for index in indexes:
            self.bit_array[index] = 1
        return ascii_values, hash1_values, hash2_values, indexes

    # Test whether a word is present
    def test_word(self, word, inserted_words):
        ascii_values, hash1_values, hash2_values, indexes = self.get_hash_details(word)
        # Get the bit values at the calculated indexes
        bit_values = [self.bit_array[index] for index in indexes]
        # If all bits are 1, word is possibly present
        is_present = all(value == 1 for value in bit_values)
        # Check actual list to identify false positive
        was_inserted = word in inserted_words
        
        if was_inserted:
            result = "TRUE POSITIVE"
        elif is_present:
            result = "FALSE POSITIVE"
        else:
            result = "NOT PRESENT"
            
        return (
            ascii_values,
            hash1_values,
            hash2_values,
            indexes,
            bit_values,
            result
        )


def main():
    print("=" * 60)
    print("                BLOOM FILTER PROGRAM")
    print("=" * 60)

    # Take Roll Number
    roll_no = int(input("Enter your Roll Number: "))

    # Take Bloom Filter size
    filter_size = int(input("Enter Bloom Filter size: "))

    # Create Bloom Filter
    bloom_filter = BloomFilter(filter_size, roll_no)

    # INSERT WORDS
    print("\n=== ENTER 5 WORDS TO INSERT ===")
    inserted_words = []
    for i in range(5):
        word = input(f"Enter word {i + 1}: ").strip()
        inserted_words.append(word)

    # INSERTING WORDS
    print("\n=== INSERTING WORDS ===")
    print(
        f"{'Word':<12}"
        f"{'ASCII Values':<25}"
        f"{'Hash 1':<25}"
        f"{'Hash 2':<25}"
        f"{'Indexes'}"
    )
    print("-" * 115)
    for word in inserted_words:
        ascii_values, hash1_values, hash2_values, indexes = bloom_filter.insert(word)
        print(
            f"{word:<12}"
            f"{str(ascii_values):<25}"
            f"{str(hash1_values):<25}"
            f"{str(hash2_values):<25}"
            f"{str(indexes)}"
        )

    # FINAL BLOOM FILTER
    print("\n=== FINAL BLOOM FILTER ===")
    print("Indexes: ", list(range(filter_size)))
    print("Bits:    ", bloom_filter.bit_array)

    # TEST WORDS
    print("\n=== ENTER 3 WORDS TO TEST ===")
    test_words = []
    for i in range(3):
        word = input(f"Enter test word {i + 1}: ").strip()
        test_words.append(word)

    # TESTING WORDS
    print("\n=== TESTING WORDS ===")
    test_results = []
    for word in test_words:
        (
            ascii_values,
            hash1_values,
            hash2_values,
            indexes,
            bit_values,
            result
        ) = bloom_filter.test_word(word, inserted_words)

        print("\n" + "-" * 50)
        print("Test Word   :", word)
        print("ASCII Values:", ascii_values)
        print("Hash 1      :", hash1_values)
        print("Hash 2      :", hash2_values)
        print("Indexes     :", indexes)
        print("Bit Values  :", bit_values)
        print("Result      :", result)

        test_results.append((word, ascii_values, indexes, result))

    # FINAL RESULT TABLE
    print("\n=== FINAL RESULT TABLE ===")
    print("-" * 90)
    print(
        f"{'Test Word':<15}"
        f"{'ASCII Values':<30}"
        f"{'Indexes':<25}"
        f"{'Result'}"
    )
    print("-" * 90)
    for word, ascii_values, indexes, result in test_results:
        print(
            f"{word:<15}"
            f"{str(ascii_values):<30}"
            f"{str(indexes):<25}"
            f"{result}"
        )
    print("-" * 90)

    # CONCLUSION
    print("\n=== CONCLUSION ===")
    print("TRUE POSITIVE  : Word was inserted and all required bits are 1.")
    print("FALSE POSITIVE : Word was not inserted, but all required bits are 1.")
    print("NOT PRESENT    : At least one required bit is 0.")


# PROGRAM START
if __name__ == "__main__":
    main()