const CARD_VERSION = "1.0.0";

const EMBEDDED_FONT_CSS = `@font-face {
  font-family: "Brighton Dot Matrix";
  src: url("data:font/woff2;base64,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") format("woff2");
  font-style: normal;
  font-weight: 400;
  font-display: swap;
}
@font-face {
  font-family: "Brighton Dot Matrix";
  src: url("data:font/woff2;base64,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") format("woff2");
  font-style: normal;
  font-weight: 700;
  font-display: swap;
}`;
const FONT_STYLE_ID = "brighton-bus-times-embedded-fonts";

const injectEmbeddedFonts = () => {
  if (document.getElementById(FONT_STYLE_ID)) return;

  const style = document.createElement("style");
  style.id = FONT_STYLE_ID;
  style.textContent = EMBEDDED_FONT_CSS;
  document.head.appendChild(style);
};

injectEmbeddedFonts();

const escapeHtml = (value) =>
  String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

const DEFAULT_LED_COLOR = "#ffad32";

const normaliseColor = (value) => {
  const color = String(value || "").trim();
  return /^#[0-9a-f]{6}$/i.test(color) ? color.toLowerCase() : DEFAULT_LED_COLOR;
};

const shadeColor = (color, factor) => {
  const value = normaliseColor(color).slice(1);
  const channels = [0, 2, 4].map((offset) =>
    Math.round(parseInt(value.slice(offset, offset + 2), 16) * factor)
      .toString(16)
      .padStart(2, "0")
  );
  return `#${channels.join("")}`;
};

class BrightonBusTimesCard extends HTMLElement {
  static getConfigElement() {
    return document.createElement("brighton-bus-times-card-editor");
  }

