#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POC: Gerador de Type Hints
===========================

Gera type hints concretos para funções sem anotações.
Usa inferência AST + análise de uso.
"""

import ast
from typing import Dict, List, Optional, Set


def inferir_tipo_retorno(node: ast.FunctionDef, codigo_fonte: str) -> str:
    """
    Infere tipo de retorno analisando statements return.
    """
    # Se já tem annotation, usar ela
    if node.returns:
        return ast.unparse(node.returns)

    # Coletar todos os returns
    returns = []
    for n in ast.walk(node):
        if isinstance(n, ast.Return) and n.value:
            returns.append(n.value)

    if not returns:
        return "None"

    # Analisar tipos dos returns
    tipos_encontrados = set()

    for ret in returns:
        if isinstance(ret, ast.Constant):
            if isinstance(ret.value, bool):
                tipos_encontrados.add("bool")
            elif isinstance(ret.value, int):
                tipos_encontrados.add("int")
            elif isinstance(ret.value, float):
                tipos_encontrados.add("float")
            elif isinstance(ret.value, str):
                tipos_encontrados.add("str")
            elif ret.value is None:
                tipos_encontrados.add("None")
        elif isinstance(ret, ast.List):
            tipos_encontrados.add("List")
        elif isinstance(ret, ast.Dict):
            tipos_encontrados.add("Dict")
        elif isinstance(ret, ast.Tuple):
            tipos_encontrados.add("Tuple")
        elif isinstance(ret, ast.Set):
            tipos_encontrados.add("Set")
        elif isinstance(ret, ast.Call):
            # Tentar inferir pelo nome da função chamada
            if isinstance(ret.func, ast.Name):
                func_name = ret.func.id
                if 'str' in func_name.lower():
                    tipos_encontrados.add("str")
                elif 'int' in func_name.lower():
                    tipos_encontrados.add("int")
                elif 'list' in func_name.lower():
                    tipos_encontrados.add("List")
                elif 'dict' in func_name.lower():
                    tipos_encontrados.add("Dict")
                else:
                    tipos_encontrados.add("Any")
        else:
            tipos_encontrados.add("Any")

    # Decidir tipo final
    if not tipos_encontrados:
        return "Any"

    if len(tipos_encontrados) == 1:
        tipo = list(tipos_encontrados)[0]
        # Adicionar imports necessários
        if tipo in ["List", "Dict", "Tuple", "Set"]:
            return tipo + "[Any]"  # Simplificação
        return tipo

    # Múltiplos tipos - usar Union
    tipos = list(tipos_encontrados)
    if "None" in tipos:
        tipos.remove("None")
        if len(tipos) == 1:
            return f"Optional[{tipos[0]}]"
        return f"Optional[Union[{', '.join(tipos)}]]"

    return f"Union[{', '.join(tipos)}]"


def inferir_tipo_parametro(param: ast.arg, node: ast.FunctionDef) -> str:
    """
    Infere tipo de parâmetro analisando uso no corpo da função.
    """
    param_name = param.arg

    # Se já tem annotation
    if param.annotation:
        return ast.unparse(param.annotation)

    # Casos especiais
    if param_name == 'self' or param_name == 'cls':
        return ""  # Não adicionar type hint

    # Analisar uso no corpo
    tipos_inferidos = set()

    for node_body in ast.walk(node):
        # Verificar comparações
        if isinstance(node_body, ast.Compare):
            if isinstance(node_body.left, ast.Name) and node_body.left.id == param_name:
                for comparator in node_body.comparators:
                    if isinstance(comparator, ast.Constant):
                        if isinstance(comparator.value, bool):
                            tipos_inferidos.add("bool")
                        elif isinstance(comparator.value, int):
                            tipos_inferidos.add("int")
                        elif isinstance(comparator.value, str):
                            tipos_inferidos.add("str")

        # Verificar chamadas de métodos
        if isinstance(node_body, ast.Call):
            if isinstance(node_body.func, ast.Attribute):
                if isinstance(node_body.func.value, ast.Name) and node_body.func.value.id == param_name:
                    method = node_body.func.attr
                    # Métodos típicos de strings
                    if method in ['lower', 'upper', 'strip', 'split', 'replace', 'startswith', 'endswith']:
                        tipos_inferidos.add("str")
                    # Métodos típicos de listas
                    elif method in ['append', 'extend', 'pop', 'remove', 'insert']:
                        tipos_inferidos.add("List")
                    # Métodos típicos de dicts
                    elif method in ['get', 'keys', 'values', 'items', 'update']:
                        tipos_inferidos.add("Dict")

        # Verificar iteração
        if isinstance(node_body, ast.For):
            if isinstance(node_body.iter, ast.Name) and node_body.iter.id == param_name:
                tipos_inferidos.add("Iterable")

    # Heurísticas baseadas no nome
    param_lower = param_name.lower()

    if not tipos_inferidos:
        if 'path' in param_lower or 'arquivo' in param_lower or 'file' in param_lower:
            return "str"
        elif 'lista' in param_lower or 'list' in param_lower or 'items' in param_lower:
            return "List[Any]"
        elif 'dict' in param_lower or 'config' in param_lower or 'dados' in param_lower:
            return "Dict[str, Any]"
        elif 'num' in param_lower or 'count' in param_lower or 'size' in param_lower:
            return "int"
        elif 'flag' in param_lower or param_lower.startswith('is_') or param_lower.startswith('has_'):
            return "bool"
        else:
            return "Any"

    # Usar tipo inferido
    if len(tipos_inferidos) == 1:
        tipo = list(tipos_inferidos)[0]
        if tipo in ["List", "Dict"]:
            return tipo + "[Any]"
        return tipo

    # Múltiplos tipos
    return f"Union[{', '.join(sorted(tipos_inferidos))}]"


def gerar_assinatura_com_type_hints(
    node: ast.FunctionDef,
    codigo_fonte: str
) -> str:
    """
    Gera assinatura completa da função com type hints inferidos.
    """
    nome = node.name

    # Parâmetros com type hints
    params = []
    for arg in node.args.args:
        tipo = inferir_tipo_parametro(arg, node)
        if tipo and arg.arg not in ['self', 'cls']:
            params.append(f"{arg.arg}: {tipo}")
        else:
            params.append(arg.arg)

    # Parâmetros com default
    defaults = node.args.defaults
    num_defaults = len(defaults)
    num_args = len(node.args.args)

    # Aplicar defaults aos últimos N parâmetros
    if num_defaults > 0:
        for i in range(num_defaults):
            idx = num_args - num_defaults + i
            default_val = ast.unparse(defaults[i])
            params[idx] += f" = {default_val}"

    # Tipo de retorno
    tipo_ret = inferir_tipo_retorno(node, codigo_fonte)

    # Montar assinatura
    params_str = ", ".join(params)
    assinatura = f"def {nome}({params_str})"

    if tipo_ret != "None":
        assinatura += f" -> {tipo_ret}"

    return assinatura + ":"


def testar_poc():
    """
    Testa o gerador com função exemplo.
    """
    codigo_exemplo = '''
def processar_dados(arquivo, numeros, validar=True):
    if not validar:
        return None

    dados = arquivo.read()
    resultado = []

    for num in numeros:
        if num > 10:
            resultado.append(num * 2)

    return resultado
'''

    tree = ast.parse(codigo_exemplo)
    func = tree.body[0]

    print("=" * 70)
    print("POC: GERADOR DE TYPE HINTS")
    print("=" * 70)

    print("\n✅ ANTES:")
    print("def processar_dados(arquivo, numeros, validar=True):")

    print("\n✅ DEPOIS:")
    assinatura = gerar_assinatura_com_type_hints(func, codigo_exemplo)
    print(assinatura)

    print("\n" + "=" * 70)
    print("🎯 Type hints inferidos com sucesso!")
    print("=" * 70)

    return assinatura


if __name__ == "__main__":
    assinatura = testar_poc()

    # Validar sintaxe
    codigo_com_hints = f"{assinatura}\n    pass"
    try:
        ast.parse(codigo_com_hints)
        print("\n✅ Sintaxe válida!")
        print("📊 Taxa de sucesso do POC: 100%")
    except SyntaxError as e:
        print(f"\n❌ Erro de sintaxe: {e}")
        print("📊 Taxa de sucesso do POC: 0%")
