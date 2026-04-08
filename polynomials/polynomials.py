# Script representativo de polinômios e operações polinomiais
# -- Setup --
# Funções
UPPERSCRIPT = '⁰¹²³⁴⁵⁶⁷⁸⁹'
to_upscritp = lambda val: ''.join([UPPERSCRIPT[int(c)] for c in str(val)])
# Classes
class Monomio:
    """Representação de monômios reais"""
    def __init__(self, coef: complex, exp: int, var: str = 'x'):
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
                raise ValueError(f"Variáveis {other.var} != {self.var}! Sem suporte!")
        else:
            raise ValueError("Valor inválido!")
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
    # - Representação -
    def __str__(self):
        # Por agora sem to_upscritp
        return f"{(round(self.coef, 1) if isinstance(self.coef,float) else self.coef)}{self.var}^({self.exp})"
    def __repr__(self):
        return self.__str__()


class Polinomio:
    """Classe para polinomios"""
    def __init__(self, monos: list[Monomio], letra: str = 'P'):
        # Organiza os monômios em um dicionário onde o grau é a chave
        # Deixa os monômios em ordem decrescente de grau
        # TODO: Somar poli de mesmo graus aqui! (a.k.a Colpsar o polinômio)
        self.monos = sorted(monos, key=lambda m: m.gr, reverse=True)
        self.letra = letra
    # - Matemáticos -
    @property
    def gr(self):
        # return max([m.gr() for m in self.monos if m])
        # Uma vez que estão em ordem decrescente de grau!
        return self.monos[0].gr
    def __add__(self, other):
        # TODO: talvez com sistema de POPS pra ir registrnado monos.?
        e_mono = isinstance(other, Monomio)
        e_poli = isinstance(other, Polinomio)
        novos_mono: list[Monomio] = []
        if e_mono or e_poli:
            if e_poli:
                nova_letra = f"[{self.letra} + {other.letra}]"
                for mono in self:
                    temp_monos = []
                    for o_mono in other:
                        if mono.var == o_mono.var:
                            if mono.gr == o_mono.gr:
                                temp_monos.append(mono + o_mono)
                    if not temp_monos:
                        novos_mono.append(mono)
                    else:
                        novos_mono.extend(temp_monos)
            elif e_mono:
                nova_letra = self.letra # TODO: Arrumar outro jeito!
                for mono in self:
                    if mono.gr == other.gr:
                        novos_mono.append(mono + other) # Assume polinômio colapsado!
                    else:
                        novos_mono.append(mono)
        else:
            raise ValueError("Sem suporte!")
        return Polinomio(monos = novos_mono, letra = nova_letra)
    # - Computacionais -
    def get_vars(self):
        """Returna variáveis ordenadas alfabeticamente"""
        return sorted(list({m.var for m in self.monos}))
    def __iter__(self):
        for mono in self.monos:
            yield mono
    # - Representação -
    def __str__(self):
        # Por agora sem to_upscritp
        return f"{self.letra}({','.join(v for v in self.get_vars())}) = {' + '.join([str(m) for m in self])}"
    def __repr__(self):
        return self.__str__()
    


def main():
    m = Monomio(300.09, 3)
    n = Monomio(200.09, 3, var='y')
    r = Monomio(2, 2)
    s = Monomio(3,2)
    p = Polinomio([m * r, n])
    p1 = Polinomio([m], letra = "P1")
    p2 = Polinomio([n], letra = "P2")
    print(p1)
    print(p2)
    print(p1 + p2)


if __name__ == "__main__":
    main()