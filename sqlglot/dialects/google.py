
from __future__ import annotations
from sqlglot.dialects.dialect import Dialect
from sqlglot import tokens, parser, exp, generator
from sqlglot.tokens import TokenType


class Google(Dialect):
    class Tokenizer(tokens.Tokenizer):
        KEYWORDS = {
            **tokens.Tokenizer.KEYWORDS,
            "DECLARE": TokenType.DECLARE,
        }

    class Parser(parser.Parser):
        STATEMENT_PARSERS = {
            **parser.Parser.STATEMENT_PARSERS,
            TokenType.DECLARE: lambda self: self._parse_declare(),
        }

        def _parse_declare(self) -> exp.DeclareItem:
            var = self._parse_var()
            data_type = self._parse_types()
            return self.expression(exp.DeclareItem, this=var, kind=data_type)

    class Generator(generator.Generator):
        TRANSFORMS = {
            **generator.Generator.TRANSFORMS,
            exp.DeclareItem: lambda self, e: self._declare_sql(e),
        }

        TYPE_MAPPING = {
            **generator.Generator.TYPE_MAPPING,
            exp.DataType.Type.TEXT: "STRING",
        }

        def _declare_sql(self, expression):
            this = self.sql(expression, "this")
            kind = self.sql(expression, "kind")
            return f"DECLARE {this} {kind};"
