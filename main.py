from Parser import Parser
from Tokenizer import tokenizeLine
from Token import Token
from Parser import Parser

def main():
    print("Starting...\n")

    lineNumber = 0
    with open('example.txt', 'r') as file:
        for line in file:
            line = line.strip()

            # Ignore empty or comment lines
            if not line or line.startswith(("#", "//")):
                continue

            try:
                tokens = tokenizeLine(line, lineNumber)
                print(f"[Line {lineNumber}] Tokens: {tokens}")
                Parser(tokens).parse()
                print(f"[Line {lineNumber}] ✅ Parsing OK\n")
            except Exception as e:
                print(f"[Line {lineNumber}] ❌ Error: {e}\n")

            lineNumber += 1

    print("Parsing finished.")

def tokenizeFile() -> list[Token]:
    lineCounter = 0
    tokenList = []
    with open('example.txt', 'r') as file:
        content = file.read()

        for line in content.splitlines():
            #Coments
            if not line.strip():
                continue
            if line.startswith("#"):
                continue
            if line.startswith("//"):
                continue
            if line.startswith("/*") and line.endswith("*/"):
                continue
            if line.startswith("/*"):
                while not line.endswith("*/"):
                    line = file.readline()
                continue
            if line.endswith("*/"):
                continue

            # Tokenize the line
            tokenizedLine = tokenizeLine(line, lineCounter)
            print(tokenizedLine)
            tokenList.extend(tokenizedLine)
            lineCounter += 1

    print(tokenList)
    return tokenList

if __name__ == '__main__':
    main()