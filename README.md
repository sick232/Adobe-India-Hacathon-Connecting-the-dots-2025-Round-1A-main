-----

# **Adobe India Hackathon 2025 - Round 1A**

This repository contains a Dockerized solution for Round 1A of the Adobe India Hackathon 2025. It extracts a structured outline (Title, H1, H2, H3) from PDF files and outputs the result as JSON.

## **Getting Started**

To get started with the project, follow these steps:

**1. Setup the Project**

First, ensure you have **Docker Desktop** installed and running. Next, clone the repository and arrange your project files in the following structure:

```graphql
.
├── Dockerfile
├── process_pdfs.py
├── requirements.txt
├── input/          # Place your PDF files here
└── output/         # JSON output will be generated here
```

**2. Build the Docker Image**

Navigate to the project's root directory in your terminal and run the following command to build the Docker image.

```bash
docker build --platform linux/amd64 -t my-adobe-solution:1.0 .
```

**3. Run the Docker Container**

After the build is complete, use this command to run the container. It will process all PDFs from the `input` folder and save the results to the `output` folder.

```bash
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" --network none my-adobe-solution:1.0
```

> **Note for Windows Users:** If `$(pwd)` causes issues in PowerShell, replace it with the full, absolute path to your project folders.

## **Output Format**

The generated JSON files will be placed in the `/output` directory. Each file will have the following structure:

```json
{
  "title": "Sample Document Title",
  "h1": ["Introduction", "Chapter 1"],
  "h2": ["Background", "Methodology"],
  "h3": ["Section 1.1", "Section 2.1"]
}
```

## **Authors**

  * Mayank Chauhan
  * Adithya Sankar Menon
  * Piyush Maurya
