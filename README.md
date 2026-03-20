# Build applications with GitHub Copilot agent mode

<!-- ![](../../actions/workflows/0-start-course.yml/badge.svg?branch=main) -->
<img src="https://github.com/user-attachments/assets/1b3ea5df-f18d-4ed8-9ae6-f96dc1861818" alt="octofit-tracker" width="300"/>

_Build an application with GitHub Copilot agent mode in less than an hour._

## Welcome

People love how GitHub Copilot helps them write code faster and with fewer errors.
But what if GitHub could create a multi-tier application with a presentation, logic, and data layers based on requirements written in natural language?
In this exercise, we will prompt GitHub Copilot agent mode to create a complete application.

- **Who is this for**: Intermediate developers familiar with GitHub Copilot, basic GitHub, and basic web development
- **What you'll learn**: We'll introduce GitHub Copilot agent mode and how to use it for application development.
- **What you'll build**: You'll use GitHub Copilot agent mode to create a fitness application as the gym teacher of a high school.
- **Prerequisites**: Skills Exercise: <a href="https://github.com/skills/getting-started-with-github-copilot">Getting Started with GitHub Copilot</a>.
- **How long**: This course takes less than one hour to complete.

In this exercise, you will:

1. Start up a preconfigured development environment for making a multi-tier application.
1. Prompt in GitHub Copilot Chat and select the edit tab and select agent mode from the edit/agent drop-down.
1. In this exercise I primarily used the latest default LLM.
1. Try other LLM models to see other output.
1. For each step open up a new Copilot Chat session by hitting the plus `+` icon in the Copilot Chat pane.

---

## 🗄️ Oracle Database & SQL Developer Integration

El proyecto incluye una **base de datos Oracle 21C** con el esquema **GYM_APP** y soporte completo para **SQL Developer**.

### 📚 Documentación Rápida

| Recurso | Descripción |
|---------|-------------|
| [QUICKSTART.md](oracle_db/QUICKSTART.md) | ⭐ **Guía rápida** con checklist de 10 pasos |
| [STRUCTURE.md](oracle_db/STRUCTURE.md) | Estructura de archivos y diagrama visual |
| [oracle_db/README.md](oracle_db/README.md) | Documentación técnica completa |
| [.github/instructions/ORACLE_SQLDEVELOPER.instructions.md](.github/instructions/ORACLE_SQLDEVELOPER.instructions.md) | Instrucciones detalladas para SQL Developer |
| [oracle_db/sql/queries_example.sql](oracle_db/sql/queries_example.sql) | Ejemplos de queries útiles |

### 🚀 Inicio Rápido (3 min)

```bash
# 1. Descargar SQL Developer
wget https://download.oracle.com/otn/java/sqldeveloper/sqldeveloper-23.1.0.087.1900-no-jdk.zip
unzip sqldeveloper-23.1.0.087.1900-no-jdk.zip
./sqldeveloper/sqldeveloper.sh

# 2. En SQL Developer:
# - Crear conexión SYSDBA (localhost:1521, ORCLCDB, sys)
# - Ejecutar: oracle_db/sql/00_create_schema.sql
# - Crear conexión GYM_APP (usuario: GYM_APP, password: gym_app_password)
# - Ejecutar: oracle_db/sql/01_create_tables.sql
# - Ejecutar: oracle_db/sql/02_create_procedures.sql
```

### 📁 Estructura Oracle

```
octofit-tracker/backend/
├── .env (ORACLE_DB_USER=GYM_APP)
└── octofit_tracker/settings.py (DATABASES config)

oracle_db/
├── QUICKSTART.md ⭐ Comienza aquí
├── STRUCTURE.md
├── README.md
└── sql/
    ├── 00_create_schema.sql (Crear GYM_APP)
    ├── 01_create_tables.sql (6 tablas)
    ├── 02_create_procedures.sql (4 procedimientos)
    └── queries_example.sql (Ejemplos)
```

**Estatus:** ✅ Listo para usar

---

### How to start this exercise

Simply copy the exercise to your account, then give your favorite Octocat (Mona) **about 20 seconds** to prepare the first lesson, then **refresh the page**.

[![](https://img.shields.io/badge/Copy%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github&labelColor=197935)](https://github.com/new?template_owner=skills&template_name=build-applications-w-copilot-agent-mode&owner=%40me&name=skills-build-applications-w-copilot-agent-mode&description=Exercise:+Build+applications+with+GitHub+Copilot+agent+mode&visibility=public)

<details>
<summary>Having trouble? 🤷</summary><br/>

When copying the exercise, we recommend the following settings:

- For owner, choose your personal account or an organization to host the repository.

- We recommend creating a public repository, since private repositories will use Actions minutes.

If the exercise isn't ready in 20 seconds, please check the "Actions" tab of your repository (or visit `https://github.com/<YOUR-USERNAME>/<YOUR-REPO>/actions`).

- Check to see if a job is running. Sometimes it simply takes a bit longer.

- If the page shows a failed job, please submit an issue. Nice, you found a bug! 🐛

</details>

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)
