#!/usr/bin/python3
# Resolvedor de equações lineares
# Por agora só resolve matrizes quadradas
# TODO: Debugging com lista de instruções
# ATENÇÃO: OU TUDO É FLOAT OU TUDO É FRAÇÂO
# NÃO HÁ SUPORTE PARA TIPOS MISTOS
# TODO: Consertar frações!
# ---- Definições e Funções ----
class Frac:
    """Frações"""
    def __init__(self, numerador: int, denominador: int = 1, sinal: int = None):
        # XOR
        if not sinal:
            self.sinal: int = -1 if ((numerador < 0) ^ (denominador < 0)) else 1
        else:
            self.sinal: int = -1 if sinal < 0 else 1

        self.n: int = abs(numerador)
        self.d: int = abs(denominador)
    def __str__(self):
        return f"{"-" if self.sinal == -1 else ""}{self.n}/{self.d}"
    def __repr__(self):
        return self.__str__()
    def __neg__(self):
        return Frac(self.n, self.d, -self.sinal)
    def inv(self):
        # Lida com consevação de sinais
        return Frac(self.d, self.n, self.sinal)
    def __add__(self, other):
        print(self, "+", other)
        if isinstance(other, Frac):
            valor = other
        elif isinstance(other, int) or isinstance(other, float):
            # Por agora força o float a ser inteiro!
            valor = Frac(int(other))
        else:
            print(f"Tipo inválido: {self} + {other}")
            exit(1)
        
        novo_d = 1
        novo_n = 0

        if valor.d != self.d:
            # Redundante, mas diminui complexidade frações
            novo_d = self.d * valor.d
            novo_n = self.n * (valor.d) * valor.sinal + valor.n * (self.d) * self.sinal
        else:
            novo_d = self.d
            novo_n = self.n * self.sinal + valor.n * valor.sinal
        return Frac(numerador=novo_n,denominador=novo_d)
    def __sub__(self, other):
        return self.__add__(-other)
    def __mul__(self, other):
        print(self, "*", other, end="= ")
        if isinstance(other, Frac):
            valor = other
        elif isinstance(other, int) or isinstance(other, float):
            valor = Frac(int(other))
        else:
            print(f"Tipo inválido: {self} * {other}")
            exit(1)
        
        novo_d = 1
        novo_n = 0

        novo_d = self.d * valor.d
        novo_n = self.n * valor.n * self.sinal * valor.sinal
        print(Frac(numerador=novo_n,denominador=novo_d))
        return Frac(numerador=novo_n,denominador=novo_d)
    def __truediv__(self, other):
        print("S")
        if isinstance(other, Frac):
            valor = other.inv()
        elif isinstance(other, int) or isinstance(other, float):
            # Inverso
            valor = Frac(1, int(other))
        else:
            print(f"Tipo inválido: {self} / {other}")
            exit(1)
        return self.__mul__(valor)
    def __format__(self, format_spec):
        # Por agora só se retorna
        return self.__str__()
    def __round__(self, ndigits=None):
        # Por agora só se retorna
        return self

class Vetor:
    def __init__(self, vet: list):
        self.vet = vet
        self.n = len(vet)
    def __add__(self, valor):
        if isinstance(valor, float) or isinstance(valor, int):
            return Vetor([v + valor for v in self.vet])
        elif isinstance(valor, Vetor):
            if valor.n == self.n:
                return Vetor([v + valor[i] for i, v in enumerate(self.vet)])
            else:
                print(f"Dimensões incompatíveis! {self.n} e {valor.n}")
    def __sub__(self, valor):
        return self.__add__(-valor)
    def __mul__(self, valor):
        """Multiplicação por escalar"""
        return Vetor([v * valor for v in self.vet])
    def __truediv__(self, valor):
        # NOTE: Poderia ter utilizado a __mul__
        if valor != 0:
            return Vetor([v / valor for v in self.vet])
        else:
            print("Divisão por zero!")
            raise ZeroDivisionError
    def __getitem__(self, key):
        return self.vet[key]
    def __setitem__(self, key, valor):
        self.vet[key] = valor
    def __str__(self):
        return str(f"Vet{self.vet}")
    def __repr__(self):
        return self.__str__()
    def __len__(self):
        return len(self.vet)
    def __neg__(self):
        return self.__mul__(-1)

