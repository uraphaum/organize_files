import os
import shutil
import json
import argparse
from pathlib import Path
from datetime import datetime

CATEGORIAS = {
    # Imagens
    ".jpg": "Imagens", ".jpeg": "Imagens", ".png": "Imagens",
    ".gif": "Imagens", ".bmp": "Imagens", ".svg": "Imagens",
    ".webp": "Imagens", ".ico": "Imagens",
    # Vídeos
    ".mp4": "Videos", ".mkv": "Videos", ".avi": "Videos",
    ".mov": "Videos", ".wmv": "Videos", ".flv": "Videos",
    # Áudios
    ".mp3": "Audios", ".wav": "Audios", ".flac": "Audios",
    ".aac": "Audios", ".ogg": "Audios",
    # Documentos
    ".pdf": "Documentos", ".doc": "Documentos", ".docx": "Documentos",
    ".xls": "Documentos", ".xlsx": "Documentos", ".ppt": "Documentos",
    ".pptx": "Documentos", ".txt": "Documentos", ".odt": "Documentos",
    # Código
    ".py": "Codigo", ".js": "Codigo", ".ts": "Codigo",
    ".html": "Codigo", ".css": "Codigo", ".json": "Codigo",
    ".xml": "Codigo", ".yaml": "Codigo", ".yml": "Codigo",
    ".sh": "Codigo", ".bat": "Codigo", ".c": "Codigo",
    ".cpp": "Codigo", ".java": "Codigo", ".rs": "Codigo",
    # Compactados
    ".zip": "Compactados", ".rar": "Compactados", ".tar": "Compactados",
    ".gz": "Compactados", ".7z": "Compactados",
    # Executáveis / instaladores
    ".exe": "Programas", ".msi": "Programas", ".deb": "Programas",
    ".AppImage": "Programas",
    # Fontes
    ".ttf": "Fontes", ".otf": "Fontes", ".woff": "Fontes", ".woff2": "Fontes",
}

LOG_FILE = ".organizer_log.json"


def organizar(pasta: Path, dry_run: bool = False) -> None:
    """Move os arquivos da pasta para subpastas por categoria."""

    if not pasta.exists() or not pasta.is_dir():
        print(f"Pasta não encontrada: {pasta}")
        return

    arquivos = [f for f in pasta.iterdir() if f.is_file() and f.name != LOG_FILE]

    if not arquivos:
        print("Nenhum arquivo encontrado para organizar.")
        return

    log = {"data": datetime.now().isoformat(), "movimentos": []}
    contador = 0

    print(f"\nOrganizando: {pasta.resolve()}")
    print("─" * 50)

    for arquivo in sorted(arquivos):
        extensao = arquivo.suffix.lower()
        categoria = CATEGORIAS.get(extensao, "Outros")
        destino_dir = pasta / categoria
        destino = destino_dir / arquivo.name

        # Evita sobrescrever arquivos com o mesmo nome
        if destino.exists():
            stem = arquivo.stem
            sufixo = arquivo.suffix
            i = 1
            while destino.exists():
                destino = destino_dir / f"{stem}_{i}{sufixo}"
                i += 1

        acao = f"  {arquivo.name:35s} → {categoria}/"
        print(acao)

        if not dry_run:
            destino_dir.mkdir(exist_ok=True)
            shutil.move(str(arquivo), str(destino))
            log["movimentos"].append({
                "origem": str(arquivo),
                "destino": str(destino),
            })
            contador += 1

    if not dry_run:
        log_path = pasta / LOG_FILE
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=2)
        print("─" * 50)
        print(f"\n {contador} arquivo(s) organizado(s)!")
        print(f" Log salvo em: {log_path.name}\n")
    else:
        print("─" * 50)
        print("\n Simulação concluída (nenhum arquivo foi movido).\n")


def desfazer(pasta: Path) -> None:
    """Reverte os movimentos registrados no log."""

    log_path = pasta / LOG_FILE

    if not log_path.exists():
        print("  Nenhum log de organização encontrado nesta pasta.")
        return

    with open(log_path, "r", encoding="utf-8") as f:
        log = json.load(f)

    movimentos = log.get("movimentos", [])

    if not movimentos:
        print(" Log vazio, nada para desfazer.")
        return

    print(f"\n Desfazendo organização de {log['data'][:10]}...")
    print("─" * 50)

    restaurados = 0
    for mov in reversed(movimentos):
        origem = Path(mov["origem"])
        destino = Path(mov["destino"])

        if destino.exists():
            origem.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(destino), str(origem))
            print(f"  ← {destino.name}")
            restaurados += 1
        else:
            print(f"  Não encontrado: {destino.name}")

    # Remove pastas vazias criadas
    for categoria in set(CATEGORIAS.values()) | {"Outros"}:
        cat_dir = pasta / categoria
        if cat_dir.exists() and not any(cat_dir.iterdir()):
            cat_dir.rmdir()

    log_path.unlink()
    print("─" * 50)
    print(f"\n✅  {restaurados} arquivo(s) restaurado(s)!\n")


def main():
    parser = argparse.ArgumentParser(
        description="Organiza arquivos de uma pasta por tipo/extensão.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "pasta",
        nargs="?",
        default=".",
        help="Caminho da pasta a organizar (padrão: pasta atual)",
    )
    parser.add_argument(
        "--desfazer",
        action="store_true",
        help="Desfaz a última organização usando o log salvo",
    )
    parser.add_argument(
        "--simular",
        action="store_true",
        help="Mostra o que seria feito sem mover nenhum arquivo",
    )

    args = parser.parse_args()
    pasta = Path(args.pasta)

    if args.desfazer:
        desfazer(pasta)
    else:
        organizar(pasta, dry_run=args.simular)


if __name__ == "__main__":
    main()
