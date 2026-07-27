# 1. libGammaMass.py
Este arquivo contém toda a geometria (materiais e células) para a simulação. Ele cria e entra em uma nova pasta toda vez que é executado. Contém configurações para plotagem e função para definir tallies.

# 2. simuUnicoGammaMass.py
Este arquivo utiliza as fuções e configurações definidas no arquivo 1 para rodar a simulação uma única vez.

# 3. VariaTarugo.py
Este arquivo utiliza as fuções e configurações definidas no arquivo 1 para rodar a simulação várias vezes, variando parâmetros escolhidos.

# 4. graficoPHT.py
Puxa os resultados das simulações das pastas finalmb_XX para montar gráficos de altura de pulso (pulse height spectrum). Energia depositada no cristal em função da energia da bin.

# 5. Pastas finalmb_XX
Resultados obtidos ao rodar as simulações para diferentes porcentagens da altura útil do tarugo.
