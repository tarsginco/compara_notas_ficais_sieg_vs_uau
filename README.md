# Comparar notas ficais do sieg vs uau
 
 Essa aplicação exporta e comparada dados das notas fiscais vindos do UAU e do SIEG. O objetivo é identificar as nfs que estão com o lançamento pendente no modulo fiscal.

 O <code>download_xmls_from_sieg_online.py</code> é responsável pela exportação das planilhas contendo um acompanhamento de nfs do SIEG. Essa rotina deve rodar duas vezes em cada mês (dia 2 e dia 20).

 <code>compare_uau.py</code> comparar os dados dessa planilha com as notas fiscais que já foram lançadas no UAU, buscando por uma chave diferente para cada tipo de nota fiscal:
 <code>
 nf_types = {
    'nfe':['CNPJ Emit','CNPJ Dest','Valor','Chave da NFe'] ,
    'nfse':['CNPJ Emit','CNPJ Dest','Valor','Num NFSe'] ,
    'cte':['CNPJ Emit','CNPJ Dest','Valor','Chave CT-e'] 
}
</code>
 
 Esse script deve rodar diariamente.

 ## Configurações iniciais
 Execute os seguintes comandos no terminal:
 <code>chmod +x entrypoint.sh</code>
 <code>./entrypoint.sh</code>

 Uma vez executado, adicione as credenciais em <code>.env</code>.

