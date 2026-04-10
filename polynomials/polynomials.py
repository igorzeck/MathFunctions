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
        return self.exp
    def __neg__(self):
        """Expressão curada para caso seja MonomioNulo (que extende dessa classe!)"""
        if isinstance(self, Monomio):
            return Monomio(-self.coef, -self.exp, -self.var)
        else:
            return self
    def __add__(self, other):
        if isinstance(other, Monomio):
            if other.var != self.var:
                # Por agora sem suporte completo! Uma vez que do contrário teria que ter
                # Suporte para monômios com múltiplas variáveis
                # Teoricamente retornaria um Poli!
                # TODO: Bloquear ao invés de retornar um Poli. seria mais seguro?
                return Polinomio([other, self])
                # raise ValueError(f"Variáveis {other.var} != {self.var}! Sem suporte!")
            if other.exp != self.exp:
                raise ValueError(f"Expoentes {other.exp} != {self.exp}! Sem suporte!")
            if other.coef + self.coef != 0:
                # TODO: Taxa de tol. por se tratar de floats?
                return Monomio(other.coef + self.coef, self.exp, self.var)
            else:
                return MonoNulo()
        else:
            raise ValueError("Valor inválido!")
    def __iadd__(self, other):
        # Estranho que ele espere um retorno!
        return self + other
    def __sub__(self, other):
        return self.__add__(-other)
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
    def nulo(self):
        return False
    # - Representação -
    def __str__(self):
        # Por agora sem to_upscritp
        str_coef = f"{(round(self.coef, 1) if isinstance(self.coef,float) else self.coef)}"
        str_exp = f"{self.var}^({self.exp})" if self.exp else ""
        return f"{str_coef}{str_exp}"
    def __repr__(self):
        return self.__str__()


class MonoNulo(Monomio):
    """Representação de um monômio nulo. Variável e expoentes são irrelevantes"""
    def __init__(self, coef = 0, exp = 0, var = 'x'):
        # TODO: Talvez exp = -1 (já que não podem ser menor que 0 de qualquer jeito)?
        super().__init__(coef, exp, var)
    # - Matemáticos -
    def __add__(self, other):
        return other
    def __sub__(self, other):
        return other
    # - Computacionais -
    def nulo(self):
        return True
    

class Polinomio:
    """Classe para polinomios"""
    def __init__(self, monos: list, letra: str = 'P'):
        # Organiza os monômios em um dicionário onde o grau é a chave
        # Deixa os monômios em ordem decrescente de grau
        max_gr = max(monos, key=Monomio.get_gr).gr
        # Adiciona elementos de mesmo grau
        # Dicionário de dicionários!
        # Note que o monos_pool guarda os objetos em si que são referenciados pelo dicionário
        # Pelo menos em teoria...
        self.monos_pool: list[Monomio] = []
        self.monos: dict[dict[Monomio]] = dict()
        
        # Separa por variáveis únicas
        for var in set([m.var for m in monos]):
            # Cria dicionário para aquela variável
            self.monos[var] = dict()
            for k in range(max_gr + 1):
                todos_gr = [m for m in monos if (m.gr == k) and (m.var == var)]
                if todos_gr:
                    if len(todos_gr) > 1:
                        v = todos_gr[0]
                        for v1 in todos_gr[1:]:
                            v += v1
                    else:
                        v = todos_gr[0]
                    # Evitar append de monômios nulos!
                    if not v.nulo():
                        self.monos[var][k] = v
                        self.monos_pool.append(v)
        self.monos_pool.sort(key=Monomio.get_gr, reverse=True)
        self.letra = letra
    # - Matemáticos -
    @property
    def gr(self):
        # return max([m.gr() for m in self.monos if m])
        return len(self.monos)
    def get_coefs(self, var: str = 'x'):
        # TODO: Ideal seria que var fosse por padrão a primeira do polinômio!
        """Série de coeficientes é por variável"""
        for m in range(max(self.monos[var]), -1, -1):
            if m in self.monos[var]:
                mono = self.monos[var][m]
                yield mono.coef
            else:
                yield 0
    def __neg__(self):
        mono_l = []
        for mono in self.monos_pool:
            mono_l.append(Monomio(-mono.coef, mono.exp, mono.var))
        return Polinomio(mono_l, self.letra)
    def __add__(self, other):
        monos_l = []
        var_u = set(self.monos.keys()).union(set(other.monos.keys()))
        for var in var_u: 
            # Por clareza se mantém o '[var]' no 'monos' e não no 'self'/'other'
            k_u = set(self.monos[var].keys()).union(set(other.monos[var].keys()))
            for k in k_u:
                # TODO: Streamline isso aqui
                if k in self.monos[var] and k in other.monos[var]:
                    # Possível que seja um Poli!
                    monos_l.append(self.monos[var][k] + other.monos[var][k])
                elif k in self.monos[var]:
                    monos_l.append(self.monos[var][k])
                elif k in other.monos[var]:
                    monos_l.append(self.monos[var][k])
        return Polinomio(monos_l, letra = "[" + self.letra + "+" + other.letra + "]")
    def __sub__(self, other):
        return self.__add__(-other)
    # - Computacionais -
    def get_vars(self):
        """Retorna variáveis ordenadas alfabeticamente"""
        return sorted(list({m.var for m in self.monos_pool}))
    def __iter__(self):
        # Note que já está sorteado!
        for m in self.monos_pool:
            yield m
    # - Representação -
    def __str__(self):
        # Por agora sem to_upscritp
        return f"{self.letra}({','.join(v for v in self.get_vars())}) = {self.eq}"
    def __repr__(self):
        return self.__str__()
    def __getitem__(self, key):
        return self.mono[key]
    @property
    def eq(self):
        # TODO: Melhorar formatação para números negativos!
        return f"{' + '.join([str(m) for m in self if not m.nulo()])}"


def main():
    m = Monomio(300.09, 3)
    n = Monomio(200.09, 4)
    o = Monomio(100.09, 3, var="y")
    v = Monomio(300.09, 3, var="y")
    p1 = Polinomio([m,n,o], letra = "P")
    p2 = Polinomio([m,v], letra = "Q")
    print(list(p1.get_coefs()))
    print(f"({p1.eq})-({p2.eq})=({(p1-p2).eq})")


if __name__ == "__main__":
    main()