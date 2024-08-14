# globo-programming-api
Consulta programação da TV Globo.

## Obtenha um API Token em ScrapingAnt

Para usar a globo-programming-api, é necessário um token de API do ScrapingAnt para contornar verificações anti-webscraping.

O ScrapingAnt fornece 1.000 consultas gratuitas por mês.

Você pode criar uma conta em [ScrapingAnt][scrapingant] e obter seu token API lá.

## Instalação das dependências

```
pip install -r requirements.txt
```

## Iniciar o servidor

```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Via Docker

```
docker run --name globo-programming-api -e SA_TOKENS="token1,token2,token3" -p 8000:8000 juniorkrz/globo-programming-api
```

Lembre-se de substituir `"token1,token2,token3"` pelos seus tokens reais, separados por vírgula. Você pode adicionar quantos tokens forem necessários.

## Descrição
Este projeto permite realizar consultas na programação da TV Glovo. Ele oferece as seguintes funcionalidades:

- Obter a lista de canais completa.
- Obter a programação de um canal específico.

## Endpoints

## /channels

Obtém a lista de canais completa.

## /channel_programs/{name}

Realiza a consulta da programação do canal informado.

Confira todos os canais disponíveis [aqui][channels].

## Autor
- [Antônio Roberto Júnior][krz]

## Licença

Este projeto está licenciado sob a [MIT License][license].

[krz]: https://github.com/juniorkrz
[license]: https://github.com/juniorkrz/globo-programming-api/blob/master/LICENSE
[scrapingant]: https://scrapingant.com
[channels]: ./docs/Channels.MD