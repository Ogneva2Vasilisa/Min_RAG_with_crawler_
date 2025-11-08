#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
from scripts.model_init import get_embedder
from scripts.pdf_loader import add_pdfs_to_faiss_main
from scripts.url_loader import crawl_and_update_faiss
from scripts.rag import start_rag_bot

DEFAULT_OUT = "kb_output"

def main():
    parser = argparse.ArgumentParser(description="RAG KB manager")
    subparsers = parser.add_subparsers(dest="command")

    # PDF
    pdf_parser = subparsers.add_parser("pdf", help="Добавить PDF в FAISS")
    pdf_parser.add_argument("--pdf_dir", "-p", required=True, help="Directory with PDF files")
    pdf_parser.add_argument("--out", "-o", default=DEFAULT_OUT, help="Output folder")

    # URL
    url_parser = subparsers.add_parser("url", help="Обойти URL и обновить FAISS")
    url_parser.add_argument("--seeds", "-s", required=True, help="Seed URLs file")
    url_parser.add_argument("--out", "-o", default=DEFAULT_OUT, help="Output folder")
    url_parser.add_argument("--max_pages", "-m", type=int, default=100, help="Max pages to crawl")
    url_parser.add_argument("--delay", "-d", type=float, default=0.2, help="Delay between requests")

    # Chat
    chat_parser = subparsers.add_parser("chat", help="Запуск RAG бота")
    chat_parser.add_argument("--out", "-o", default=DEFAULT_OUT, help="FAISS folder")

    args = parser.parse_args()
    embedder = get_embedder()

    if args.command == "pdf":
        pdf_dir = Path(args.pdf_dir)
        add_pdfs_to_faiss_main(pdf_dir, args.out, embedder)

    elif args.command == "url":
        crawl_and_update_faiss(embedder, args.seeds, args.out, max_pages=args.max_pages, delay=args.delay)

    elif args.command == "chat":
        start_rag_bot(embedder, Path(args.out))

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
