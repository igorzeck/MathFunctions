# Script representativo de polinômios e operações polinomiais
# -- Setup --
from math import isclose
# Funções
UPPERSCRIPT = '⁰¹²³⁴⁵⁶⁷⁸⁹'
NUMERICOS = (int, float, complex)

to_upscritp = lambda val: ''.join([UPPERSCRIPT[int(c)] for c in str(val)])
# Classes
# TODO: Classe para numéricos como Monômios? Assim simplifica funções!
class Monomio:
    """
    Representação de monômios reais.
    Funções constantes podem ser representadas com o valor de variável vazia
    """
    # TODO: Suporte para inserção por string para o __init__
    def __init__(self, coef: complex = 1, exp: int = 1, var: str = 'x'):
        self.coef = coef
        self.exp = exp if exp > 0 else 0
        self.var = var
    # - Matemáticos -
    # Decorator '@' equivalente a gr = property(gr)
    @property
    def gr(self):
        return self.exp
    def __neg__(self):
        return Monomio(-self.coef, -self.exp, self.var)
    def __add__(self, other):
        if isinstance(other, Monomio):
            if other.nulo():
                # Elemento nulo!
                return self
            if other.var != self.var:
                # Por agora sem suporte completo! Uma vez que do contrário teria que ter
                # Suporte para monômios com múltiplas variáveis
                # Teoricamente retornaria um Poli!
                return Polinomio.compor([self, other])
                # raise ValueError(f"Variáveis {other.var} != {self.var}! Sem suporte!")
            if other.exp != self.exp:
                return Polinomio.compor([self, other])
                # raise ValueError(f"Expoentes {other.exp} != {self.exp}! Sem suporte!")
            if not isclose(other.coef + self.coef, 0):
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
        if isinstance(other, NUMERICOS):
            # Para todos efeitos um poli./mono. constante (exceto o complexo)
            return Monomio(self.coef * other, self.exp, self.var)
        elif isinstance(other, Monomio):
            if other.var == self.var:
                return Monomio(other.coef * self.coef, other.exp + self.exp, self.var)
            else:
                # Por agora sem suporte! Uma vez que do contrário teria que ter
                # Suporte para monômios com múltiplas variáveis
                raise ValueError(f"Variáveis {other.coef} != {self.coef}! Sem suporte!")
        else:
            raise ValueError("Valor inválido!")
    def __truediv__(self, other):
        # Claro, pode dar erro ZeroDivisionError se um deles for do tipo MonoNulo
        # Poderia ser __mul__ com on inverso deles também, mas teoricamente
        # haveriam entes matemáticos diferentes de polinômios envolvidos
        if isinstance(other, NUMERICOS):
            return Monomio(self.coef / other, self.exp, self.var)
        exp_novo = self.exp - other.exp
        if other.var and (self.var != other.var):
            raise ValueError("Divisão por Monômios de variáveis diferentes não retornaria um polinômio.")
        if exp_novo < 0:
            raise ValueError(f"Valor não é expressão polinomial. Expoente < 0 ({exp_novo})")
        # Caso seja um valor constante a "variável" será apens ''
        var_nova = '' if exp_novo else self.var
    
        return Monomio(self.coef / other.coef, exp_novo, self.var)
    # - Computacionais -
    def get_gr(self):
        return self.gr
    def resolver(self, x: complex) -> complex:
        return self.coef * (x ** self.exp)
    # Talvez property? Se for o caso teria que mudar pra tirar do MonoNulo!
    def nulo(self):
        return False
    # - Representação -
    def __str__(self):
        # Por agora sem "to_upscritp"
        if isinstance(self.coef,float):
            coef_str = str(round(self.coef, 1))
            # "1.5" -> "1" -> ""
            if coef_str[-2:] == '.0':
                coef_str = coef_str[:-2]
            if coef_str == '1' and self.exp != 0:
                coef_str = ''
        else:
            self.coef == self.coef
        str_coef = f"{(coef_str if isinstance(self.coef,float) else self.coef)}"
        str_exp = f"{self.var}^({self.exp})" if self.exp else ""
        return f"{str_coef}{str_exp}"
    def __repr__(self):
        return self.__str__()


