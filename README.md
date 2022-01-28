# Automation of satellite image processing methodologies for geospatial applications - UDT Labgis System

  
## Description
```
O repositório contém codigos em python para  auxiliar a aquisição das imagens de satelites(Landsat Explorer e Sentinel Explorer).
Ferramenta opensource potencializa de maneira prática as metodologias para geração de produtos derivados de imagens de sensores remotos de baixo custo ou gratuitas.
```

## Features
```
O código possui os recursos listados abaixo.

* Pesquisa das imagens de satélite no catálogo da Espacial Européria (ESA) e do Serviço Geológico Americano (USGS).

* Geração de um arquivo de texto com os ids das imagens buscadas.

* Download automático a partir do arquivo de texto, ao qual contém os ids necessários para download.

*Gera um arquivo de texto com os logins do usuário

```


## Requirements
```
Referente aos códigos, necessita dos itens abaixo.

Necessário a  instalação da [API Python Sentinelsat](https://pypi.org/project/sentinelsat/).
```

### Python Library
```
Utiliza os pacotes de python  [Urllib](https://pypi.org/project/urllib3/), [json](https://pypi.org/project/jsonlib/), [threaded](https://pypi.org/project/threaded/), [csv](https://pypi.org/project/csvfile/), [requets](https://pypi.org/project/requests/), [time](https://pypi.org/project/times/), [path](https://pypi.org/project/times/).
```

## Contributing
```
A equipe Labgis agradece a contribuição de qualquer pessoa, desde que seja para aprimorar.
```

## Usage e Documentation
```
O código pesquisa_landsat_.py realiza a pesquisa das imagens pelos parâmetros requeridos pela  doumentação 
da [USGS](https://m2m.cr.usgs.gov/api/docs/reference/#scene-search), 
por meio da inserção opcional de localização, data, porcentagem de nuvem dentre outras. 
Ademais, posteriormente após o fim da busca é agrupados todos os ids(leia-se nomes delas) das imagens em um arquivo 
de texto, ao qual são utlizados para baixar as imagens no código download_landsat.py
 
Conjuntamente é carregado o acesso_py.py, ao qual realiza a interação com o usuário no quesito login, 
em que são pedidos o login e a senha para acesso ao site. Posteriormente esse login é salvo em arquivo de texto
na máquina do usuário, criptografado, garantido a segurança das credenciais e o sigilo. Essas informações são utilizadas 
no código de pesquisa principal.

O código pesquisa_sentinelsat.py busca as imagens pelos pelos parametros requeridos pela doumentação da 
[ESA](https://sentinelsat.readthedocs.io/en/v0.9.1/api.html),
através da inserção de localização, data, porcentagem de nuvem dentre outras.
Ademais, posteriormente após o fim da busca é agrupados todos os ids das imagens em um arquivo de texto,
ao qual são utlizados para baixar as imagens no código download_sentinelsat.py.
```
### Example
#### Pesquisa geral de solicitações de amostra
```
{
    "maxResults": 100,
    "datasetName": "gls_all",
    "sceneFilter": {
        "ingestFilter": null,
        "spatialFilter": null,
        "metadataFilter": null,
        "cloudCoverFilter": {
            "max": 100,
            "min": 0,
            "includeUnknown": true
        },
        "acquisitionFilter": null
    }
    
}

