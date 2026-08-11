# Brighton Bus Times for Home Assistant

A custom Home Assistant integration for live and scheduled bus departures in Brighton and Hove, powered by [Brighton Bus Times](https://buses.subwavenetwork.uk).

It creates one **Next departure** sensor for each selected stop and includes an LED-style dashboard card inspired by Brighton's roadside bus signs.

> [!NOTE]
> This integration is not yet included in the default HACS catalogue. Install it by adding this repository to HACS as a custom repository, or install it manually.

## Features

- Search for stops by name during setup
- Select multiple stops, including directional indicators such as `(opp)` and `(adj)`
- Manual NaPTAN stop-ID entry when needed
- Live and scheduled departure information
- One Home Assistant device and sensor per stop
- Full departure board data exposed in sensor attributes
- Configurable polling interval from 15 to 300 seconds
- Bundled LED-style Lovelace card with a visual editor
- Configurable LED colour, row count, title, and Live/Scheduled badges
- Embedded dot-matrix fonts with no separate font resource to install

## Installation

### Option 1: HACS custom repository (recommended)

[HACS](https://www.hacs.xyz/) must already be installed and configured.

1. Open **HACS** in Home Assistant.
2. Select the three-dot menu in the top-right corner.
3. Select **Custom repositories**.
4. Enter this repository URL:

   ```text
   https://github.com/MrSleeps/Brighton-Bus-Times-Home-Assistant-Custom-Component
   ```

5. Select **Integration** as the category.
6. Select **Add**.
7. Find and open **Brighton Bus Times** in HACS.
8. Select **Download** and install the latest version.
9. Restart Home Assistant.

HACS installs integrations under your Home Assistant `custom_components` directory. This custom-repository process follows the [official HACS instructions](https://www.hacs.xyz/docs/faq/custom_repositories/).

### Option 2: Manual installation

1. Download the latest release from this repository's [Releases page](https://github.com/MrSleeps/Brighton-Bus-Times-Home-Assistant-Custom-Component/releases).
2. Extract the downloaded archive.
3. Copy the entire `brighton_bus_times` integration directory into Home Assistant so the resulting path is:

   ```text
   /config/custom_components/brighton_bus_times/
   ```

4. Confirm that this file exists:

   ```text
   /config/custom_components/brighton_bus_times/manifest.json
   ```

5. Restart Home Assistant.

Do not copy the repository itself into `custom_components`. Only the directory at `custom_components/brighton_bus_times` belongs there.

## Set up the integration

After installing and restarting Home Assistant:

1. Open **Settings → Devices & services**.
2. Select **Add integration**.
3. Search for **Brighton Bus Times**.
4. Leave the API URL at its default value unless you run a compatible API yourself.
5. Enter at least two characters of a stop name and submit the form.
6. Select one or more matching stops. Directional indicators help distinguish stops on opposite sides of the road.
7. Choose the refresh interval and complete setup.

You can alternatively enter one or more NaPTAN stop IDs manually. Separate multiple IDs with commas or new lines.

The integration uses this API by default:

```text
https://buses.subwavenetwork.uk
```

## Changing stops

Open **Settings → Devices & services → Brighton Bus Times**, then select **Configure**. Add or remove stop IDs and adjust the refresh interval. The integration reloads automatically after the options are saved.

## Entities and attributes

Each selected stop is represented by a Home Assistant device with a **Next departure** sensor. The sensor state is the number of minutes until the next bus; `0` means the bus is due.

The sensor attributes include:

- Stop ID and stop name
- Route and destination
- Live or scheduled status
- Direction and scheduled departure time
- Vehicle reference and distance, when available
- The complete `departures` array
- Routes serving the stop
- Feed update, cache, and source information

## LED departure-board card

The integration bundles the **Brighton Bus Times** Lovelace card. On systems using storage-managed Lovelace resources, the integration registers the JavaScript module automatically.

After installing or updating the integration:

1. Restart Home Assistant.
2. Refresh the Home Assistant app or browser. A hard refresh may be required after card updates.
3. Edit a dashboard and select **Add card**.
4. Search for **Brighton Bus Times**.
5. Select the stop sensor and customise the card in its visual editor.

The editor supports an optional title, the number of departures, the LED text colour, and whether Live/Scheduled badges are displayed.

### Manual card resource fallback

If the card does not appear in the card picker, add its resource manually:

1. Open **Settings → Dashboards → Resources**.
2. Add this URL:

   ```text
   /brighton_bus_times/brighton-bus-times-card.js
   ```

3. Select **JavaScript module** as the resource type.
4. Refresh Home Assistant and try the card picker again.

### Manual card YAML

```yaml
type: custom:brighton-bus-times-card
entity: sensor.second_avenue_opp_next_departure
title: Second Avenue (opp)
departures: 5
show_status: true
color: "#ffad32"
```

Replace the example `entity` with the entity ID created for your stop.

## Updating

### HACS installation

Install the update from **Settings → Updates** or open the repository in HACS and select **Redownload**, then restart Home Assistant.

### Manual installation

Download the latest release and replace the existing contents of:

```text
/config/custom_components/brighton_bus_times/
```

Restart Home Assistant afterwards. A browser or app refresh may also be needed when the bundled card changes.

## Troubleshooting

### The integration does not appear

- Confirm that `/config/custom_components/brighton_bus_times/manifest.json` exists.
- Check that an extra directory level was not introduced while extracting the archive.
- Restart Home Assistant, then clear the browser cache or perform a hard refresh.
- Check **Settings → System → Logs** for errors mentioning `brighton_bus_times`.

### The card does not appear or still shows an older design

- Restart Home Assistant after installing the integration.
- Fully close and reopen the Home Assistant mobile app.
- Hard-refresh the browser to clear its cached JavaScript.
- If needed, add the manual Lovelace resource described above.

### A stop cannot be found

- Try a shorter stop-name search.
- Check the directional indicator before selecting a result.
- Enter the stop's NaPTAN ID manually if you know it.

### The API cannot be reached

Confirm that the Home Assistant host can reach `https://buses.subwavenetwork.uk`. If the service is temporarily unavailable, Home Assistant retains the previous data and reports the coordinator update as failed.

## Repository layout

For HACS compatibility, the integration files must remain in this structure:

```text
custom_components/
└── brighton_bus_times/
    ├── __init__.py
    ├── api.py
    ├── config_flow.py
    ├── const.py
    ├── coordinator.py
    ├── frontend/
    │   └── brighton-bus-times-card.js
    ├── manifest.json
    ├── sensor.py
    ├── strings.json
    └── translations/
        └── en.json
```

## Support

If you find a bug or have a feature request, [open an issue](https://github.com/MrSleeps/Brighton-Bus-Times-Home-Assistant-Custom-Component/issues) and include:

- Your Home Assistant version
- The integration version
- Relevant Home Assistant log entries
- Clear reproduction steps

## Disclaimer

This is an independent community project. It is not affiliated with, endorsed by, or supported by Brighton & Hove Buses or Home Assistant.