class Matriz:
    def __init__(self, mat: list[list]):
        self.mat = []
        # Vetoriza
        for vet in mat:
            if isinstance(vet, list):
                self.mat.append(Vetor(vet))
            elif isinstance(vet, Vetor):
                self.mat.append(vet)
            else:
                print(f"Tipo inválido para vetor {type(vet)}")
                exit(1)
        self.n = len(self.mat)
        self.m = len(self.mat[0])
    def __add__(self, valor):
        if isinstance(valor, float) or isinstance(valor, int):
            return Matriz([vet + valor for vet in self.mat])
        elif isinstance(valor, Matriz):
            if valor.n == self.n:
                return Matriz([vet + valor[i] for i, vet in enumerate(self.mat)])
            else:
                print(f"Dimensões incompatíveis! {self.n} e {valor.n}")
    def __sub__(self, valor):
        return self.__add__(-valor)
    def __mul__(self, valor):
        """Multiplicação por escalar"""
        return Matriz([vet * valor for vet in self.mat])
    def __truediv__(self, valor):
        # NOTE: Poderia ter utilizado a __mul__
        if valor != 0:
            return Matriz([vet / valor for vet in self.mat])
        else:
            print("Divisão por zero!")
            raise ZeroDivisionError
    def __getitem__(self, key):
        return self.mat[key]
    def __setitem__(self, key, valor):
        self.mat[key] = valor
    def __len__(self):
        return (self.n, self.m)
    def __str__(self):
        texto = ""
        for linha in self.mat:
            for i, el in enumerate(linha):
                texto += f"{round(el, 1):<6}" + ("" if i != len(linha) - 2 else "| ")
            texto += "\n"
        return texto
    def __repr__(self):
        return f"Matriz: {self.n}X{self.m}"
    # - Funcional -
    def copiar(self):
        """Retorna objeto matriz copiado com os mesmos valores"""
        return Matriz(self.mat.copy())
    # - Visual -
    def printar(self):
        """Printa matriz"""
        print("MATRIZ -\n" + self.__str__())
    # - Matemáticos -
    def trocar_linha(self, de: int, para: int):
        if de > mat.n or para > mat.n:
            print("Troca além do limite da matriz")
            exit(1)
        temp_vet = self.mat[de]
        self.mat[de] = self.mat[para]
        self.mat[para] = temp_vet


mat_l = []
# ---- Leitura da matriz ----
# TODO: Colocar dentro da classe matriz
with open("matriz.txt", mode="r") as arq:
    for linha_str in arq:
        linha_l = linha_str.rstrip().split(" ")
        
        # Verifica se há fração:
        vet_l = []
        for el in linha_l:
            frac = el.split("/")
            if len(frac) == 1:
                vet_l.append(float(el))
            else:
                # Assume fração
                vet_l.append(Frac(int(frac[0]), int(frac[1])))
        mat_l.append(vet_l)


def escalonar(mat: Matriz, inicio: Vetor = Vetor([0,0])):
    min_dim = min(mat.n, mat.m - 1)
    for offset in range(min_dim):
        i1, i2 = inicio + offset
        # Divide pelo pivô linha atual
        print("Diagonal: ", offset + 1)
        pivo = mat[i1][i2]
        # Troca de linha (se possível)
        j = i1 - 1
        while pivo == 0 and (j + 1) < mat.n:
            j += 1
            pivo = mat[j][i2]
        if pivo == 0:
            print("Variável zerada!")
            continue
        elif j != i1 - 1:
            print(f"l{i1 + 1} <-> l{j + 1}")
            mat.trocar_linha(de=i1,para=j)
        if pivo != 1:
            mat[i1] = mat[i1] / pivo
            print(f"l{i1 + 1} <- l{i1 + 1} / {pivo + 1}")
        # Deleta acima e abaixo
        for l in range(mat.n):
            coef = mat[l][i2]
            if l != i1:
                mat[l] = mat[l] - mat[i1]*coef
                print(f"l{l + 1} <- l{l + 1} - l{i1 + 1}")
        mat.printar()
    return(mat)


def sistematizar(mat: Matriz):
    """Exibição dos valores por variável"""
    print("Sistema final:")
    for i, linha in enumerate(mat):
        # Variável principal:
        lado_d = False
        linha_str = ""
        for j, valor in enumerate(linha):
            valor_a = -valor if lado_d and (j + 1 < mat.m) else valor
            valor_str = ""
            # Teoricamente deveria checar se valores arredondados são igaus a 1 ou -1
            # TODO: Consertar sinal!
            if j + 1 < mat.m:
                if valor != 0:
                    valor_str += "("
                    if valor_a!= 1:
                        valor_str += f"{valor_a:.2f}"
                    elif valor_a == -1.00:
                        valor_str += "-"
                    valor_str += f"x_{j + 1})"
                    valor_str += ")"
                else:
                    continue
                if not lado_d:
                    valor_str += " = "
                    lado_d = True
                elif j + 1 < mat.m:
                    valor_str += " + "
            else:
                if linha_str:
                    valor_str += f"({valor_a:.2f})"
            linha_str += valor_str
        print(linha_str)

mat = Matriz(mat_l)
# ---- Checa se matriz é valida ----
# [A|B] com A sendo quadrada:
if (mat.n == mat.m - 1):
    print(f"Matriz quadrada válida: {mat.n}X{mat.n}")
else:
    print(f"Matriz assimétrica: {mat.n}X{mat.n}")

# ---- Loop principal (Escalonamento) ----
# -1 pois ignora coluna das independentes!
# Se for assimétrica acha todas as quadradas nela!
min_dim = min(mat.n, mat.m - 1)
# mat.n - min_dim + 1 - 1
# O +1 é pra contar de 0 até algum índice
# O -1 é para tirar as independentes
for d1 in range(mat.n - min_dim + 1):
    for d2 in range(mat.m - min_dim):
        inicio_atual = Vetor([d1,d2])
        print("Matriz inicial:")
        mat.printar()
        print("Início:", str(inicio_atual))
        mat_final = escalonar(mat.copiar(), inicio=inicio_atual)
        print("Matriz final:")
        mat_final.printar()
        sistematizar(mat_final)
# TODO: Talvez output para um arquivo latex?