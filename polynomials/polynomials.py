# Script representativo de polinômios e operações polinomiais
# -- Setup --
# Funções
UPPERSCRIPT = '⁰¹²³⁴⁵⁶⁷⁸⁹'
to_upscritp = lambda val: ''.join([UPPERSCRIPT[int(c)] for c in str(val)])
# Classes
class Monomio:
    """Representação de monômios reais"""
    def __init__(self, coef: complex, exp: int = 1, var: str = 'x'):
        self.coef = coef
        self.exp = exp if exp > 0 else 0
        self.var = var
    # - Matemáticos -
    # Decorator '@' equivalente a gr = property(gr)
    @property
    def gr(self):
        return self.exp if self.coef != 0 else None
    def __add__(self, other):
        if isinstance(other, Monomio):
            if other.var == self.var:
                if other.exp == self.exp:
                    return Monomio(other.coef + self.coef, self.exp, self.var)
                else:
                    raise ValueError(f"Expoentes {other.exp} != {self.exp}!")
            else:
                # Por agora sem suporte! Uma vez que do contrário teria que ter
                # Suporte para monômios com múltiplas variáveis
                # Teoricamente retornaria um Poli!
                return Polinomio([other.coef, self.coef])
                # raise ValueError(f"Variáveis {other.var} != {self.var}! Sem suporte!")
        else:
            raise ValueError("Valor inválido!")
    def __iadd__(self, other):
        # Estranho que ele espere um retorno!
        return self + other
    def __sub__(self, other):
        if isinstance(other, Monomio):
            # self.__add__(-other) também seria possível! (Teria que definir __neg__
            if other.var == self.var:
                if other.exp == self.exp:
                    if other.coef - self.coef != 0:
                        return Monomio(other.coef + self.coef, self.exp, self.var)
                    # else:
                    #     # TODO: Suporte para Monomios indefinidos
                    #     return Monomio(other.coef - self.coef, None, None)
                else:
                    raise ValueError(f"Expoentes {other.exp} != {self.exp}!")
            else:
                # Por agora sem suporte! Uma vez que do contrário teria que ter
                # Suporte para monômios com múltiplas variáveis
                raise ValueError(f"Variáveis {other.coef} != {self.other}! Sem suporte!")
        else:
            raise ValueError("Valor inválido!")
    def __mul__(self, other):
        if isinstance(other, Monomio):
            if other.var == self.var:
                return Monomio(other.coef * self.coef, other.exp + self.exp, self.var)
            else:
                # Por agora sem suporte! Uma vez que do contrário teria que ter
                # Suporte para monômios com múltiplas variáveis
                raise ValueError(f"Variáveis {other.coef} != {self.coef}! Sem suporte!")
        else:
            raise ValueError("Valor inválido!")
    # - Computacionais -
    def get_gr(self):
        return self.gr
    def e_nulo(self):
        return self.coef == 0
    # - Representação -
    def __str__(self):
        # Por agora sem to_upscritp
        return f"{(round(self.coef, 1) if isinstance(self.coef,float) else self.coef)}{self.var}^({self.exp})"
    def __repr__(self):
        return self.__str__()


class Polinomio:
    """Classe para polinomios"""
    def __init__(self, monos: list, letra: str = 'P'):
        # Organiza os monômios em um dicionário onde o grau é a chave
        # Deixa os monômios em ordem decrescente de grau
        # TODO: Somar poli de mesmo graus aqui! (a.k.a Colapsar o polinômio)
        # Possível Polinômio na lista!

        max_gr = max(monos, key=Monomio.get_gr).gr
        # Adiciona elementos de mesmo grau
        # TODO: Arrumar dicionário para ter suporte para variáveis diferentes
        # TODO: Talvez uma lista de dicionários por variável?
        self.monos = dict()
        
        for k in range(max_gr + 1):
            todos_gr = [m for m in monos if m.gr == k]
            if todos_gr:
                if len(todos_gr) > 1:
                    v = todos_gr[0]
                    for v1 in todos_gr[1:]:
                        v += v1
                else:
                    v = todos_gr[0]
                self.monos[k] = v
        self.letra = letra
    # - Matemáticos -
    @property
    def gr(self):
        # return max([m.gr() for m in self.monos if m])
        return len(self.monos)
    def get_coefs(self):
        for m in range(max(self.monos), -1, -1):
            if m in self.monos:
                mono = self.monos[m]
                yield mono.coef
            else:
                yield 0
    def __add__(self, other):
        monos_l = []
        for k in set(self.monos.keys()).union(set(other.monos.keys())):
            # TODO: Streamline isso aqui
            if k in self.monos and k in other.monos:
                # Possível que seja um Poli!
                monos_l.append(self.monos[k] + other.monos[k])
            elif k in self.monos:
                monos_l.append(self.monos[k])
            elif k in other.monos:
                monos_l.append(self.monos[k])
                
        return Polinomio(monos_l, letra = "[" + self.letra + "+" + other.letra + "]")
    # - Computacionais -
    def get_vars(self):
        """Returna variáveis ordenadas alfabeticamente"""
        return sorted(list({self.monos[k].var for k in self.monos}))
    def __iter__(self):
        # O sorted é para garantir que venham em ordem garantidamente
        for m in range(max(self.monos), -1, -1):
            if m in self.monos:
                mono = self.monos[m]
                yield mono
    # - Representação -
    def __str__(self):
        # Por agora sem to_upscritp
        return f"{self.letra}({','.join(v for v in self.get_vars())}) = {self.eq}"
    def __repr__(self):
        return self.__str__()
    @property
    def eq(self):
        return f"{' + '.join([str(m) for m in self if not m.e_nulo()])}"
    


def main():
    m = Monomio(300.09, 3)
    n = Monomio(200.09, 4)
    o = Monomio(100.09, 3)
    p1 = Polinomio([m,n,o], letra = "P")
    p2 = Polinomio([m,o], letra = "Q")
    print(f"({p1.eq})+({p2.eq})=({(p1+p2).eq})")
    print(list(p1.get_coefs()))


if __name__ == "__main__":
    main()