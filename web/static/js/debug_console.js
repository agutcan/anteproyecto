/**
 * Debug Console - Consola interactiva para ejecutar consultas ORM en desarrollo
 * Activarse presionando F12 en la página
 */

class DebugConsole {
    constructor() {
        this.isOpen = false;
        this.isLoading = false;
        this.history = [];
        this.historyIndex = -1;
        this.init();
    }

    /**
     * Inicializa la consola: crea elementos DOM y configura listeners
     */
    init() {
        // Crear HTML
        this.createDOM();

        // Event listeners
        document.addEventListener("keydown", (e) => this.handleKeydown(e));
        this.closeBtn.addEventListener("click", () => this.close());
        this.backdrop.addEventListener("click", () => this.close());
        this.executeBtn.addEventListener("click", () => this.execute());
        this.clearBtn.addEventListener("click", () => this.clearOutput());

        // Permitir Submit con Enter en el textarea
        this.queryInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && e.ctrlKey) {
                this.execute();
            }
        });

        // Historia de consultas con flechas
        this.queryInput.addEventListener("keydown", (e) => {
            if (e.key === "ArrowUp") {
                e.preventDefault();
                this.showPreviousQuery();
            } else if (e.key === "ArrowDown") {
                e.preventDefault();
                this.showNextQuery();
            }
        });
    }

    /**
     * Crea los elementos DOM de la consola
     */
    createDOM() {
        // Backdrop
        this.backdrop = document.createElement("div");
        this.backdrop.className = "debug-console-backdrop";

        // Contenedor principal
        this.dialog = document.createElement("div");
        this.dialog.className = "debug-console-dialog";

        // Header
        const header = document.createElement("div");
        header.className = "debug-console-header";
        header.innerHTML = '<h3>🔧 Consola de Depuración (ORM Queries)</h3>';

        this.closeBtn = document.createElement("button");
        this.closeBtn.className = "debug-console-close";
        this.closeBtn.innerHTML = "✕";
        header.appendChild(this.closeBtn);

        // Body
        const body = document.createElement("div");
        body.className = "debug-console-body";

        // Input Area
        const inputArea = document.createElement("div");
        inputArea.className = "debug-console-input-area";

        const queryLabel = document.createElement("label");
        queryLabel.className = "debug-console-label";
        queryLabel.textContent = "Consulta ORM (Python/Django):";

        this.queryInput = document.createElement("textarea");
        this.queryInput.className = "debug-console-query";
        this.queryInput.placeholder =
            "Ej: list(Player.objects.values('username', 'country')[:5])";
        this.queryInput.spellcheck = false;

        // Options
        const options = document.createElement("div");
        options.className = "debug-console-options";

        const evalLabel = document.createElement("label");
        evalLabel.style.display = "flex";
        evalLabel.style.alignItems = "center";
        evalLabel.style.gap = "6px";
        evalLabel.style.cursor = "pointer";

        this.evalCheckbox = document.createElement("input");
        this.evalCheckbox.type = "checkbox";
        this.evalCheckbox.className = "debug-console-checkbox";
        this.evalCheckbox.checked = true;

        evalLabel.appendChild(this.evalCheckbox);
        evalLabel.appendChild(document.createTextNode("Modo eval (devuelve resultado)"));

        options.appendChild(evalLabel);

        inputArea.appendChild(queryLabel);
        inputArea.appendChild(this.queryInput);
        inputArea.appendChild(options);

        // Output Area
        const outputLabel = document.createElement("label");
        outputLabel.className = "debug-console-label";
        outputLabel.style.marginTop = "8px";
        outputLabel.textContent = "Resultado:";

        this.outputArea = document.createElement("div");
        this.outputArea.className = "debug-console-output-area";

        // Buttons
        const buttons = document.createElement("div");
        buttons.className = "debug-console-buttons";

        this.executeBtn = document.createElement("button");
        this.executeBtn.className = "debug-console-btn";
        this.executeBtn.textContent = "Ejecutar (Ctrl+Enter)";

        this.clearBtn = document.createElement("button");
        this.clearBtn.className = "debug-console-btn clear";
        this.clearBtn.textContent = "Limpiar Output";

        buttons.appendChild(this.executeBtn);
        buttons.appendChild(this.clearBtn);

        // Ensamblar
        body.appendChild(inputArea);
        body.appendChild(outputLabel);
        body.appendChild(this.outputArea);
        body.appendChild(buttons);

        this.dialog.appendChild(header);
        this.dialog.appendChild(body);

        document.body.appendChild(this.backdrop);
        document.body.appendChild(this.dialog);
    }

    /**
     * Maneja los eventos de teclado
     */
    handleKeydown(e) {
        // F8 para abrir/cerrar
        if (e.key === "F12" && e.shiftKey === false && e.ctrlKey === false && e.altKey === false) {
            e.preventDefault();
            this.toggle();
        }

        // Escape para cerrar
        if (e.key === "Escape" && this.isOpen) {
            this.close();
        }
    }

    /**
     * Alterna la visibilidad de la consola
     */
    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    /**
     * Abre la consola
     */
    open() {
        this.isOpen = true;
        this.backdrop.classList.add("active");
        this.dialog.classList.add("active");
        this.queryInput.focus();
    }

    /**
     * Cierra la consola
     */
    close() {
        this.isOpen = false;
        this.backdrop.classList.remove("active");
        this.dialog.classList.remove("active");
    }

    /**
     * Ejecuta la consulta ORM
     */
    async execute() {
        const query = this.queryInput.value.trim();

        if (!query) {
            this.addOutput("Por favor ingresa una consulta", "error");
            return;
        }

        if (this.isLoading) {
            return;
        }

        // Guardar en historia
        if (this.history[this.history.length - 1] !== query) {
            this.history.push(query);
            this.historyIndex = this.history.length;
        }

        this.isLoading = true;
        this.executeBtn.disabled = true;

        try {
            const response = await fetch("/api/debug/query/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": this.getCookie("csrftoken"),
                },
                body: JSON.stringify({
                    query: query,
                    eval: this.evalCheckbox.checked,
                }),
            });

            const data = await response.json();

            if (data.success) {
                this.addOutput(
                    `✅ Éxito:\n${data.result}`,
                    "success",
                    query
                );
            } else {
                this.addOutput(
                    `❌ Error:\n${data.error}`,
                    "error",
                    query
                );
            }
        } catch (error) {
            this.addOutput(
                `❌ Error de red:\n${error.message}`,
                "error",
                query
            );
        } finally {
            this.isLoading = false;
            this.executeBtn.disabled = false;
        }
    }

    /**
     * Añade un resultado al área de output
     */
    addOutput(result, type = "success", query = null) {
        const resultDiv = document.createElement("div");
        resultDiv.className = `debug-console-result ${type}`;

        if (query) {
            const queryLabel = document.createElement("div");
            queryLabel.className = "debug-console-result-label";
            queryLabel.textContent = `Query: ${query.substring(0, 50)}${query.length > 50 ? "..." : ""}`;
            resultDiv.appendChild(queryLabel);
        }

        const content = document.createElement("div");
        content.className = "debug-console-result-content";
        content.textContent = result;

        resultDiv.appendChild(content);
        this.outputArea.appendChild(resultDiv);

        // Auto-scroll al final
        this.outputArea.scrollTop = this.outputArea.scrollHeight;
    }

    /**
     * Limpia el área de output
     */
    clearOutput() {
        this.outputArea.innerHTML = "";
        this.addOutput("Output limpiado ✓", "success");
    }

    /**
     * Muestra la consulta anterior en el historial
     */
    showPreviousQuery() {
        if (this.history.length === 0) return;

        if (this.historyIndex > 0) {
            this.historyIndex--;
            this.queryInput.value = this.history[this.historyIndex];
        }
    }

    /**
     * Muestra la siguiente consulta en el historial
     */
    showNextQuery() {
        if (this.history.length === 0) return;

        if (this.historyIndex < this.history.length - 1) {
            this.historyIndex++;
            this.queryInput.value = this.history[this.historyIndex];
        } else if (this.historyIndex === this.history.length - 1) {
            this.historyIndex = this.history.length;
            this.queryInput.value = "";
        }
    }

    /**
     * Obtiene una cookie CSRF
     */
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", () => {
    window.debugConsole = new DebugConsole();
    console.log("Debug Console iniciada. Presiona F12 para abrir.");
});
