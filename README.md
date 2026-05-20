# Chaos WA Ultimate 

<p align="center">

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat&logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-11-0078D6?style=flat&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)
![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)

</p>

Simulador de grupo de WhatsApp caótico poblado por bots de IA que discuten, se ignoran, insultan y envían stickers cursed.

**"Los Pendejos de Silicio"** es un experimento de interacción multi‑agente con personalidades definidas, filtros anti‑asistente y memoria social tóxica.  
Los bots **NO** ayudan, **NO** explican cosas y **NO** son amables. Solo generan caos realista en tiempo real.

---

## Características

- **4 bots independientes** con modelos de Ollama distintos y personalidades opuestas.
- **Interfaz gráfica** (tkinter) estilo chat, con burbujas alineadas a la izquierda/derecha.
- **Filtro de salida**: elimina cualquier rastro de asistente, roleplay, romanticismo o párrafos largos.
- **Sistema de decisiones**: cada bot decide si responder según su humor, su relación con el autor y el contenido del chat.
- **Mensajes espontáneos**: cuando el grupo está inactivo, los bots pueden mandar “xd”, stickers falsos o eventos eliminados.
- **Logs estructurados**: todas las interacciones se registran en `chat_logs.jsonl` con timestamp, nivel y payload.
- **Comportamiento dinámico**: los bots se aburren, cambian de humor y pueden ignorar al usuario o a otros bots.
- **Totalmente local**: todo corre en tu máquina con Ollama.

---

## Requisitos

- Python 3.14 o superior
- [Ollama](https://ollama.com/) instalado y corriendo
- Modelos de Ollama descargados:
  - `qwen2.5:7b` (usado por Pedro y Carlos)
  - `gemma:2b` (usado por Ana)
  - `phi4-mini:latest` (usado por Laura)

Para cambiar los modelos que usa, puedes modificar ``chaos_engine.py`` en la sección de ``self.bot()``

Puedes descargarlos con:
```bash
ollama pull qwen2.5:7b
ollama pull gemma:2b
ollama pull phi4-mini:latest
```

---
## Modificaciones al codigo

El codigo está bajo una MIT License, si hay algún error o modificación que quieras añadir al proyecto, abre un Issue o empieza un Pull Request
