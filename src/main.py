""" Tutorial para aprender novas ferramentas.

Changelog
---------
.. versionadded::    23.10
    |br| 🌱 Rascunho inicial (28)

|   **Open Source Notification:** This file is part of open source program **Rapha Tutorial**
|   **Copyright © 2023  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <https://is.gd/3Udt>`_.
|   `Labase <http://labase.selfip.org/>`_ - `NCE <https://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""
# import bs4
import mechanicalsoup


# noinspection SpellCheckingInspection
class PokemonBase:
    def __init__(self):
        """ Preenche um dicionário Pokemon a partir dados encontrados no Fandom Nacional.

        Usa o Mechanical Soup que é o equivalente em Python do Puppeteer.

        """
        self.browser = mechanicalsoup.StatefulBrowser()
        url = "https://pokemon.fandom.com/pt-br/wiki/Pok%C3%A9dex_Nacional"
        self.browser.open(url)
        self.gera_poke = []  # cabeçalhos que descrevem cada geração
        self.poke_links = []  # link que podem ser de um pokemon
        self.poke_dex = {}  # dicionário que descreve os pokemons em cada geração
        self.consulta_poke = {}  # dicionário reverso que retorna a geração dado o pokemon

    def recolhe_dados_do_site(self):
        """ Sequência das operações para montar o dicionário.

        :return: None (Só chama as operações)
        """
        self.coleciona_links_das_geracoes()
        self.nome_dos_pokemons_nas_geracoes()
        self.conserta_sobrepor_listas()
        self.consultar_poke()

    def coleciona_links_das_geracoes(self):
        """ Encontra os títulos que delimitam as gerações nas tabelas.

        Na página os títulos das tabelas de geração são descritos assim:
        <span class="mw-headline" id="Segunda_Geração">Segunda Geração</span>

        As características são a classe e a palavra Geração encontrada no id.

        :return: None (preenche o gera_poke, lista de cabeçalhos das gerações)
        """
        self.gera_poke = [
            span_tag for span_tag in self.browser.page.find_all(class_="mw-headline")
            # acha todas as tags cuja classe seja "mw-headline"
            if "Geração" in span_tag["id"]
            # a palavra Geração tem que estar no id da tag span
        ]
        self.poke_dex = {
            span_tag["id"].split("_")[0]: span_tag
            # remove o sufixo _geração dividindo a string em torno do "_" e pegando a primeira parte [0]
            for span_tag in self.gera_poke}
        # temos agora um dicionário com o nome da geração e o span que está no cabeçalho

    def nome_dos_pokemons_nas_geracoes(self):
        """ Pega cada cabeçalho e lista todos os links abaixo que tenha o nome de um Pokemon.

        <td etc ><a href="/pt-br/wiki/Pokemon" title="Pokemon"><img alt="etc" src="etc"></a></td>
        A tag a ser encontrada é esta. Está dentro duma tag "td" e antes de uma tag "img".

        :return: None (Cria o poke_dex)
        """
        # x: bs4.element.Tag
        # x.find_next()
        self.poke_dex = {
            gera_do_pokemon: [
                link_do_pokemon["title"] for link_do_pokemon in span_tag.find_all_next("a")
                # obtém todos os links que estão abaixo deste cabeçalho
                if link_do_pokemon.has_attr("title") and
                # o link tem que ter um título
                link_do_pokemon.parent.name == "td" and
                # ele é filho duma tag "td" - table data
                link_do_pokemon.find_next().name == "img"
                # a próxima tag tem que ser img
            ]
            for gera_do_pokemon, span_tag in self.poke_dex.items()}
        # print("NEW POKE DEX")
        # print(self.poke_dex)
        # [print(gera, poke) for gera in "Oitava Nona".split() for poke in self.poke_dex[gera]]

    def conserta_sobrepor_listas(self):
        """ As listas das primeiras gerações englobam as seguintes devida à função find_all_next

        Para corrigir temos que remover duma lista os itens que estão na próxima.

        :return: None (Corrige o poke_dex)
        """
        ordem_ = ['Primeira', 'Segunda', 'Terceira', 'Quarta', 'Quinta', 'Sexta', 'Sétima', 'Oitava', 'Nona']
        corrente = ordem_.pop(0)
        # obtém o primeiro item e remove da lista
        while ordem_:
            proxima_gera = ordem_.pop(0)
            # obtém o próximo item e remove da lista
            self.poke_dex[corrente] = [it for it in self.poke_dex[corrente] if it not in self.poke_dex[proxima_gera]]
            # elimina cada item da próxima lista que está duplicado nesta
            corrente = proxima_gera

        # print("NEW POKE DEX CORRIGIDO")
        # [print(gera, poke) for gera in "Oitava Nona".split() for poke in self.poke_dex[gera]]
        self.consulta_poke = {poke: gera for gera, pokes in self.poke_dex.items() for poke in pokes}
        # cria um dicionário reverso que permita saber a geração dado o nome de um pokemon

    def consultar_poke(self):
        poke = input("diga o nome do pokemon: ")
        if poke in self.consulta_poke:
            print("A geração deste pokemon é: ", self.consulta_poke[poke])
        else:
            print("O nome não está correto")


if __name__ == '__main__':
    PokemonBase().recolhe_dados_do_site()
