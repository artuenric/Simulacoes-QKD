# Simulações QKD
Este repositório armazena códigos desenvolvidos em Python para simular redes que utilizam de **Distribuição Quântica de Chaves (QKD)** para atender às demandas de chaves para aplicações com criptografia clássica.

## Informações básicas
As redes são construídas com auxílio da biblioteca ``networkx``, contendo topologias da China, Vienna e EUA, além de algumas topologias genéricas. Os protocolos de QKD utilizados são: BB84, E91, B92. As simulações levam em consideração as diferentes formas de cálculo das rotas, topologias da rede, fidelidade dos canais e atributos dos requests.

## Diretórios
- ``/components``: arquivos necessários para o funcionamento das simulações.
- ``/qkd``: arquivos dedicados ao funcionamento dos protocolos.
- ``/demos``: demonstrações práticas do funcionamento dos protocolos e simulações.
- ``/lixeira``: arquivos ou ideias antigas que não foram totalmente descartadas.
