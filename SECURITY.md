# Security policy

## Supported versions

Security reports are welcome for the latest release and the default development branch. This is a small early-stage utility and does not have a dedicated security response team.

## Reporting a concern

Do not post an exploit, sensitive document, or private data in a public issue. Contact the repository owner through GitHub's private contact options and include a concise description, affected version, and steps to reproduce that do not expose private files.

## Safe use

BanglaPDFCheck processes local PDF files with a third-party parser. Parsing malformed files can consume significant resources. Only process documents you trust, and avoid running the tool on unusually large or suspicious files in resource-constrained environments. The tool does not upload files, but it is not a PDF sandbox or malware scanner.
