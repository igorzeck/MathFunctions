# Script representativo de polinômios e operações polinomiais
# -- Setup --
from math import isclose
# Funções
UPPERSCRIPT = '⁰¹²³⁴⁵⁶⁷⁸⁹'
NUMERICOS = (int, float, complex)
NO_VAR_STR = '_CONSTANT_'

to_upscritp = lambda val: ''.join([UPPERSCRIPT[int(c)] for c in str(val)])
# Classes
class Monomio:
    """
    Representação de monômios reais.
    Funções constantes podem ser representadas com o valor de variável vazia
    """
    def __init__(self, *args, **kwargs):
        """
        *args -> coef, exp, var
        """
        # Valores default
        coef: complex = 1
        var: str = 'x'
        exp: int = 1
        expr = None

        if args:
            if isinstance(args[0],NUMERICOS):
                # Padrão
                coef: complex = args[0]
                if len(args) > 1:
                    exp: int = args[1]
                if len(args) > 2:
                    var: str = args[2]
            elif isinstance(args[0], str):
                expr: str = args[0]
            else:
                raise TypeError("Parâmetro inválido.")
        else:
            coef: complex = kwargs['coef'] if 'coef' in kwargs else coef
            exp: int = kwargs['exp'] if 'exp' in kwargs else exp
            var: str = kwargs['var'] if 'var' in kwargs else var
            expr: str = kwargs['expr'].lower().replace(' ', '') if 'expr' in kwargs else expr

        if expr:
            coef, var, exp = self._ler_expr(expr, coef, var, exp)

        self.coef = coef
        self.exp = exp if exp > 0 else 0
        self.var = var if exp > 0 else NO_VAR_STR
    # - Matemáticos -
    # Decorator '@' equivalente a gr = property(gr)
    @property
    def gr(self):
        return self.exp
    def __neg__(self):
        return Monomio(-self.coef, self.exp, self.var)
    def __add__(self, other):
        if isinstance(other, Monomio):
            if other.nulo():
                # Elemento nulo!
                return self
            if other.var != self.var:
                # Por agora sem suporte completo! Uma vez que do contrário teria que ter
                # Suporte para monômios com múltiplas variáveis
                # Retorna um Poli.!
                return Polinomio.compor_de_monos([self, other])
            if other.exp != self.exp:
                return Polinomio.compor_de_monos([self, other])
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
        elif isinstance(other, Polinomio):
            return self.cPoli() / other
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
    def _ler_expr(self, expr: str, pdr_coef, pdr_var, pdr_exp):
        if expr:
            # Lógica é simplista (divide string em três ao redo da variável)
            i_ini = -1
            i_fim = -1
            for i_tmp, c in enumerate(expr):
                if c.isalpha() and c != 'j':
                    if i_ini < 0:
                        i_ini = i_tmp
                        i_fim = i_tmp + 1
                else:
                    if i_ini > 0:
                        i_fim = i_tmp
                        break
            
            if i_ini < 0:
                pdr_coef = complex(expr) if 'j' in expr else float(expr)
                pdr_var = NO_VAR_STR
                pdr_exp = 0
            else:
                coef_, var_, exp_ = expr.partition(expr[i_ini:i_fim])
                pdr_coef = complex(coef_) if 'j' in coef_ else float(coef_)
                pdr_var = var_
                exp_ = exp_.replace("^","").replace("**","")

                # Checa por upperscript
                exp_clean_ = ""
                for n in exp_:
                    n_down = UPPERSCRIPT.find(n)
                    if n_down >= 0:
                        exp_clean_ += str(n_down)
                    else:
                        exp_clean_ += n
                if exp_:
                    pdr_exp = int(exp_clean_)
        return pdr_coef, pdr_var, pdr_exp
    def copiar(self):
        return Monomio(self.coef, self.exp, self.var)
    def cPoli(self, nome: str = 'M'):
        return Polinomio({self.var:{self.gr:self}}, [self], nome)
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
        self._raizes = []
    @staticmethod
    def compor_de_monos(lista_monos: list[Monomio]|Monomio, nome: str = 'P'):
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
    @staticmethod
    def compor(poli_str: str = ""):
        eq_str = poli_str.partition('=')
        if any((not s for s in eq_str)):
            raise ValueError("String da equação inválido. Escreva no padrão 'A(x) = 1x² + 2x^4 + 3x**5'")
        m_ind = 2 if any([c.upper() for c in eq_str[0]]) else 0
        n_ind = 0 if m_ind == 2 else 2

        eq_str[n_ind].strip()
        n_pos = eq_str[n_ind].find('(')
        n_pos = n_pos if n_pos >= 0 else -1

        n_str = eq_str[n_ind][:n_pos]

        # Com tratamento para negativos
        m_l = eq_str[m_ind].replace('-', '+-').replace(' ','').split('+')
        monos = [Monomio(m_str) for m_str in m_l]

        return Polinomio.compor_de_monos(monos, n_str)

    # - Matemáticos -
    @property
    def gr(self):
        return max([m.gr for m in self.monos_pool if m])
    def get_raizes(self):
        # Suporte atual apenas para univariáveis
        if len(list(self.get_vars())) > 1:
            raise ValueError("Polinômios multivariados não suportados.")
        if not self._raizes:
            self._calc_raiz()
        return self._raizes
    def get_coef_k(self, k: int, var: str = ""):
        if abs(k) > self.gr:
            raise ValueError(f"Não há coeficiente {k} para polinômio de grau {self.gr}")
        # Suporte para index negativo
        if k >= 0:
            # Note que o índice 0 refere-se ao "último" elemento
            k = self.gr - k
        else:
            k = abs(k) - 1
        if not var:
            var = self.get_vars()[0]
        if k in self.monos[var]:
            return self.monos[var][k].coef
        else:
            return 0

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
        return Polinomio.compor_de_monos(mono_l, self.nome)
    def __add__(self, other):
        monos_l = []
        if isinstance(other, Monomio):
            # Hot conversion
            other = other.cPoli("_")
        var_u = set(self.monos.keys()).union(set(other.monos.keys()))
        for var in var_u: 
            # Por clareza se mantém o '[var]' no 'monos' e não no 'self'/'other'
            if (var in self.monos) and (var in other.monos):
                k_u = set(self.monos[var].keys()).union(set(other.monos[var].keys()))

                for k in k_u:
                    if (k in self.monos[var]) and (k in other.monos[var]):
                        monos_l.append(self.monos[var][k] + other.monos[var][k])
                    elif k in self.monos[var]:
                        monos_l.append(self.monos[var][k])
                    elif k in other.monos[var]:
                        monos_l.append(other.monos[var][k])
            elif var in self.monos:
                monos_l.extend([self.monos[var][k] for k in self.monos[var]])
            elif var in other.monos:
                monos_l.extend([other.monos[var][k] for k in other.monos[var]])
        nome = "[" + self.nome + "+" + other.nome + "]" if other.nome != "_" else self.nome
        return Polinomio.compor_de_monos(monos_l, nome = nome)
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
        return Polinomio.compor_de_monos(mono_l, nome=novo_nom)
    def __truediv__(self, other):
        """
        Retorna tupla de (quociente, Resto) -> (Monomio|Polinomio|Numerico, Monomio|Polinomio|Numerico)
        """
        # Algorítmo da divisão
        # Por agora, par números:
        if isinstance(other, NUMERICOS):
            return Polinomio.compor_de_monos(monos=[m / other for m in self.monos_pool], nome = self.nome), MonoNulo()

        if not isinstance(other, (Polinomio, Monomio)):
            raise TypeError(f"Tipo {type(other)} não suportado para divisão de polinômios!")
        
        if self.gr < other.gr:
            # Talvez retornar copia ao invés de self? Com o nome 'R'
            return MonoNulo(), self.copiar("R")
        
        # Sem suporte para polinômios multivariados
        if len(self.get_vars()) > 1:
            raise ValueError("Divião não suportada para polinômios multivariados!")
        
        max_iter = 100  # Teoricamente pode lidar com polinômios de grau máximo = 100!
        i = 0
        
        # Note que monos_pool já é ordenado por grau (decrescente)!
        resto = Polinomio.compor_de_monos(self.monos_pool, nome = 'R')
        quociente: list[Monomio] = []
        o_termo_p = other.monos_pool[0] if isinstance(other, Polinomio) else other

        while (i < max_iter) and (resto.gr >= other.gr) and not (resto is MonoNulo):
            mono_q = resto.monos_pool[0] / o_termo_p
            quociente.append(mono_q)

            temp_poli = other * mono_q

            # Possível que não zere o termo principal! A conta deveria ser
            # iealmente feita numa lista de coeficientes não aqui!
            dif = resto - temp_poli
            if isinstance(dif, Polinomio):
                resto = Polinomio.compor_de_monos(lista_monos = dif, nome = 'R')
            elif isinstance(dif, MonoNulo):
                resto = dif
            i += 1
        
        return Polinomio.compor_de_monos(quociente, nome='Q'), resto
    def _calc_raiz(self):
        autoreciproco = all([self.get_coef_k(k) == self.get_coef_k(self.gr - k) for k in range(self.gr // 2)])
        # -- Raizes triviais --
        # Por agora apenas suporte para uma variável
        # Raiz 0
        if self.get_coef_k(-1) == 0:
            self._raizes.append(0)
        # - Raizes autorecíprocas e recíprocas -
        # Raiz 1
        if sum(self.get_coefs()) == 0:
            self._raizes.append(1)
        
        # Caso seja autorecíproco para toda raiz ele terá sua inversa garantida
        # - Raizes gerais -
        # NOTE: Foge escopo do projeto

    def identidade(self, other):
        if self.get_vars() != other.get_vars():
            return False
        
        # Bem direto, mas serve
        if list(self.get_coefs()) != list(other.get_coefs()):
            return False
        
        return True
    def __eq__(self, value):
        if isinstance(value, Polinomio):
            return self.identidade(value)
        else:
            # Mesmo para poli. de grau 0 comparando a valor numérico
            return False
    # - Computacionais -
    def get_vars_indie(self):
        """Retorna variáveis ordenadas alfabeticamente com todas categorias (inclui termos indenpendentes)"""
        return sorted(list({m.var for m in self.monos_pool}))
    def get_vars(self):
        """Retorna variáveis ordenadas alfabeticamente"""
        return sorted(list({m.var for m in self.monos_pool if m.var != NO_VAR_STR}))
    def __iter__(self):
        # Note que já está ordenado!
        for m in self.monos_pool:
            yield m
    def valor_numerico(self, xi: list[complex], vars: list[str] = []) -> complex:
        # Idealmente o valor numérico seria uma lista de valores!
        all_v = self.get_vars()
        if not vars:
            vars = [all_v[0]]

        no_v = set(all_v).difference(set(vars))
        val = 0

        for i, var in enumerate(vars):
            if var not in self.monos:
                raise ValueError(f"Variável {var} não ecnontrada no polinômio {self}.")

            val += sum((self.monos[var][m].resolver(xi[i]) for m in self.monos[var]))
        
        if NO_VAR_STR in self.monos:
            val += self.monos[NO_VAR_STR][0].resolver(0)

        if not no_v:
            return val
        else:
            return Polinomio.compor_de_monos([m for m in self.monos_pool if m.var in no_v] + [Monomio(str(val))])
    def copiar(self, nome_copia: str = ''):
        return Polinomio(self.monos, self.monos_pool, self.nome if not nome_copia else nome_copia) 
    def __getitem__(self, key):
        return self.monos[key]
    def __call__(self, *args, **kwds):
        """
        Valor numérico para 1 ou mais variáveis
        
        p(4) -> Valor numérico para variáel canônica
        
        p(y = 4) -> Valor numérico para variável de escolha (y)
        """
        if kwds:
            vars, vals = map(list, zip(*kwds.items()))
            return self.valor_numerico(vals, vars)
        elif args:
            all_vars = self.get_vars()
            split_ind = len(args) if len(args) < len(all_vars) else len(all_vars)
            
            all_vars = all_vars[:split_ind]

            return self.valor_numerico(args, all_vars)
        else:
            return 0
    # - Representação -
    def __str__(self):
        parenthesis = f"({','.join(v for v in self.get_vars() if v)})" if len(self.get_vars()) else ''
        return f"{self.nome}{parenthesis} = {self.eq}"
    def __repr__(self):
        return self.__str__()
    @property
    def eq(self):
        return f"{' + '.join([(str(m) if m.coef > 0 else f"[{str(m)}]") for m in self if not m.nulo()])}"


def main():
    m = Monomio(1.0, 2)
    n = Monomio(2, 1)
    o = Monomio(1.0, 0)
    
    p1 = Polinomio.compor_de_monos([m,n,o], nome = "P")
    p4 = Polinomio.compor("A = 2x⁴-3y   + 9")
    p5 = Polinomio.compor("A = 4x² - 4")
    print(p4.valor_numerico([2, 1], ['x','y']))
    print(p4(y=1,x=2))
    print(p4(1))
    print(p5 / Polinomio.compor("P(x)=2x"))
    print(p5 / Monomio("2x"))
    print(Monomio("2x") / p5)


if __name__ == "__main__":
    main()