# Utilizando Singleton pattern
class MonoNulo(Monomio):
    # Classe(params) -> el = __new__(cls) -> el.__init__(self, params)
    """Representação de um monômio nulo. Variável e expoentes são indefinidos."""
    _instancia = None  # Essencialmente atributo estático
    # De certa forma todas as classes se referem a um único objeto
    def __new__(cls):
        # NOTE: __init__ não controla classe retornada, mas o __new__ sim (O __init ainda roda)
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia
    def __init__(self):
        # NOTE: O expoente é tratado como zero, apesar de ser indeterminado
        if hasattr(self, '_inicializado'):
            return
        # Tecnicamente é só uma constante 0!
        super().__init__(0, 0, '')
        self._inicializado = True
    # - Matemáticos -
    def __neg__(self):
        return self
    def __add__(self, other):
        return other
    def __sub__(self, other):
        return other
    def __mul__(self, other):
        # Por "performance" retorna a mesma entidade...
        # Idealmente haveria apenas um MonoNulo que seria referenciado em todo lugar!
        return self
    def __truediv__(self, other):
        # Notas semelhantes para o caso de __mul__
        if isinstance(other, NUMERICOS):
            if other == 0:
                raise ZeroDivisionError()
        
        return self
    # - Computacionais -
    def nulo(self):
        return True
    

class Polinomio:
    """
    Classe para polinomios
    Note que a classe é de natureza estática e não
    lida bem com modificações após sua criação.
    """
    # NOTE: Raízes são unidas (U) durante multiplicação polinomial!
    # NOTE: a*P(x) tem mesma raíz que P(x)?
    def __init__(self, monos, monos_pool, nome: str = 'P'):
        # Verifica se resultado é de fato Polinômio ou Monômio/Constante
        # Pelo visto o ideal é ter um construtor a parte mesmo!
        self.monos = monos
        self.monos_pool = monos_pool
        self.nome = nome
    @staticmethod
    def compor(lista_monos: list[Monomio], nome: str = 'P'):
        """Cria um polinômio com base em uma lista de monômios ou uma string"""
        # Organiza os monômios em um dicionário onde o grau é a chave
        # Deixa os monômios em ordem decrescente de grau
        # É possível ter um polinômio de um só monômio
        max_gr = max(lista_monos, key=Monomio.get_gr).gr
        # Adiciona elementos de mesmo grau
        # Dicionário de dicionários!
        # Note que o monos_pool guarda os objetos em si que são referenciados pelo dicionário
        # Pelo menos em teoria...
        monos_pool: list[Monomio] = []
        monos: dict[dict[Monomio]] = dict()
        
        # Separa por variáveis únicas
        for var in set([m.var for m in lista_monos]):
            # Cria dicionário para aquela variável
            monos[var] = dict()
            for k in range(max_gr + 1):
                todos_gr = [m for m in lista_monos if (m.gr == k) and (m.var == var)]
                if todos_gr:
                    if len(todos_gr) > 1:
                        v = todos_gr[0]
                        for v1 in todos_gr[1:]:
                            v += v1
                    else:
                        v = todos_gr[0]
                    # Evitar append de monômios nulos!
                    if not v.nulo():
                        monos[var][k] = v
                        monos_pool.append(v)
        if monos_pool:
            monos_pool.sort(key=Monomio.get_gr, reverse=True)
            return Polinomio(monos=monos, monos_pool=monos_pool, nome=nome)
        else:
            return MonoNulo()
    # - Matemáticos -
    @property
    def gr(self):
        return max([m.gr for m in self.monos_pool if m])
    def get_coefs(self, var: str = ""):
        # Por padrão é a "primeira" do Polinômio
        # Polinômio garantidamente sempre terá variável!
        if not var:
            var = self.get_vars()[0]
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
        return Polinomio.compor(mono_l, self.nome)
    def __add__(self, other):
        monos_l = []
        var_u = set(self.monos.keys()).union(set(other.monos.keys()))
        for var in var_u: 
            # Por clareza se mantém o '[var]' no 'monos' e não no 'self'/'other'
            k_u = set(self.monos[var].keys()).union(set(other.monos[var].keys()))
            for k in k_u:
                # TODO: Streamline isso aqui
                if (k in self.monos[var]) and (k in other.monos[var]):
                    monos_l.append(self.monos[var][k] + other.monos[var][k])
                elif k in self.monos[var]:
                    monos_l.append(self.monos[var][k])
                elif k in other.monos[var]:
                    monos_l.append(other.monos[var][k])
        return Polinomio.compor(monos_l, nome = "[" + self.nome + "+" + other.nome + "]")
    def __sub__(self, other):
        # Nome poli. errado!
        return self.__add__(-other)
    def __mul__(self, other):
        mono_l = []
        novo_nom = self.nome
        if isinstance(other, (int, float, complex, Monomio)):
            # Extrair nome de uma variável como essa é mais complexo que necessário
            # Nome se mantém!
            for mono in self.monos_pool:
                mono_l.append(mono * other)
        elif isinstance(other, Polinomio):
            novo_nom += other.nome
            # Distributiva
            # NOTE: Por simplicidade só é feito entre mesmas variáveis
            if len(set(other.get_vars() + self.get_vars())) > 1:
                raise IndexError("Multiplicação suportada apenas entre polinômios de mesma variável!")
            
            for mono_s in self.monos_pool:
                for mono_o in other.monos_pool:
                    mono_l.append(mono_o * mono_s)
        elif isinstance(other, Monomio):
            mono_l = [mono_s * other for mono_s in self.monos_pool]
        else:
            raise ValueError(f"Valor inválido para multiplicação: {other}")
        return Polinomio.compor(mono_l, nome=novo_nom)
    def __truediv__(self, other):
        """
        Retorna tupla de (quociente, Resto) -> (Monomio|Polinomio|Numerico, Monomio|Polinomio|Numerico)
        """
        # Algorítmo da divisão
        # Por agora, par números:
        if isinstance(other, NUMERICOS):
            return Polinomio.compor(monos=[m / other for m in self.monos_pool], nome = self.nome), MonoNulo()

        if not isinstance(other, Polinomio):
            raise TypeError(f"Tipo {type(other)} não suportado para divisão de polinômios!")
            # TODO: Suporte para monômios!
        
        if self.gr < other.gr:
            # Talvez retornar copia ao invés de self? Com o nome 'R'
            return MonoNulo(), self.copiar("R")
        
        # Por agora, sem suporte para polinômios multivariados
        if len(self.get_vars()) > 1:
            raise ValueError("Divião não suportada para polinômios multivariados!")
        
        max_iter = 100  # Teoricamente pode lidar com poli. de grau máximo = 100!
        i = 0
        
        # Note que monos_pool já é ordenado por grau (decrescente)!
        resto = Polinomio.compor(self.monos_pool, nome = 'R')
        quociente: list[Monomio] = []
        o_termo_p = other.monos_pool[0] if isinstance(other, Polinomio) else other

        while (i < max_iter) and (resto.gr >= other.gr) and not (resto is MonoNulo):
            mono_q = resto.monos_pool[0] / o_termo_p
            quociente.append(mono_q)
            print(quociente)

            temp_poli = other * mono_q

            # Possível que não zere o termo principal! A conta deveria ser
            # iealmente feita numa lista de coeficientes não aqui!
            dif = resto - temp_poli
            if isinstance(dif, Polinomio):
                resto = Polinomio.compor(lista_monos = dif, nome = 'R')
            elif isinstance(dif, MonoNulo):
                resto = dif
            i += 1
        
        return Polinomio.compor(quociente, nome='Q'), resto
    # - Computacionais -
    def get_vars(self):
        """Retorna variáveis ordenadas alfabeticamente"""
        return sorted(list({m.var for m in self.monos_pool}))
    def __iter__(self):
        # Note que já está sorteado!
        for m in self.monos_pool:
            yield m
    def valor_numerico(self, x: complex) -> complex:
        return sum((m.resolver(x) for m in self.monos_pool))
    def copiar(self, nome_copia: str = ''):
        return Polinomio(self.monos, self.monos_pool, self.nome if not nome_copia else nome_copia)
    # - Representação -
    def __str__(self):
        # Por agora sem to_upscritp
        return f"{self.nome}({','.join(v for v in self.get_vars())}) = {self.eq}"
    def __repr__(self):
        return self.__str__()
    def __getitem__(self, key):
        return self.monos[key]
    @property
    def eq(self):
        return f"{' + '.join([(str(m) if m.coef > 0 else f"[{str(m)}]") for m in self if not m.nulo()])}"


