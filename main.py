from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Dict, Any

# Token types for lexical analysis
class TokenType(Enum):
    TEXT = auto()
    VARIABLE = auto()
    BLOCK_START = auto()
    BLOCK_END = auto()

@dataclass
class Token:
    type: TokenType
    value: str

class Lexer:
    def __init__(self, template: str):
        self.template = template
        self.pos = 0
        self.tokens = []

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.template):
            if self.template[self.pos:self.pos+2] == '{{':
                self.tokens.append(Token(TokenType.BLOCK_START, '{{'))
                self.pos += 2
                continue
            elif self.template[self.pos:self.pos+2] == '}}':
                self.tokens.append(Token(TokenType.BLOCK_END, '}}'))
                self.pos += 2
                continue
            
            # Handle variable or text
            current_text = ''
            while self.pos < len(self.template):
                if self.template[self.pos:self.pos+2] in ['{{', '}}']:
                    break
                current_text += self.template[self.pos]
                self.pos += 1
            
            if current_text:
                self.tokens.append(Token(TokenType.TEXT, current_text))

        return self.tokens

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> List[dict]:
        ast = []
        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            
            if token.type == TokenType.TEXT:
                ast.append({'type': 'text', 'value': token.value})
            elif token.type == TokenType.BLOCK_START:
                self.pos += 1
                variable_token = self.tokens[self.pos]
                ast.append({'type': 'variable', 'value': variable_token.value.strip()})
                self.pos += 1  # Skip the BLOCK_END
            
            self.pos += 1
        return ast

class Renderer:
    def render(self, ast: List[dict], context: Dict[str, Any]) -> str:
        output = []
        for node in ast:
            if node['type'] == 'text':
                output.append(node['value'])
            elif node['type'] == 'variable':
                value = context.get(node['value'], '')
                output.append(str(value))
        return ''.join(output)

class TemplateEngine:
    def __init__(self):
        self.cache = {}

    def render(self, template: str, context: Dict[str, Any]) -> str:
        # Lexical analysis
        lexer = Lexer(template)
        tokens = lexer.tokenize()

        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()

        # Rendering
        renderer = Renderer()
        return renderer.render(ast, context)

# Example usage
if __name__ == "__main__":
    template = "Hello {{name}}! Today is {{day}}."
    context = {"name": "John", "day": "Sunday"}
    
    engine = TemplateEngine()
    result = engine.render(template, context)
    print(result)  # Output: Hello John! Today is Sunday.
