import argparse
import json
from Token import Token
from Lexer import Lexer

def token_to_dict(token: Token) -> dict:
    return token.tokenToDict()

def tokenizeFileAndSaveJSON(input_path: str, output_path: str) -> list[Token]:
    token_list = []
    output_data = []
    line_counter = 0

    with open(input_path, 'r') as file:
        lines = file.readlines()

    in_multiline_comment = False

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue
        if stripped.startswith("/*"):
            in_multiline_comment = True
            continue
        if in_multiline_comment:
            if "*/" in stripped:
                in_multiline_comment = False
            continue
        if stripped.startswith("#") or stripped.startswith("//"):
            continue

        try:
            tokenizer = Lexer(stripped, line_counter)
            tokens = tokenizer.tokenize()
            token_list.extend(tokens)
            print(f"[Line {line_counter}] Tokens: {tokens}")
            output_data.append({
                "line": line_counter,
                "tokens": [token_to_dict(tok) for tok in tokens]
            })

        except Exception as e:
            output_data.append({
                "line": line_counter,
                "error": str(e)
            })

        line_counter += 1

    with open(output_path, "w", encoding="utf-8") as out_file:
        json.dump(output_data, out_file, indent=4)

    print(f"\n✅ Tokens salvos em {output_path}")
    return token_list

def main():
    parser = argparse.ArgumentParser(description="Lexer Tokenizer")
    parser.add_argument("--file", required=True, help="Arquivo de entrada com código-fonte")
    parser.add_argument("--save-json", action="store_true", help="Salvar tokens em formato JSON")
    parser.add_argument("--output", default="tokens_output.json", help="Caminho do arquivo de saída JSON (opcional)")
    args = parser.parse_args()

    if args.save_json:
        tokenizeFileAndSaveJSON(args.file, args.output)
    else:
        print("Starting...\n")
        line_number = 0
        with open(args.file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith(("#", "//")):
                    continue
                try:
                    tokenizer = Lexer(line, line_number)
                    tokens = tokenizer.tokenize()
                    print(f"[Line {line_number}] Tokens: {tokens}")
                except Exception as e:
                    print(f"[Line {line_number}] ❌ Error: {e}")
                line_number += 1

if __name__ == '__main__':
    main()