def main():
    m = Monomio(1.0, 3)
    n = Monomio(2, 4)
    o = Monomio(2, 3)
    print(m + n)
    # o = Monomio(1, 2)
    # v = Monomio(3, 3, var="y")
    p1 = Polinomio.compor([m,n,o], nome = "P") # Grau 4
    p2 = Polinomio.compor([m,o], nome = "Q") # Grau 3
    
    # ex1 = Polinomio(monos = [Monomio(exp = 5),
    #                          Monomio(2, 4),
    #                          Monomio(8, 3),
    #                          Monomio(4, 2),
    #                          Monomio(5, 1),
    #                          Monomio(2, 0),
    #                          ], nome = 'A')
    # print(ex1)
    # ex2 = Polinomio(monos = [Monomio(exp = 3),
    #                          Monomio(exp = 2),
    #                          Monomio(2, 1),
    #                          Monomio(-3, 0)
    #                          ], nome = 'B')
    # print(f"({ex1.eq})/({ex2.eq})=({(ex1 / ex2)})")
    
    # k = 2
    # x = (1j)
    # print(f"x={x},",p1.eq,end=" = ")
    # print(p1.valor_numerico(x))


    # print(f"({p1.eq})/({k})=({(p1 / k)})")
    print(p1, p2)
    # print(f"({p2.eq})/({p1.eq})=({(p2 / p1)})")
    print(f"({p1.eq})/({p2.eq})=({(p1 / p2)})")
    # print(f"({p1.eq})*({p2.eq})=({(p1 * p2).eq})")


if __name__ == "__main__":
    main()