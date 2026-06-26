# organize_files

Uma ferramenta de linha de comando que organiza automaticamente os arquivos de uma pasta, separando-os em subpastas por tipo.

Fiz esse projeto para estudar mais sobre manipulação de arquivos com Python, uso do módulo `pathlib`, criação de CLIs com `argparse`, e como estruturar um script pequeno de forma que outras pessoas consigam usar e entender com facilidade.

---

## Como usar

```bash
# Aqui inicia o Código, e é Organizado a Pasta atual.
python organize_files.py

# Organiza uma Pasta Especificada
python organize_files.py ~/Downloads

# Uma Simulação, Sem Mover nenhum Arquivo
python organize_files.py ~/Downloads --simular

# Desfaz a Última Organização feita
python organize_files.py ~/Downloads --desfazer
```

---

## Categorias reconhecidas

| Pasta       | Extensões                                  |
|-------------|--------------------------------------------|
| Imagens     | .jpg, .jpeg, .png, .gif, .svg, .webp, ... |
| Videos      | .mp4, .mkv, .avi, .mov, ...               |
| Audios      | .mp3, .wav, .flac, .aac, ...              |
| Documentos  | .pdf, .docx, .xlsx, .txt, ...             |
| Codigo      | .py, .js, .html, .css, .json, ...         |
| Compactados | .zip, .rar, .tar, .gz, .7z                |
| Programas   | .exe, .msi, .deb, .AppImage               |
| Fontes      | .ttf, .otf, .woff, .woff2                 |
| Outros      | qualquer extensão não mapeada              |

Arquivos com nomes duplicados no destino são renomeados automaticamente.

---

## Como funciona o desfazer

Cada vez que a organização roda, um arquivo `.organizer_log.json` é salvo na pasta com o registro de tudo que foi movido. O modo `--desfazer` lê esse log e restaura cada arquivo para o lugar original, removendo as subpastas criadas caso estejam vazias.

---

## Requisitos

- Python 3.6+
- Sem dependências externas

---

Desenvolvido com Carinho por Raphaum! 🌸
