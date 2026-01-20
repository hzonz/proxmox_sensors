class ProxmoxPanel extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
            <style>
                .wrapper {
                    padding: 24px;
                    font-family: sans-serif;
                }
                h1 {
                    font-size: 28px;
                    margin-bottom: 12px;
                }
                p {
                    font-size: 16px;
                    opacity: 0.8;
                }
            </style>

            <div class="wrapper">
                <h1>Panel Proxmox</h1>
                <p>El panel se ha cargado correctamente.</p>
                <p>Versión del panel: __PANEL_VERSION__</p>
            </div>
        `;
    }
}

customElements.define("proxmox-panel", ProxmoxPanel);
