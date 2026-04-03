# Script para cálculo de simplex em R ----
# 0. Setup ----
library(tidyverse)

# 1. Matriz ----
# matriz <- tribble(
#   ~z,~x1,~x2,~s1,~s2,~s3,~b,
#   1,-3,-2,0,0,0,0, # 1 -> z
#   0,2,1,1,0,0,100,
#   0,1,1,0,1,0,80,
#   0,1,0,0,0,1,40,
# )
# matriz <- tribble(
#   ~z,~x1,~x2,~s1,~s2,~b,
#   1,-40,-30,0,0,0, # 1 -> z
#   0,1,1,1,0,12,
#   0,2,1,0,1,16,
# )
# matriz <- tribble(
#   ~z,~x1,~x2,~x3,~x4,~s1,~s2,~s3,~s4,~b,
#   1,-25.473,-9.45,-85.2,-31,0,0,0,0,450.3, # 1 -> z
#   0,1.1,5,63,28,1,0,0,0,350,
#   0,13,3.4,21,2.7,0,1,0,0,80,
#   0,11,1,1.2,.3,0,0,1,0,20,
#   0,.373,0.05,0,0,0,0,0,1,.3,
# )

n_var <- length(matriz) - 1

matriz

# 2. Simplex ----
# Para máximo e com restrições <= 0

rec_max <- 10
iter <- 0

# 0. Quantidade de não básicas
n_dim <- matriz |> 
  select(starts_with("x")) |> 
  names() |> 
  length()

# Apenas entra no loop e negativo
while (any(matriz[1,] < 0) && iter < rec_max) {
  print(paste("Iter:", iter))
  # 0. Seleciona próxima VNBs
  # Por agora seleciona os != de zero na linha z (sem contar z e b)
  # Por problema de precisão, seleciona-se os n_dim maiores valores,
  # com n sendo o tamanho da VNB
  vnb <- matriz[1,] |> 
    summarise(across(2:(length(matriz) - 1), ~ max(abs(.), na.rm = TRUE))) |> 
    pivot_longer(everything()) |> 
    slice_max(value, n = n_dim) |> 
    pull(name)
  
  cat("VNB = {",paste0(vnb, ","),"}\n")
  # RESULTADo: Mostra resultado da anterior
  # Pega apenas colunas relevantes na matriz
  resultado <- matriz |> 
    select(!all_of(vnb))
  
  print(matriz)
  print("Resultado:")
  print(resultado)
  
  # 1. Escolhe coluna com menor valor na linha da função objetivo (linha 1)
  # Lembrando que: z (1), x1 (2), ... b (n_var + 1)
  matriz_var <- matriz[2:n_var]
  coluna <- names(matriz_var)[apply(matriz_var, 2, min) == min(apply(matriz_var, 2, min))][1]
  print(paste("Coluna:", coluna))
  
  # 2. Escolhe linha que passa o teste da razão
  teste_razao <- matriz$b / matriz[,coluna]
  # Suporte para max apenas
  id_linha_min <- which.max(teste_razao[,1])
  
  # Escolha do menor id!
  for (id_linha in seq(2, nrow(teste_razao))) {
    val_min <- teste_razao[id_linha,]
    if (val_min < teste_razao[id_linha_min,] && val_min > 0) {
      id_linha_min <- id_linha
    }
  }
  linha <- id_linha_min
  
  print(paste("Linha:", linha))
  
  # 3. Divide linha pelo pivõ
  matriz[linha,] <- matriz[linha,] / as.numeric(matriz[linha, coluna])
  
  # 4. Zera acima e embaixo do pivô
  for (id_linha in 1:nrow(matriz[,coluna])) {
    # Multiplica pelo oposto do elemento a ser anulado
    if (id_linha != linha) {
      matriz[id_linha,] <- matriz[id_linha,] - matriz[linha,] * as.numeric(matriz[id_linha, coluna])
    }
  }
  
  # Iterador
  iter <- iter + 1
}

# Note que existe a restrição de todos eles serem positivos!

