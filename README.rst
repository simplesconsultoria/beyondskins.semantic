.. contents:: Table of Contents
   :depth: 2

*****************************************************
beyondskins.semantic.portal
*****************************************************

Introdução
----------
Este documento tem que describir as mudanças gerales no pacote para entender o
que acontece ao intalar ele.

Document by-line
----------------

O template do viewlet 'plone.belowcontenttitle.documentbyline' foi sobrescrito
para mostrar as datas de publicação e modificação do conteúdo. A data de
modificação só se motra se for diferente da data de publicação.

Para o viewlet se mostrar para usuário não autenticados tem que selecionar
'Permitir a qualquer um ver as informações sobre o conteúdo' em Configurações
de segurança da Configuração do Site.

Tiles
-----

Coleção de autores
^^^^^^^^^^^^^^^^^^
Mostra os 4 primeiros itens do resultado duma coleção. Os itens tem que ser
artigos o eles vão ser filtrados.

Lista de autores
^^^^^^^^^^^^^^^^
Mostra uma lista de até 5 autores e seu artigo publicado mais recente.