  static getStubConfig(hass, entities) {
    const entity = (entities || []).find((entityId) =>
      entityId.includes("next_departure")
    );
    return { entity: entity || "", departures: 5 };
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error("Select a Brighton Bus Times sensor");
    }
    this.config = {
      departures: 5,
      show_status: true,
      color: DEFAULT_LED_COLOR,
      ...config,
    };
    this.render();
  }

  set hass(hass) {
    this._hass = hass;
    this.render();
  }

  getCardSize() {
    return Math.max(3, Number(this.config?.departures || 5) + 1);
  }

  render() {
    if (!this.config || !this._hass) return;

    const state = this._hass.states[this.config.entity];
    if (!state) {
      this.innerHTML = `<ha-card><div class="missing">Entity not found: ${escapeHtml(
        this.config.entity
      )}</div></ha-card>`;
      return;
    }

    const attributes = state.attributes || {};
    const departures = Array.isArray(attributes.departures)
      ? attributes.departures.slice(0, Number(this.config.departures || 5))
      : [];
    const title =
      this.config.title ||
      attributes.stop_name ||
      attributes.friendly_name ||
      this.config.entity;
    const updated = attributes.last_updated
      ? String(attributes.last_updated).slice(11, 16)
      : "--:--";
    const ledColor = normaliseColor(this.config.color);
    const dimLedColor = shadeColor(ledColor, 0.68);

    const rows = departures.length
      ? departures
          .map((departure) => {
            const live = departure.is_live === true;
            const eta = departure.eta_display ??
              (departure.eta_minutes === 0
                ? "Due"
                : `${departure.eta_minutes ?? "—"} mins`);
            const status = this.config.show_status
              ? `<span class="status ${live ? "live" : "scheduled"}">${
                  live ? "LIVE" : "SCHED"
                }</span>`
              : "";

            return `
              <div class="departure-row">
                <span class="route">${escapeHtml(departure.route || "—")}</span>
                <span class="destination">${escapeHtml(
                  departure.destination || "Destination unavailable"
                )}</span>
                ${status}
                <span class="eta">${escapeHtml(eta)}</span>
              </div>`;
          })
          .join("")
      : `<div class="empty">NO DEPARTURES AVAILABLE</div>`;

    this.innerHTML = `
      <ha-card>
        <div class="sign" role="region" aria-label="Bus departures for ${escapeHtml(
          title
        )}">
          <div class="header">
            <span class="stop-name">${escapeHtml(title)}</span>
            <span class="updated">UPDATED ${escapeHtml(updated)}</span>
          </div>
          <div class="column-headings">
            <span>BUS</span><span>DESTINATION</span><span></span><span>DUE</span>
          </div>
          <div class="departures">${rows}</div>
          <div class="footer">REAL-TIME BUS INFORMATION</div>
        </div>
      </ha-card>
      <style>
        ha-card {
          overflow: hidden;
          background: #080a09;
          border: 8px solid #242826;
          border-radius: 10px;
          box-shadow: inset 0 0 0 2px #000, 0 3px 12px rgba(0, 0, 0, .38);
        }
        .sign {
          --amber: ${ledColor};
          --dim-amber: ${dimLedColor};
          position: relative;
          padding: 14px 15px 10px;
          color: var(--amber);
          background-color: #070908;
          background-image: radial-gradient(color-mix(in srgb, var(--amber) 8%, transparent) .7px, transparent .9px);
          background-size: 4px 4px;
          font-family: "Brighton Dot Matrix", "Courier New", monospace;
          font-weight: 400;
          letter-spacing: .035em;
          text-transform: uppercase;
          text-shadow: 0 0 1px var(--dim-amber);
        }
        .header, .departure-row, .column-headings {
          display: grid;
          grid-template-columns: minmax(48px, .58fr) minmax(120px, 3fr) auto minmax(58px, .85fr);
          align-items: center;
          gap: 9px;
        }
        .header {
          grid-template-columns: 1fr auto;
          padding-bottom: 10px;
          border-bottom: 1px solid color-mix(in srgb, var(--amber) 46%, transparent);
        }
        .stop-name {
          overflow: hidden;
          font-size: 1.14rem;
          font-weight: 700;
          white-space: nowrap;
          text-overflow: ellipsis;
        }
        .updated, .column-headings, .footer {
          color: var(--dim-amber);
          font-size: .66rem;
          letter-spacing: .09em;
        }
        .column-headings {
          padding: 8px 0 4px;
        }
        .column-headings span:last-child { text-align: right; }
        .departure-row {
          min-height: 42px;
          border-top: 1px dotted color-mix(in srgb, var(--amber) 24%, transparent);
        }
        .route {
          font-size: 1.24rem;
          white-space: nowrap;
        }
        .destination {
          overflow: hidden;
          font-size: 1rem;
          white-space: nowrap;
          text-overflow: ellipsis;
        }
        .eta {
          grid-column: 4;
          justify-self: end;
          font-size: 1rem;
          text-align: right;
          white-space: nowrap;
        }
        .status {
          padding: 2px 4px;
          border: 1px solid currentColor;
          border-radius: 2px;
          font-size: .57rem;
          line-height: 1;
          letter-spacing: .05em;
          text-shadow: none;
        }
        .status.live { color: var(--amber); }
        .status.scheduled { color: var(--dim-amber); }
        .empty {
          padding: 25px 5px;
          text-align: center;
        }
        .footer {
          padding-top: 9px;
          text-align: right;
        }
        .missing {
          padding: 16px;
        }
        @media (max-width: 480px) {
          .sign { padding: 11px 10px 8px; }
          .departure-row, .column-headings {
            grid-template-columns: 43px minmax(80px, 1fr) minmax(53px, auto);
            gap: 6px;
          }
          .header {
            grid-template-columns: minmax(0, 1fr);
            gap: 0;
          }
          .stop-name {
            overflow: visible;
            font-size: 1rem;
            line-height: 1.2;
            white-space: normal;
            overflow-wrap: anywhere;
            text-overflow: clip;
          }
          .departure-row .status, .column-headings span:nth-child(3) { display: none; }
          .eta { grid-column: 3; }
          .destination, .eta { font-size: .86rem; }
          .route { font-size: 1.05rem; }
          .updated { display: none; }
        }
      </style>`;
  }
}

class BrightonBusTimesCardEditor extends HTMLElement {
  setConfig(config) {
    this.config = {
      departures: 5,
      show_status: true,
      color: DEFAULT_LED_COLOR,
      ...config,
    };
    if (this.querySelector("ha-entity-picker")) {
      this.syncControls();
    } else {
      this.render();
    }
  }

  set hass(hass) {
    this._hass = hass;
    const picker = this.querySelector("ha-entity-picker");
    if (picker) {
      picker.hass = hass;
    } else {
      this.render();
    }
  }

  connectedCallback() {
    this.render();
  }

