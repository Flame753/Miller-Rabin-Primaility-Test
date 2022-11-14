import json
import os

# Performing the module operator with the square and multiply technique .
def square_and_multiply(base:int, exponent:int, mod_num:int) -> int:
    binary_num = bin(exponent)[3:]  # Converting # into a str binary representation and removing "0b1"
    remainder = base%mod_num
    for bit in binary_num:
        remainder = (remainder**2)%mod_num
        if bit == "1": 
            remainder = (remainder*base)%mod_num
    return remainder

# Find the component for n - 1 = 2^u * r
# fn must be a odd number.
# Were u is the number of trailing zero in the binary represented of n - 1
# r is the integer value without any trailing zeros from n - 1  
def find_components(n:int) -> tuple:
    if n%2 == 0: raise ValueError("The number entered is not a odd number!")
    
    # Find r and u
    d = n - 1
    d_binary = bin(d)
    reversed_binary = d_binary[::-1]
    u = reversed_binary.find('1')
    r = int(reversed_binary[reversed_binary.find('1'):][::-1], 2)
    return r, u

# It return false if n (the candidate #) is composite and return true if prime. 
# u is the number of trailing zero in the binary represented of n - 1.
# z is the output of the modules n.
def is_likely_prime(n:int, z:int, u:int)-> bool:
    if z != 1 and z != n-1:
        for _ in range(u):
            z_ = (z**2)%n
            if (z_ == 1 and z != 1 and z != (n -1)): return False
            z = z_
        if z_ != 1: return False
    return True

def is_prime(num:int) -> bool:
    for n in range(2,int(num**0.5)+1):
        if num%n==0: return False
    return True

# Returning a dictionary with the list of 'a' value that would make n be a component or prime number.
def miller_test(n:int) -> dict:
    r, u = find_components(n)
    outcome = {"prime_prime": [],
                "composite_prime": [],
                "prime_composite": [],
                "composite_composite": []}
    for a in [num for num in range(2, n-1)]:  # Generate a list of 'a' value between 2 and n-2
        z = square_and_multiply(a, r, n)
        if is_likely_prime(n, z, u):
            if is_prime(n): outcome.get("prime_prime").append(a)  # Must be prime
            else: outcome.get("composite_prime").append(a)  # Error
        else:
            if is_prime(n): outcome.get("prime_composite").append(a)  # Should be impossible
            else: outcome.get("composite_composite").append(a)  # Correct answer
    return outcome

# Calculate a decimal represented for a composite number being a prime.
def how_likely_prime(n:int) -> int:
    # if n <= 1: return f'{0:.3f}'  # Any negative #, 0, 1 are not prime
    if n <= 3: return f'{0:.3f}'  # 2, 3 are prime #'s
    # if n%2 == 0: return f'{0:.3f}'  # Even #'s are not prime
    result = miller_test(n)
    error_percentage = len(result.get("composite_prime"))/(n-3)
    return f'{error_percentage:.3f}'

# A easy way to read and write into a Json file.
class JsonFile:
    def __init__(self, filename) -> None:
        self.filename = filename
    
    def save(self, data):
        with open(self.filename, 'w') as outfile:
            return json.dump(data, outfile, sort_keys=False, indent=4)
    
    def load(self):
        with open(self.filename, 'r') as outfile:
            self.data = json.load(outfile)

def main():
    # Numbers to calculate the decimal represented for a number to be likely prime.
    upper_bound = 30
    lower_bound = 2
    
    # Setting up a location to store the data found
    file = JsonFile("output.json")
    if not os.path.getsize(file.filename):  # Empty File
        file.save({})
    file.load()
    
    error_percentages = []
    # Getting the error percentages
    for n in range(lower_bound, upper_bound + 1):
        if n%2 == 0: continue
        
        # Data was not found in the file then percentage is calculated.
        if not file.data.get(str(n)):
            # A decimal % of a number is likely to be prime
            file.data.update({str(n): how_likely_prime(n)})
        
        n_error_present = float(file.data.get(str(n)))
        # print(n, n_error_present)  # Testing line that show what number the script is on
        
        # Finding the 10 highest error percentages
        if n_error_present >= 0.001:
            error_percentages.append((n, n_error_present))
            
        
    file.save(file.data)
    errors_sorted = sorted(error_percentages, key=lambda pair: pair[1], reverse=True) # Sorting from greatest to smallest percentage
    print(f"{'n':5}: error percentage")
    for pair in errors_sorted[:10]: 
        print(f"{pair[0]}: {pair[1]}")
        
if __name__ == "__main__":
    main()