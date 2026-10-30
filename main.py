import argparse
import logging
import sys
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_contract(contract_code):
    """
    Analyzes smart contract code for potential dead code related to crypto operations.
    This is a simplified example and would need significant expansion for real-world use.

    Args:
        contract_code (str): The smart contract code to analyze.

    Returns:
        list: A list of warnings or findings related to potential dead code.
    """

    findings = []

    # The checks below count mentions in the raw text. That is a rough
    # signal, not a call graph: a name that appears once has no call site
    # besides its own mention, which is worth flagging, but a mention
    # inside a comment or a string counts the same as real code, so the
    # findings are prompts to look, not proof that code is dead.
    if "hashlib.sha256" in contract_code and contract_code.count("hashlib.sha256") <= 1: # example usage condition
        findings.append("Warning: 'hashlib.sha256' is used infrequently, potentially redundant.")

    # Example 2: Check for unused key generation functions.  This is very basic.
    if "rsa.generate_private_key" in contract_code and contract_code.count("rsa.generate_private_key") <=1:
         findings.append("Warning: 'rsa.generate_private_key' function not consistently used, potential optimization opportunity.")

    # Example 3: Check for functions that are defined but never called.
    # This requires more sophisticated parsing and symbol table analysis.
    # Placeholder - would need a proper parser and static analysis.

    return findings



def simulate_vulnerability(contract_code):
    """
    Simulates a potential vulnerability related to crypto operations.
    This is a deliberately simplified example for demonstration purposes only.

    Args:
        contract_code (str): The smart contract code to simulate against.

    Returns:
        bool: True if a vulnerability is detected (simulated), False otherwise.
    """
    try:
        #Insecure comparison example:
        if "==" in contract_code and "hashlib.sha256" in contract_code:
            logging.warning("Potential Vulnerability: Insecure comparison used with hash. Check for timing attacks and collision risks.")
            return True

        # Insecure random number generation
        if "random.random" in contract_code:
            logging.warning("Potential Vulnerability: Insecure random number generation used. Consider using os.urandom or secrets module.")
            return True


        return False

    except Exception as e:
        logging.error(f"Error during vulnerability simulation: {e}")
        return False


def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.

    Returns:
        argparse.ArgumentParser: The argument parser object.
    """
    parser = argparse.ArgumentParser(description="Analyze smart contracts for crypto-related dead code and vulnerabilities.")
    parser.add_argument("contract_file", help="Path to the smart contract file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")
    parser.add_argument("-s", "--simulate", action="store_true", help="Simulate potential vulnerabilities.")
    return parser


def main():
    """
    Main function to drive the crypto dead code analyzer.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logging.info(f"Analyzing contract: {args.contract_file}")

    try:
        with open(args.contract_file, "r") as f:
            contract_code = f.read()

        # Perform dead code analysis
        findings = analyze_contract(contract_code)
        if findings:
            logging.warning("Potential dead code findings:")
            for finding in findings:
                logging.warning(f"  - {finding}")
        else:
            logging.info("No potential dead code found.")


        # Optionally simulate vulnerabilities
        if args.simulate:
            if simulate_vulnerability(contract_code):
                logging.warning("Vulnerability simulation triggered. Review code for weaknesses.")
            else:
                logging.info("Vulnerability simulation did not detect any issues (this does not guarantee security!).")


    except FileNotFoundError:
        logging.error(f"Error: Contract file not found: {args.contract_file}")
        sys.exit(1)
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        sys.exit(1)

    logging.info("Analysis complete.")


if __name__ == "__main__":
    # Earlier versions wrote a bundled example contract to my_contract.sol
    # in the caller's working directory before main() ran, so even a --help
    # call created a file the user never asked for. The tool takes its
    # contract as an argument; it should not manufacture one on the side.
    main()