  render() {
    if (!this.config || !this._hass) return;
    if (this.querySelector("ha-entity-picker")) {
      this.syncControls();
      return;
    }

    this.innerHTML = `
      <div class="editor">
        <ha-entity-picker label="Stop sensor" allow-custom-entity></ha-entity-picker>
        <ha-textfield label="Title (optional)"></ha-textfield>
        <ha-textfield label="Number of departures" type="number" min="1" max="10"></ha-textfield>
        <label class="color-field">
          <span>LED text colour</span>
          <span class="color-control">
            <input type="color" aria-label="LED text colour">
            <code class="color-value"></code>
          </span>
        </label>
        <ha-formfield label="Show Live/Scheduled badges">
          <ha-switch></ha-switch>
        </ha-formfield>
      </div>
      <style>
        .editor { display: grid; gap: 16px; padding: 8px 0; }
        .color-field {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 16px;
          color: var(--primary-text-color);
        }
        .color-control { display: flex; align-items: center; gap: 10px; }
        input[type="color"] {
          width: 48px;
          height: 36px;
          padding: 2px;
          border: 1px solid var(--divider-color);
          border-radius: 6px;
          background: transparent;
          cursor: pointer;
        }
        .color-value { color: var(--secondary-text-color); }
      </style>`;

    const picker = this.querySelector("ha-entity-picker");
    picker.includeDomains = ["sensor"];
    picker.hass = this._hass;
    picker.addEventListener("value-changed", (event) =>
      this.updateConfig("entity", event.detail.value)
    );

    const fields = this.querySelectorAll("ha-textfield");
    fields[0].addEventListener("change", (event) =>
      this.updateConfig("title", event.target.value || undefined)
    );
    fields[1].addEventListener("change", (event) =>
      this.updateConfig(
        "departures",
        Math.max(1, Math.min(10, Number(event.target.value) || 5))
      )
    );
    this.querySelector('input[type="color"]').addEventListener("change", (event) =>
      this.updateConfig("color", normaliseColor(event.target.value))
    );
    this.querySelector("ha-switch").addEventListener("change", (event) =>
      this.updateConfig("show_status", event.target.checked)
    );

    this.syncControls();
  }

  syncControls() {
    if (!this.config) return;

    const picker = this.querySelector("ha-entity-picker");
    const fields = this.querySelectorAll("ha-textfield");
    const toggle = this.querySelector("ha-switch");
    const colorInput = this.querySelector('input[type="color"]');
    const colorValue = this.querySelector(".color-value");

    const entity = this.config.entity || "";
    if (picker && picker.value !== entity) picker.value = entity;

    const title = this.config.title || "";
    if (fields[0] && fields[0].value !== title) fields[0].value = title;

    const departures = String(this.config.departures || 5);
    if (fields[1] && fields[1].value !== departures) {
      fields[1].value = departures;
    }

    const color = normaliseColor(this.config.color);
    if (colorInput && colorInput.value !== color) colorInput.value = color;
    if (colorValue && colorValue.textContent !== color.toUpperCase()) {
      colorValue.textContent = color.toUpperCase();
    }

    const showStatus = this.config.show_status !== false;
    if (toggle && toggle.checked !== showStatus) toggle.checked = showStatus;
  }

  updateConfig(key, value) {
    const config = { ...this.config };
    if (value === undefined || value === "") delete config[key];
    else config[key] = value;
    this.dispatchEvent(
      new CustomEvent("config-changed", {
        detail: { config },
        bubbles: true,
        composed: true,
      })
    );
  }
}

if (!customElements.get("brighton-bus-times-card")) {
  customElements.define("brighton-bus-times-card", BrightonBusTimesCard);
}
if (!customElements.get("brighton-bus-times-card-editor")) {
  customElements.define(
    "brighton-bus-times-card-editor",
    BrightonBusTimesCardEditor
  );
}

window.customCards = window.customCards || [];
window.customCards.push({
  type: "brighton-bus-times-card",
  name: "Brighton Bus Times",
  description: "Amber LED-style live bus departure board",
  preview: true,
  documentationURL: "https://brightonbustimes.uk",
});

console.info(`%c BRIGHTON BUS TIMES CARD %c v${CARD_VERSION} `, "color:#ffffff;background:#64CCC9;font-weight:bold", "color:#ffffff;background:#065361");
